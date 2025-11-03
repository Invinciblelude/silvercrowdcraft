#!/usr/bin/env python3
"""
Extract dominant straight lines (walls) from the floor plan image using OpenCV (Canny + Hough).
Output: docs/assets/cad-previews/floor_lines.svg sized to the source image for simple overlay.
No OCR required.
"""
import cv2
import numpy as np
from pathlib import Path
import xml.etree.ElementTree as ET

SRC = Path('blueprints/classified/ARCH/07-Proposed-FloorPlan.jpg')
OUT_SVG = Path('docs/assets/cad-previews/floor_lines.svg')
OUT_SVG.parent.mkdir(parents=True, exist_ok=True)

img = cv2.imread(str(SRC))
if img is None:
    raise SystemExit(f"Image not found: {SRC}")

h, w = img.shape[:2]
# Preprocess
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Blur to reduce noise
blur = cv2.GaussianBlur(gray, (5,5), 0)
# Edge detection
edges = cv2.Canny(blur, 80, 180, apertureSize=3)
# Dilate a bit to join small gaps
edges = cv2.dilate(edges, np.ones((3,3), np.uint8), iterations=1)

# Hough lines (probabilistic)
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=120, minLineLength=int(min(w,h)*0.05), maxLineGap=10)

# Prepare SVG
svg = ET.Element('svg', {
    'xmlns':'http://www.w3.org/2000/svg',
    'width': str(w),
    'height': str(h),
    'viewBox': f'0 0 {w} {h}',
    'style': 'background: none'
})
# Semi-transparent dark overlay to see lines
# ET.SubElement(svg, 'rect', {'x':'0','y':'0','width':str(w),'height':str(h),'fill':'rgba(0,0,0,0)'})

if lines is not None:
    # Filter and draw
    for l in lines[:,0,:]:
        x1,y1,x2,y2 = map(int, l)
        # Skip tiny segments or very shallow thickness
        length = np.hypot(x2-x1, y2-y1)
        if length < min(w,h)*0.06:
            continue
        # Draw as cyan for visibility
        ET.SubElement(svg, 'line', {
            'x1': str(x1), 'y1': str(y1), 'x2': str(x2), 'y2': str(y2),
            'stroke': '#67e8f9', 'stroke-width': '3', 'stroke-linecap':'round'
        })
else:
    # No lines detected – place a note
    ET.SubElement(svg, 'text', {'x': '20','y':'30','fill':'#f87171','font-size':'20'}).text = 'No lines detected'

ET.ElementTree(svg).write(OUT_SVG, encoding='utf-8', xml_declaration=True)
print(f"✅ Wrote SVG: {OUT_SVG} ({w}x{h})")
