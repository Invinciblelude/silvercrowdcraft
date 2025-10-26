#!/usr/bin/env python3
"""
Extract PDF pages with proper names from the actual blueprint PDF.
This will read text from each page, identify the sheet number/title,
and save JPEGs with meaningful names.
"""

import fitz  # PyMuPDF
from pathlib import Path
import re

PDF_PATH = Path("/Users/invinciblelude/728 Cordant project/blueprints/incoming/728 Cortlandt Drive Plans actual.pdf")
OUTPUT_DIR = Path("/Users/invinciblelude/728 Cordant project/blueprints/classified")

# Classification rules based on sheet prefixes
CLASSIFICATIONS = {
    'A': 'ARCH',
    'S': 'STRUCT', 
    'E': 'MEP/ELEC',
    'M': 'MEP/MECH',
    'P': 'MEP/PLUMB',
    'C': 'CIVIL',
    'L': 'LANDSCAPE',
    'G': 'GENERAL',
}

def extract_sheet_info(page):
    """Extract sheet number and title from a page."""
    text = page.get_text()
    
    # Common patterns for sheet identifiers
    # Example: "A1.1", "S-1", "E2.0", etc.
    patterns = [
        r'\b([A-Z]\d+(?:\.\d+)?)\b',  # A1.1, E2, S3.5
        r'\b([A-Z]-\d+)\b',            # A-1, S-2
        r'SHEET\s+([A-Z]\d+(?:\.\d+)?)',
        r'DRAWING\s+([A-Z]\d+(?:\.\d+)?)',
    ]
    
    sheet_num = None
    for pattern in patterns:
        match = re.search(pattern, text[:1000])  # Search first 1000 chars
        if match:
            sheet_num = match.group(1).replace('-', '')
            break
    
    # Extract title - usually near top, often in all caps
    lines = text.split('\n')[:30]  # First 30 lines
    title_candidates = []
    
    for line in lines:
        line = line.strip()
        # Look for lines that might be titles
        if len(line) > 10 and len(line) < 80:
            # Skip common header info
            if any(skip in line.lower() for skip in ['date', 'scale', 'drawn by', 'checked', 'project', 'sheet']):
                continue
            if line.isupper() and len(line.split()) > 1:
                title_candidates.append(line)
    
    title = title_candidates[0] if title_candidates else "UNKNOWN"
    
    # Clean up title for filename
    title = re.sub(r'[^\w\s-]', '', title)
    title = re.sub(r'\s+', '_', title)
    title = title[:50]  # Limit length
    
    return sheet_num, title

def classify_sheet(sheet_num):
    """Determine classification folder based on sheet number."""
    if not sheet_num:
        return "_unmatched"
    
    prefix = sheet_num[0].upper()
    
    # Check for known prefixes
    if prefix in CLASSIFICATIONS:
        return CLASSIFICATIONS[prefix]
    
    return "_unmatched"

def main():
    if not PDF_PATH.exists():
        print(f"❌ PDF not found: {PDF_PATH}")
        return
    
    print(f"📄 Opening PDF: {PDF_PATH}")
    doc = fitz.open(str(PDF_PATH))
    print(f"📊 Total pages: {doc.page_count}")
    
    # Clear existing classified images
    print("\n🧹 Cleaning old classified images...")
    for folder in OUTPUT_DIR.rglob("*"):
        if folder.is_dir():
            for img in folder.glob("*.jpeg"):
                img.unlink()
                print(f"  Deleted: {img.name}")
    
    print("\n🔍 Extracting pages with proper names...")
    extracted = 0
    
    for page_num in range(doc.page_count):
        page = doc[page_num]
        
        # Extract sheet info
        sheet_num, title = extract_sheet_info(page)
        
        if not sheet_num:
            sheet_num = f"PAGE_{page_num+1:03d}"
        
        # Classify
        category = classify_sheet(sheet_num)
        category_dir = OUTPUT_DIR / category
        category_dir.mkdir(parents=True, exist_ok=True)
        
        # Create filename: SheetNum_Title.jpeg
        filename = f"{sheet_num}_{title}.jpeg"
        output_path = category_dir / filename
        
        # Render page to image at 300 DPI
        mat = fitz.Matrix(300/72, 300/72)  # 300 DPI
        pix = page.get_pixmap(matrix=mat, alpha=False)
        pix.save(str(output_path), "jpeg", jpg_quality=95)
        
        print(f"✅ [{page_num+1}/{doc.page_count}] {category}/{filename}")
        extracted += 1
    
    doc.close()
    
    print(f"\n✨ Extracted {extracted} pages with proper names!")
    print(f"📁 Output: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()

