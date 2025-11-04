"""
OCR to JSON Pipeline

- Accepts a PDF file or a directory of images
- Uses Tesseract (pytesseract) and optional Poppler (pdf2image) to extract text
- Uses OpenCV to detect long line segments (candidate walls)
- Outputs structured JSON matching bim_wall_model.py schema

Configuration:
- Tesseract path via env TESSERACT_CMD or common defaults (/opt/homebrew/bin/tesseract, /usr/local/bin/tesseract)
- Poppler path via env POPPLER_PATH for PDF conversion

Usage examples:
  python3 ocr_to_json.py --pdf "/path/to/plan.pdf" --project 728-cordant --scale-px 2400 --scale-in 480 \
      --stock-plate-length-in 144 --out "/path/out.json"

  python3 ocr_to_json.py --images-dir "/path/to/images" --project TEST --scale-px 1200 --scale-in 240 --out test.json
"""

from __future__ import annotations

import os
import re
import sys
import json
import math
import glob
import shutil
import tempfile
import subprocess
import argparse
from typing import List, Dict, Tuple, Any


def _set_tesseract_path() -> None:
    try:
        import pytesseract  # type: ignore
    except Exception as exc:  # pragma: no cover
        print("pytesseract not installed: pip install pytesseract", file=sys.stderr)
        raise

    # Prefer explicit env, else which(), else common paths
    for candidate in [
        os.environ.get("TESSERACT_CMD"),
        os.environ.get("TESSERACT_PATH"),
        shutil.which("tesseract"),
        "/opt/homebrew/bin/tesseract",
        "/usr/local/bin/tesseract",
        "/usr/bin/tesseract",
        r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
    ]:
        if candidate and os.path.exists(candidate):
            pytesseract.pytesseract.tesseract_cmd = candidate
            return
    # Else leave default; pytesseract will error if not found


def _pdf_to_images_pdftoppm(pdf_path: str, dpi: int = 300) -> List["Image.Image"]:
    from PIL import Image  # type: ignore
    images: List[Image.Image] = []
    poppler_cmd = shutil.which("pdftoppm") or os.environ.get("POPPLER_PATH")
    if not poppler_cmd or not poppler_cmd.strip():
        return images
    with tempfile.TemporaryDirectory() as td:
        out_prefix = os.path.join(td, "page")
        try:
            subprocess.run([poppler_cmd, "-r", str(dpi), pdf_path, out_prefix, "-png"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception:
            return images
        for p in sorted(glob.glob(os.path.join(td, "page-*.png"))):
            try:
                images.append(Image.open(p))
            except Exception:
                pass
    return images


def _load_images(args: argparse.Namespace) -> List["Image.Image"]:
    from PIL import Image  # type: ignore
    images: List[Image.Image] = []
    if args.pdf:
        try:
            from pdf2image import convert_from_path  # type: ignore
        except Exception:
            # Fallback to pdftoppm
            imgs = _pdf_to_images_pdftoppm(args.pdf, dpi=300)
            if imgs:
                images.extend(imgs)
            else:
                print("pdf2image not installed and pdftoppm not found: install one to process PDFs", file=sys.stderr)
                raise
        else:
            poppler_path = os.environ.get("POPPLER_PATH")
            pages = convert_from_path(args.pdf, dpi=300, poppler_path=poppler_path)
            images.extend(pages)
    elif args.images_dir:
        for ext in ("*.png", "*.jpg", "*.jpeg", "*.tif", "*.tiff", "*.bmp"):
            for p in sorted(glob.glob(os.path.join(args.images_dir, ext))):
                try:
                    images.append(Image.open(p))
                except Exception:
                    pass
    else:
        raise SystemExit("Provide either --pdf or --images-dir")
    if not images:
        raise SystemExit("No images found to process")
    return images


def _image_to_cv(img) -> "np.ndarray":
    import numpy as np  # type: ignore
    from PIL import Image  # type: ignore
    if isinstance(img, Image.Image):
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return img


def _preprocess(cv_img: "np.ndarray") -> "np.ndarray":
    # Binarize + deskew (simple)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Estimate skew using Hough on edges
    edges = cv2.Canny(bw, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, math.pi / 180.0, 200)
    angle_deg = 0.0
    if lines is not None and len(lines) > 0:
        angles = []
        for rho, theta in lines[:, 0]:
            a = (theta * 180.0 / math.pi) % 180.0
            if 10 < a < 170:  # ignore near-vertical to reduce noise
                angles.append(a)
        if angles:
            median_angle = sorted(angles)[len(angles)//2]
            angle_deg = median_angle - 90.0
    if abs(angle_deg) > 0.2:
        (h, w) = bw.shape[:2]
        M = cv2.getRotationMatrix2D((w/2, h/2), angle_deg, 1.0)
        bw = cv2.warpAffine(bw, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return bw


def _detect_lines(cv_img: "np.ndarray") -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    import numpy as np  # type: ignore
    bw = _preprocess(cv_img)
    edges = cv2.Canny(bw, 50, 150, apertureSize=3)
    # Probabilistic Hough Transform for line segments
    lines = cv2.HoughLinesP(edges, rho=1, theta=math.pi / 180.0, threshold=120, minLineLength=150, maxLineGap=10)
    segs: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
    if lines is not None:
        for l in lines:
            x1, y1, x2, y2 = map(int, l[0])
            segs.append(((x1, y1), (x2, y2)))
    return segs


def _scale_points(pts: List[Tuple[float, float]], scale_px: float, scale_in: float) -> List[Tuple[float, float]]:
    if scale_px <= 0 or scale_in <= 0:
        return pts
    factor = scale_in / scale_px
    return [(x * factor, y * factor) for (x, y) in pts]


def _segment_to_wall(seg: Tuple[Tuple[int, int], Tuple[int, int]], scale_px: float, scale_in: float, defaults: Dict[str, Any]) -> Dict[str, Any]:
    (x1, y1), (x2, y2) = seg
    sp = _scale_points([(float(x1), float(y1)), (float(x2), float(y2))], scale_px, scale_in)
    (sx, sy), (ex, ey) = sp
    wall = {
        "id": f"W-{int(sx)}_{int(sy)}_{int(ex)}_{int(ey)}",
        "start_pt": [round(sx, 2), round(sy, 2)],
        "end_pt": [round(ex, 2), round(ey, 2)],
        "stud_size": defaults.get("stud_size", "2x4"),
        "stud_spacing": defaults.get("stud_spacing", 16),
        "wall_height": defaults.get("wall_height", 96),
        "is_load_bearing": bool(defaults.get("is_load_bearing", True)),
        "ro_openings": [],
        "utilities": [],
    }
    return wall


def _perform_ocr(cv_img: "np.ndarray", psm: int = 4) -> List[Dict[str, Any]]:
    # Returns list of {text, x, y, w, h}
    import pytesseract  # type: ignore
    config = f"--psm {psm}"
    data = pytesseract.image_to_data(cv_img, config=config, output_type=pytesseract.Output.DICT)
    n = len(data.get("text", []))
    out: List[Dict[str, Any]] = []
    for i in range(n):
        txt = (data["text"][i] or "").strip()
        if not txt:
            continue
        out.append({
            "text": txt,
            "x": int(data.get("left", [0])[i]),
            "y": int(data.get("top", [0])[i]),
            "w": int(data.get("width", [0])[i]),
            "h": int(data.get("height", [0])[i]),
        })
    return out


_RE_INCH_VAL = re.compile(r"(?:(\d+)'[ -]?)?(\d+(?:\.\d+)?)\"?")


def _parse_inches(token: str) -> float | None:
    # Supports 12' 6", 12'-6", 12', 144", 144
    t = token.strip().lower()
    if t.endswith('in'):
        t = t[:-2]
    if '"' in t or "'" in t or '-' in t or ' ' in t:
        m = _RE_INCH_VAL.search(token.replace('in', ''))
        if not m:
            return None
        feet = m.group(1)
        inch = m.group(2)
        return (float(feet) * 12.0 if feet else 0.0) + float(inch)
    try:
        return float(t)
    except Exception:
        return None


def _project_point_to_segment(px: float, py: float, ax: float, ay: float, bx: float, by: float) -> Tuple[float, float, float]:
    # Returns (t, projx, projy) with t in [0,1]
    vx, vy = bx - ax, by - ay
    wx, wy = px - ax, py - ay
    seg_len2 = vx * vx + vy * vy
    if seg_len2 == 0:
        return 0.0, ax, ay
    t = max(0.0, min(1.0, (wx * vx + wy * vy) / seg_len2))
    projx, projy = ax + t * vx, ay + t * vy
    return t, projx, projy


def _map_keywords_to_wall(ocr_words: List[Dict[str, Any]], wall_px: Tuple[Tuple[float, float], Tuple[float, float]], scale_px: float, scale_in: float) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    # Returns (ro_openings, utilities)
    (ax, ay), (bx, by) = wall_px
    ro_list: List[Dict[str, Any]] = []
    utils: List[Dict[str, Any]] = []
    for i, w in enumerate(ocr_words):
        word = w["text"].upper()
        cx = w["x"] + w["w"] / 2.0
        cy = w["y"] + w["h"] / 2.0
        if word.startswith("WINDOW"):
            # Search nearby tokens for WIDTH, HT/HEIGHT, SILL, CL, START_X
            width_in = None
            height_in = None
            sill_in = None
            start_x_in = None
            for j in range(i + 1, min(i + 8, len(ocr_words))):
                t = ocr_words[j]["text"].upper()
                val = _parse_inches(t)
                if "WIDTH" in t or t == "WIDTH":
                    continue
                if "HT" in t or "HEIGHT" in t:
                    continue
                if "SILL" in t:
                    continue
                # Assign by order if inches
                if val is not None:
                    if width_in is None:
                        width_in = val
                        continue
                    if height_in is None:
                        height_in = val
                        continue
                    if sill_in is None:
                        sill_in = val
                        continue
            # Position along wall: project WINDOW label center
            t, projx, projy = _project_point_to_segment(cx, cy, ax, ay, bx, by)
            along_px = math.hypot(projx - ax, projy - ay)
            scale = scale_in / scale_px if scale_px > 0 else 1.0
            start_x_in = along_px * scale
            if width_in is not None:
                ro_list.append({
                    "TYPE": "Window",
                    "START_X": round(float(start_x_in), 2),
                    "WIDTH": float(width_in),
                    "HEIGHT": float(height_in or 48.0),
                    "SILL_HGT": float(sill_in or 44.0),
                })
        elif word.startswith("OUTLET"):
            # Find an inches value near token; else use projection
            xloc_in = None
            for j in range(i + 1, min(i + 5, len(ocr_words))):
                val = _parse_inches(ocr_words[j]["text"]) or None
                if val is not None:
                    xloc_in = val
                    break
            if xloc_in is None:
                t, projx, projy = _project_point_to_segment(cx, cy, ax, ay, bx, by)
                along_px = math.hypot(projx - ax, projy - ay)
                xloc_in = along_px * (scale_in / scale_px if scale_px > 0 else 1.0)
            utils.append({
                "TYPE": "OUTLET",
                "X_LOC": round(float(xloc_in), 2),
                "OUTLET_TYPE": "STANDARD" if "GFCI" not in word else "GFCI",
            })
        elif word.startswith("PLUMBING") or word.startswith("DRAIN"):
            xloc_in = None
            diameter = None
            for j in range(i + 1, min(i + 6, len(ocr_words))):
                t = ocr_words[j]["text"].upper()
                if "DIA" in t or "DIAM" in t:
                    # take next inches number
                    if j + 1 < len(ocr_words):
                        diameter = _parse_inches(ocr_words[j + 1]["text"]) or diameter
                v = _parse_inches(ocr_words[j]["text"]) or None
                if v is not None and xloc_in is None:
                    xloc_in = v
            if xloc_in is None:
                t, projx, projy = _project_point_to_segment(cx, cy, ax, ay, bx, by)
                along_px = math.hypot(projx - ax, projy - ay)
                xloc_in = along_px * (scale_in / scale_px if scale_px > 0 else 1.0)
            utils.append({
                "TYPE": "PLUMBING_DRAIN",
                "X_LOC": round(float(xloc_in), 2),
                "DIAMETER": float(diameter or 2.0),
            })
    return ro_list, utils


def build_project_json(project: str, defaults: Dict[str, Any], walls: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "project": project,
        "units": "inches",
        "defaults": {
            "stud_size": defaults.get("stud_size", "2x4"),
            "stud_spacing": defaults.get("stud_spacing", 16),
            "wall_height": defaults.get("wall_height", 96),
            "header_depth_map": {"2x4": 3.0, "2x6": 4.5},
            "is_load_bearing": bool(defaults.get("is_load_bearing", True)),
            "stock_plate_length_in": float(defaults.get("stock_plate_length_in", 144)),
        },
        "calibration": {
            "origin": [0, 0],
            "axis": {"x": "east", "y": "north"}
        },
        "walls": walls,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="OCR/Vectorization to framing JSON")
    parser.add_argument("--pdf", help="Input PDF path", required=False)
    parser.add_argument("--images-dir", help="Directory of images", required=False)
    parser.add_argument("--project", help="Project name", required=True)
    parser.add_argument("--scale-px", type=float, help="Pixel length for calibration", required=True)
    parser.add_argument("--scale-in", type=float, help="True inches corresponding to --scale-px", required=True)
    parser.add_argument("--stock-plate-length-in", type=float, default=144.0, help="Stock plate length (inches)")
    parser.add_argument("--psm", type=int, default=4, help="Tesseract PSM mode (e.g., 3,4,6)")
    parser.add_argument("--out", help="Output JSON path", required=True)
    args = parser.parse_args()

    # Configure engines
    _set_tesseract_path()
    try:
        import cv2  # type: ignore
        globals()["cv2"] = cv2
    except Exception:
        print("opencv-python not installed: pip install opencv-python", file=sys.stderr)
        raise

    images = _load_images(args)
    all_walls: List[Dict[str, Any]] = []
    # Defaults for walls
    defaults = {
        "stud_size": "2x4",
        "stud_spacing": 16,
        "wall_height": 96,
        "is_load_bearing": True,
        "stock_plate_length_in": float(args.stock_plate_length_in),
    }

    page_idx = 0
    for pil_img in images:
        page_idx += 1
        cv_img = _image_to_cv(pil_img)
        # Preprocess and OCR
        try:
            bw = _preprocess(cv_img)
            ocr_words = _perform_ocr(bw, psm=args.psm)
        except Exception:
            ocr_words = []
        # Line detection to approximate walls (choose longest per page for MVP)
        try:
            segs = _detect_lines(cv_img)
        except Exception:
            segs = []
        if segs:
            segs_sorted = sorted(segs, key=lambda s: math.hypot(s[1][0]-s[0][0], s[1][1]-s[0][1]), reverse=True)
            primary = segs_sorted[0]
            wall = _segment_to_wall(primary, args.scale_px, args.scale_in, defaults)
            # Map keywords to along-wall distances
            (x1, y1), (x2, y2) = primary
            ro_list, utils = _map_keywords_to_wall(ocr_words, ((float(x1), float(y1)), (float(x2), float(y2))), args.scale_px, args.scale_in)
            wall["ro_openings"] = ro_list
            wall["utilities"] = utils
            all_walls.append(wall)

    project_json = build_project_json(project=args.project, defaults=defaults, walls=all_walls)
    with open(args.out, "w") as f:
        json.dump(project_json, f, indent=2)
    print(f"JSON written: {args.out}")


if __name__ == "__main__":
    main()


