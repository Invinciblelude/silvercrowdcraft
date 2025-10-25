#!/usr/bin/env python3
import json
import re
import subprocess
from pathlib import Path

try:
    import pytesseract
    from PIL import Image
except Exception as e:
    pytesseract = None

ROOT = Path("/Users/invinciblelude/728 Cordant project/blueprints")
OUT_JSON = Path("/Users/invinciblelude/728 Cordant project/site/assets/ocr.json")

SHEET_RX = re.compile(r"\b([ASMEPCLGTD])[\s-]?\d{1,2}(?:\.\d+)?\b")
CALLOUT_RX = re.compile(r"\b(\d+)\s*/\s*([ASMEPCLGTD]-?\d+(?:\.\d+)?)\b")
TITLE_HINTS = ["FLOOR PLAN","ELECTRICAL","PLUMBING","MECHANICAL","SECTION","DETAIL","ELEVATION","SITE","GENERAL","SCHEDULE"]


def have_tesseract():
    from shutil import which
    return which("tesseract") is not None


def ocr_image(path: Path) -> str:
    if pytesseract and have_tesseract():
        try:
            return pytesseract.image_to_string(Image.open(path))
        except Exception:
            return ""
    # Fallback: try tesseract CLI directly if wrapper missing
    if have_tesseract():
        try:
            out = subprocess.check_output(["tesseract", str(path), "stdout"], stderr=subprocess.DEVNULL)
            return out.decode("utf-8", errors="ignore")
        except Exception:
            return ""
    return ""  # no OCR available


def parse_fields(text: str):
    text_up = text.upper()
    sheet = None
    m = SHEET_RX.search(text_up)
    if m:
        sheet = m.group(0)
    callouts = [f"{n}/{s}" for n,s in CALLOUT_RX.findall(text_up)]
    title = None
    for hint in TITLE_HINTS:
        if hint in text_up:
            title = hint
            break
    return sheet, title, callouts


def collect_images():
    folders = [ROOT/"classified"/"ARCH", ROOT/"classified"/"STRUCT", ROOT/"classified"/"MEP"/"ELEC",
               ROOT/"classified"/"MEP"/"MECH", ROOT/"classified"/"MEP"/"PLUMB", ROOT/"classified"/"CIVIL",
               ROOT/"classified"/"SITE", ROOT/"classified"/"LANDSCAPE", ROOT/"classified"/"DETAILS",
               ROOT/"classified"/"SCHEDULES", ROOT/"classified"/"GENERAL", ROOT/"_unmatched"]
    images = []
    for folder in folders:
        if not folder.exists():
            continue
        for ext in ("*.jpg","*.jpeg","*.png","*.JPG","*.JPEG","*.PNG"):
            for p in folder.glob(ext):
                images.append(p)
    return images


def main():
    imgs = collect_images()
    results = {}
    for p in imgs:
        text = ocr_image(p)
        sheet, title, callouts = parse_fields(text)
        results[str(p)] = {
            "sheet": sheet,
            "title_hint": title,
            "callouts": callouts,
            "text_sample": (text[:400] or "").replace("\n"," ")
        }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, 'w') as f:
        json.dump(results, f)
    if not have_tesseract():
        print("Note: Tesseract not installed; OCR may be empty. Install via Homebrew or pkg and rerun.")
    print(f"Wrote {OUT_JSON} with {len(results)} entries")

if __name__ == "__main__":
    main()
