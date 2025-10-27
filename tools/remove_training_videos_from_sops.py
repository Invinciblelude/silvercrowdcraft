#!/usr/bin/env python3
"""
Remove hardcoded training video sections from all SOP HTML files.
Keeps the YouTube search bar functionality.
"""

import os
import re

def remove_training_videos_from_sop(filepath):
    """Remove the training videos section from an SOP file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and remove the training videos section
        # Pattern to match the entire training videos section including the wrapping div
        pattern = r'<div class="section"[^>]*>\s*<h2>🎓 Training Videos - Learn the Skills</h2>.*?</div>\s*</div>\s*'
        
        # Remove the section
        new_content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # Only write if content changed
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
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
            if remove_training_videos_from_sop(filepath):
                modified_count += 1
                print(f"✓ Removed videos from: {filename}")
    
    print(f"\n✅ Complete! Removed training videos section from {modified_count} SOPs")
    print(f"📺 YouTube search bar remains intact for worker use")

if __name__ == '__main__':
    main()

