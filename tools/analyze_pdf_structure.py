#!/usr/bin/env python3
"""
Analyze the PDF structure to extract:
- Sheet numbers and titles
- Materials lists
- Room schedules
- Notes and specifications
- Construction details
"""

import fitz  # PyMuPDF
from pathlib import Path
import json
import re

PDF_PATH = Path("/Users/invinciblelude/728 Cordant project/blueprints/incoming/728 Cortlandt Drive Plans actual.pdf")
OUTPUT_JSON = Path("/Users/invinciblelude/728 Cordant project/docs/assets/blueprint_data.json")

def extract_page_data(page, page_num):
    """Extract structured data from a page."""
    text = page.get_text()
    
    # Try to find sheet number
    sheet_patterns = [
        r'SHEET\s*[:#]?\s*([A-Z][-\d\.]+)',
        r'DRAWING\s*[:#]?\s*([A-Z][-\d\.]+)',
        r'\b([A-Z]\d+(?:\.\d+)?)\b',
        r'\b([A-Z]-\d+)\b',
    ]
    
    sheet_num = None
    for pattern in sheet_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            sheet_num = match.group(1).strip().replace(' ', '')
            break
    
    if not sheet_num:
        sheet_num = f"PAGE-{page_num+1}"
    
    # Extract title (usually prominent text near top)
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # Look for title candidates
    title = "Untitled"
    for i, line in enumerate(lines[:40]):  # Check first 40 lines
        # Skip common non-title text
        if any(skip in line.lower() for skip in ['date:', 'scale:', 'drawn', 'checked', 'project #', 'sheet']):
            continue
        # Title is usually longer, in caps, meaningful
        if len(line) > 8 and len(line) < 100:
            if line.isupper() or line.istitle():
                # Avoid coordinates and measurements
                if not re.search(r'\d+["\']|\d+\s*x\s*\d+', line):
                    title = line
                    break
    
    # Clean title
    title = re.sub(r'[^\w\s\-/]', '', title)
    title = re.sub(r'\s+', ' ', title).strip()
    
    # Determine category
    category = categorize_sheet(sheet_num, title, text)
    
    # Extract key info
    notes = extract_notes(text)
    materials = extract_materials(text)
    
    return {
        'page_num': page_num + 1,
        'sheet_num': sheet_num,
        'title': title,
        'category': category,
        'notes': notes[:500] if notes else '',  # Limit size
        'materials': materials[:10],  # Top 10 materials
        'text_preview': text[:300]  # First 300 chars for search
    }

def categorize_sheet(sheet_num, title, text):
    """Determine what category/trade this sheet belongs to."""
    sheet_upper = sheet_num.upper()
    title_lower = title.lower()
    text_lower = text.lower()
    
    # Architecture/General
    if sheet_upper.startswith('A') or 'floor plan' in title_lower or 'elevation' in title_lower:
        if 'foundation' in text_lower or 'footing' in text_lower:
            return 'Foundation'
        elif 'roof' in title_lower or 'roof' in text_lower[:500]:
            return 'Roofing'
        elif 'framing' in text_lower or 'wall section' in title_lower:
            return 'Framing'
        elif 'door' in title_lower or 'window' in title_lower:
            return 'Doors & Windows'
        return 'Architectural'
    
    # Structural
    if sheet_upper.startswith('S') or 'structural' in title_lower:
        return 'Structural'
    
    # Electrical
    if sheet_upper.startswith('E') or 'electrical' in title_lower or 'lighting' in title_lower:
        return 'Electrical'
    
    # Mechanical
    if sheet_upper.startswith('M') or 'mechanical' in title_lower or 'hvac' in title_lower:
        return 'HVAC'
    
    # Plumbing
    if sheet_upper.startswith('P') or 'plumbing' in title_lower or 'plumb' in title_lower:
        return 'Plumbing'
    
    # Civil/Site
    if sheet_upper.startswith('C') or 'site' in title_lower or 'grading' in title_lower:
        return 'Site & Civil'
    
    # Landscape
    if sheet_upper.startswith('L') or 'landscape' in title_lower:
        return 'Landscape'
    
    # Details
    if 'detail' in title_lower or 'section' in title_lower:
        return 'Details'
    
    # Index/Cover
    if 'index' in title_lower or 'drawing list' in title_lower or 'cover' in title_lower:
        return 'Index'
    
    return 'General'

def extract_notes(text):
    """Extract general notes section."""
    notes = []
    lines = text.split('\n')
    
    # Find "GENERAL NOTES" or "NOTES" section
    in_notes = False
    for line in lines:
        line = line.strip()
        if re.match(r'^(GENERAL\s+)?NOTES?:?$', line, re.IGNORECASE):
            in_notes = True
            continue
        if in_notes:
            # Stop at next section header
            if line.isupper() and len(line) > 15 and ':' not in line:
                break
            if line and not line.startswith('_'):
                notes.append(line)
    
    return '\n'.join(notes[:20])  # First 20 note lines

def extract_materials(text):
    """Extract material callouts."""
    materials = []
    
    # Common material patterns
    patterns = [
        r'\b\d+"?\s*x\s*\d+"?\s+\w+',  # 2x4, 2"x4", etc
        r'\b\d+"\s+\w+',  # 6" concrete
        r'#\d+\s+\w+',  # #4 rebar
        r'\b[A-Z\d]+\s+(?:lumber|plywood|concrete|steel|rebar)',
    ]
    
    lines = text.split('\n')
    for line in lines:
        for pattern in patterns:
            matches = re.findall(pattern, line, re.IGNORECASE)
            materials.extend(matches)
    
    # Deduplicate and limit
    return list(set(materials))[:10]

def main():
    if not PDF_PATH.exists():
        print(f"❌ PDF not found: {PDF_PATH}")
        return
    
    print(f"📄 Analyzing PDF: {PDF_PATH}")
    doc = fitz.open(str(PDF_PATH))
    print(f"📊 Total pages: {doc.page_count}\n")
    
    all_pages = []
    
    for page_num in range(doc.page_count):
        page = doc[page_num]
        data = extract_page_data(page, page_num)
        all_pages.append(data)
        
        print(f"✅ Page {data['page_num']}: [{data['category']}] {data['sheet_num']} - {data['title'][:60]}")
    
    doc.close()
    
    # Group by category
    by_category = {}
    for page in all_pages:
        cat = page['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(page)
    
    output = {
        'project': {
            'name': '728 Cortlandt Drive',
            'address': '728 Cortlandt Drive',
            'total_pages': len(all_pages),
        },
        'pages': all_pages,
        'by_category': by_category
    }
    
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✨ Analysis complete!")
    print(f"📁 Saved to: {OUTPUT_JSON}")
    print(f"\n📊 Categories found:")
    for cat, pages in sorted(by_category.items()):
        print(f"  - {cat}: {len(pages)} pages")

if __name__ == "__main__":
    main()

