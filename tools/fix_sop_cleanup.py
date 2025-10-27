#!/usr/bin/env python3
"""
Fix SOPs by removing all remaining video content and fixing HTML structure.
"""

import os
import re

def fix_sop_file(filepath):
    """Clean up remaining video content and fix HTML structure."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove any standalone video cards and broken tags
        # Pattern 1: Remove standalone closing </a> tags
        content = re.sub(r'^\s*</a>\s*$', '', content, flags=re.MULTILINE)
        
        # Pattern 2: Remove video card blocks
        content = re.sub(
            r'<a href="https://www\.youtube\.com/watch\?v=[^"]*"[^>]*>.*?</a>\s*',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Pattern 3: Remove any remaining video-grid divs
        content = re.sub(r'<div class="video-grid">.*?</div>', '', content, flags=re.DOTALL)
        
        # Pattern 4: Clean up multiple blank lines
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        # Fix: Close any unclosed div before Quality Control section
        # Find Quality Control section
        qc_match = re.search(r'(<div class="section">\s*<h2>✅ Quality Control)', content)
        if qc_match:
            before_qc = content[:qc_match.start()]
            qc_and_after = content[qc_match.start():]
            
            # Count opening and closing div tags before QC
            open_divs = before_qc.count('<div')
            close_divs = before_qc.count('</div>')
            
            # If there are unclosed divs, close them
            if open_divs > close_divs:
                missing_closes = open_divs - close_divs
                before_qc += '\n    </div>\n' * missing_closes
            
            content = before_qc + qc_and_after
        
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
    docs_dir = os.path.join(os.path.dirname(__file__), '..', 'docs')
    sops_dir = os.path.join(docs_dir, 'sops')
    
    if not os.path.exists(sops_dir):
        print(f"Error: SOPs directory not found at {sops_dir}")
        return
    
    # Process all HTML files in the sops directory
    modified_count = 0
    for filename in sorted(os.listdir(sops_dir)):
        if filename.endswith('.html'):
            filepath = os.path.join(sops_dir, filename)
            if fix_sop_file(filepath):
                modified_count += 1
                print(f"✓ Fixed: {filename}")
    
    print(f"\n✅ Complete! Fixed {modified_count} SOPs")
    print(f"🎯 Removed all video cards and fixed HTML structure")

if __name__ == '__main__':
    main()

