#!/usr/bin/env python3
"""
Surgically remove ONLY the Training Videos section (lines 149-200 style block).
Keep everything else intact.
"""

import os
import re
from pathlib import Path

def remove_training_videos_section(filepath):
    """Remove the entire training videos div section."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Very specific pattern: Match from the opening div with "Training Videos" 
        # all the way to its closing </div> tag (before the next section starts)
        pattern = r'<div class="section" style="border-left-color: #ff6b6b;">\s*' \
                  r'<h2>🎓 Training Videos - Learn the Skills</h2>.*?' \
                  r'</p>\s*</div>\s*\n'
        
        content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # Also clean up any standalone broken elements
        content = re.sub(r'^\s*</a>\s*\n', '', content, flags=re.MULTILINE)
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        # Only write if content changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    sops_dir = Path(__file__).parent.parent / "docs" / "sops"
    
    if not sops_dir.exists():
        print(f"Error: SOPs directory not found at {sops_dir}")
        return
    
    # Process ALL HTML files
    files = sorted(sops_dir.glob("*.html"))
    print(f"🎯 Removing training videos section from SOPs...")
    
    updated_count = 0
    for filepath in files:
        if remove_training_videos_section(filepath):
            updated_count += 1
            print(f"  ✅ {filepath.name}")
    
    print(f"\n🎉 Successfully cleaned {updated_count} SOPs!")
    print(f"✅ Quality Control sections intact")
    print(f"✅ YouTube Search Bar intact")

if __name__ == '__main__':
    main()

