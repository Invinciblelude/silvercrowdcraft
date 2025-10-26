#!/usr/bin/env python3
"""
Rebuild blueprint index from actual files in classified folders.
"""

import json
from pathlib import Path
import re

CLASSIFIED_DIR = Path("/Users/invinciblelude/728 Cordant project/docs/blueprints/classified")
OUTPUT_JSON = Path("/Users/invinciblelude/728 Cordant project/docs/assets/blueprint_data.json")

def extract_sheet_from_filename(filename):
    """Try to extract sheet number from filename."""
    # Match patterns like: 02-AsBuilt, A1.02, C31401, etc.
    patterns = [
        r'^(\d{2})-',  # 02-AsBuilt
        r'^([A-Z]\d+\.?\d*)',  # A1.02, A1, S2
        r'^([A-Z]\d{5})',  # C31401
    ]
    
    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            return match.group(1)
    
    return filename.split('.')[0]  # Fallback to name without extension

def clean_title(filename):
    """Extract title from filename."""
    # Remove extension
    name = Path(filename).stem
    
    # Remove sheet number prefix
    name = re.sub(r'^\d{2}-', '', name)
    name = re.sub(r'^[A-Z]\d+\.?\d*_', '', name)
    name = re.sub(r'^[A-Z]\d{5}_', '', name)
    
    # Replace underscores and hyphens with spaces
    name = name.replace('_', ' ').replace('-', ' ')
    
    # Title case
    name = name.title()
    
    return name

def main():
    print("🔍 Scanning for blueprint images...")
    
    all_pages = []
    page_num = 1
    
    # Scan all category folders
    for category_dir in sorted(CLASSIFIED_DIR.iterdir()):
        if not category_dir.is_dir() or category_dir.name.startswith('.'):
            continue
        
        category = category_dir.name.replace('_unmatched', 'Unmatched')
        
        # Find all images
        images = sorted(list(category_dir.glob('*.jpg')) + list(category_dir.glob('*.jpeg')))
        
        for img_path in images:
            sheet_num = extract_sheet_from_filename(img_path.name)
            title = clean_title(img_path.name)
            
            # Relative path from docs root
            rel_path = f"blueprints/classified/{category}/{img_path.name}"
            
            page_data = {
                'page_num': page_num,
                'sheet_num': sheet_num,
                'title': title,
                'category': category,
                'image_path': rel_path,
                'filename': img_path.name
            }
            
            all_pages.append(page_data)
            print(f"✅ [{page_num}] {category}/{sheet_num} - {title}")
            page_num += 1
    
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
    
    print(f"\n✨ Rebuilt index with {len(all_pages)} pages!")
    print(f"📁 Saved to: {OUTPUT_JSON}")
    print(f"\n📊 Categories:")
    for cat, pages in sorted(by_category.items()):
        print(f"  - {cat}: {len(pages)} pages")

if __name__ == "__main__":
    main()

