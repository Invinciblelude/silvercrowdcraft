#!/usr/bin/env python3
"""
Remove ONLY the hardcoded video cards section, keeping Quality Control and YouTube Search Bar intact.
"""

import os
import re
from pathlib import Path

def remove_hardcoded_videos(filepath):
    """Remove leftover video card elements."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove orphaned closing </a> tags
        content = re.sub(r'^\s*</a>\s*$', '', content, flags=re.MULTILINE)
        
        # Remove any video card anchor tags (YouTube links with video-card class)
        content = re.sub(
            r'<a href="https://www\.youtube\.com/watch\?v=[^"]*"[^>]*class="video-card"[^>]*>.*?</a>\s*',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Remove video-grid div sections
        content = re.sub(
            r'<div class="video-grid">.*?</div>',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Remove the video tip paragraph
        content = re.sub(
            r'<p style="color: #8a98ab[^"]*"[^>]*>\s*💡 <strong>Tip:</strong> Watch these videos before starting the task.*?</p>\s*',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Clean up excessive whitespace
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
    print(f"🎯 Removing hardcoded videos from {len(files)} SOP files...")
    print(f"   (Keeping Quality Control and YouTube Search Bar)")
    
    updated_count = 0
    for filepath in files:
        if remove_hardcoded_videos(filepath):
            updated_count += 1
            print(f"  ✅ {filepath.name}")
    
    print(f"\n🎉 Successfully removed hardcoded videos from {updated_count} SOPs!")
    print(f"✅ Quality Control sections intact")
    print(f"✅ YouTube Search Bar intact")

if __name__ == '__main__':
    main()

