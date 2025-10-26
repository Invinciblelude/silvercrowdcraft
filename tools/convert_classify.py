#!/usr/bin/env python3
"""
Convert PDFs → JPEGs and auto-classify by trade.
"""
from pathlib import Path
import fitz  # PyMuPDF
import re
import shutil

# Paths
ROOT = Path('/Users/invinciblelude/728 Cordant project')
INCOMING = ROOT / 'blueprints' / 'incoming'
UNMATCHED = ROOT / 'blueprints' / '_unmatched'
CLASSIFIED = ROOT / 'blueprints' / 'classified'

CATEGORIES = {
    'ARCH': CLASSIFIED / 'ARCH',
    'STRUCT': CLASSIFIED / 'STRUCT',
    'ELEC': CLASSIFIED / 'MEP' / 'ELEC',
    'MECH': CLASSIFIED / 'MEP' / 'MECH',
    'PLUMB': CLASSIFIED / 'MEP' / 'PLUMB',
    'CIVIL': CLASSIFIED / 'CIVIL',
    'SITE': CLASSIFIED / 'SITE',
    'LANDSCAPE': CLASSIFIED / 'LANDSCAPE',
    'DETAILS': CLASSIFIED / 'DETAILS',
    'SCHEDULES': CLASSIFIED / 'SCHEDULES',
    'GENERAL': CLASSIFIED / 'GENERAL',
}

# Classification patterns
PATTERNS = [
    (r'\bA[\s-]?\d', 'ARCH'),
    (r'\bARCH', 'ARCH'),
    (r'\bFLOOR\s*PLAN', 'ARCH'),
    (r'\bELEVATION', 'ARCH'),
    (r'\bS[\s-]?\d', 'STRUCT'),
    (r'\bSTRUC', 'STRUCT'),
    (r'\bFOUNDATION', 'STRUCT'),
    (r'\bFRAMING', 'STRUCT'),
    (r'\bE[\s-]?\d', 'ELEC'),
    (r'\bELEC', 'ELEC'),
    (r'\bM[\s-]?\d', 'MECH'),
    (r'\bMECH', 'MECH'),
    (r'\bHVAC', 'MECH'),
    (r'\bP[\s-]?\d', 'PLUMB'),
    (r'\bPLUMB', 'PLUMB'),
    (r'\bC[\s-]?\d', 'CIVIL'),
    (r'\bCIVIL', 'CIVIL'),
    (r'\bSITE', 'SITE'),
    (r'\bLAND', 'LANDSCAPE'),
    (r'\bDETAIL', 'DETAILS'),
    (r'\bSCHED', 'SCHEDULES'),
    (r'\bCOVER', 'GENERAL'),
    (r'\bINDEX', 'GENERAL'),
    (r'\bABBREV', 'GENERAL'),
]


def ensure_dirs():
    """Create all category directories."""
    UNMATCHED.mkdir(parents=True, exist_ok=True)
    for d in CATEGORIES.values():
        d.mkdir(parents=True, exist_ok=True)


def convert_pdf_to_jpegs(pdf_path: Path) -> list[Path]:
    """Convert all pages of PDF → JPEGs at 300 DPI."""
    doc = fitz.open(str(pdf_path))
    jpegs = []
    for i in range(len(doc)):
        page = doc.load_page(i)
        mat = fitz.Matrix(300 / 72, 300 / 72)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        out = INCOMING / f"{pdf_path.stem}-{i+1:03d}.jpg"
        pix.save(out, "jpeg", jpg_quality=95)
        jpegs.append(out)
        print(f"  Page {i+1:03d} → {out.name}")
    doc.close()
    return jpegs


def classify_page(pdf_path: Path, page_idx: int, jpeg: Path):
    """Extract text from PDF page and classify."""
    doc = fitz.open(str(pdf_path))
    page = doc.load_page(page_idx)
    text = page.get_text().upper()
    doc.close()

    category = None
    for pattern, cat in PATTERNS:
        if re.search(pattern, text):
            category = cat
            break

    if category:
        dest_dir = CATEGORIES[category]
        dest = dest_dir / jpeg.name
        shutil.move(str(jpeg), str(dest))
        print(f"  → {category}: {jpeg.name}")
    else:
        dest = UNMATCHED / jpeg.name
        shutil.move(str(jpeg), str(dest))
        print(f"  → UNMATCHED: {jpeg.name}")


def main():
    ensure_dirs()
    pdfs = list(INCOMING.rglob('*.pdf'))
    print(f"Found {len(pdfs)} PDF(s)\n")

    for pdf in pdfs:
        print(f"Processing: {pdf.name}")
        jpegs = convert_pdf_to_jpegs(pdf)
        for i, jpeg in enumerate(jpegs):
            classify_page(pdf, i, jpeg)
        print()

    print("✅ Conversion & classification complete")


if __name__ == '__main__':
    main()

