#!/usr/bin/env python3
"""
Add YouTube search bar to ALL SOP HTML files (not just ones in JSON).
"""

import os
import re
from pathlib import Path

def get_youtube_search_html(task_name_search):
    """Generate the YouTube search bar HTML."""
    return f'''
    <div class="section" style="border-left-color: #FF0000;">
      <h2>🎥 Search YouTube Tutorials</h2>
      <p style="color: #a9b6c6; font-size: 14px; margin-bottom: 16px;">
        Search for video tutorials on YouTube. The search is pre-filled with this task, but you can modify it to find exactly what you need.
      </p>
      
      <div class="youtube-search-container">
        <form id="youtubeSearchForm" onsubmit="event.preventDefault(); searchYouTube();" style="display: flex; gap: 8px; margin-bottom: 12px;">
          <input 
            type="text" 
            id="youtubeSearchInput" 
            placeholder="Search YouTube tutorials..."
            value="{task_name_search}"
            style="flex: 1; padding: 12px 16px; border: 2px solid #667eea; border-radius: 6px; background: #0f1317; color: #e8eef5; font-size: 14px; outline: none;"
          >
          <button 
            type="submit"
            style="padding: 12px 24px; background: #FF0000; color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 14px; transition: all 0.2s;"
            onmouseover="this.style.background='#CC0000'"
            onmouseout="this.style.background='#FF0000'"
          >
            🔍 Search
          </button>
        </form>
        
        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px;">
          <button onclick="quickSearch('how to')" class="quick-search-btn">How To</button>
          <button onclick="quickSearch('tutorial')" class="quick-search-btn">Tutorial</button>
          <button onclick="quickSearch('step by step')" class="quick-search-btn">Step by Step</button>
          <button onclick="quickSearch('professional')" class="quick-search-btn">Professional</button>
        </div>
        
        <div id="youtubeResults" style="margin-top: 16px;"></div>
        
        <p style="color: #8a98ab; font-size: 12px; margin-top: 16px;">
          💡 <strong>Tip:</strong> Add terms like "how to", "tutorial", "step by step", or specific tool names for better results.
        </p>
      </div>
      
      <script>
        function searchYouTube() {{
          const searchTerm = document.getElementById('youtubeSearchInput').value;
          const url = 'https://www.youtube.com/results?search_query=' + encodeURIComponent(searchTerm);
          const resultsDiv = document.getElementById('youtubeResults');
          resultsDiv.innerHTML = '<iframe src="' + url + '" style="width: 100%; height: 600px; border: 2px solid #667eea; border-radius: 8px; background: #0f1317;"></iframe>';
        }}
        
        function quickSearch(modifier) {{
          const currentSearch = document.getElementById('youtubeSearchInput').value;
          document.getElementById('youtubeSearchInput').value = currentSearch + ' ' + modifier;
        }}
      </script>
      
      <style>
        .quick-search-btn {{
          padding: 8px 16px;
          background: #303947;
          color: #e8eef5;
          border: 1px solid #667eea;
          border-radius: 6px;
          cursor: pointer;
          font-size: 12px;
          transition: all 0.2s;
        }}
        .quick-search-btn:hover {{
          background: #667eea;
          transform: translateY(-1px);
        }}
      </style>
    </div>'''

def add_youtube_to_sop(filepath):
    """Add YouTube search bar before </body> if not already present."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already has YouTube search
        if 'searchYouTube' in content or 'Search YouTube Tutorials' in content:
            return False
        
        # Extract task name from filename or title
        filename = os.path.basename(filepath)
        task_match = re.search(r'<title>([^<]+)</title>', content)
        if task_match:
            task_name = task_match.group(1).replace(' - SOP', '').strip()
        else:
            # Use filename as fallback
            task_name = filename.replace('.html', '').replace('-', ' ')
        
        # Create search term
        search_term = f"{task_name} tutorial"
        
        # Generate YouTube HTML
        youtube_html = get_youtube_search_html(search_term)
        
        # Insert before </body>
        content = content.replace('</body>', youtube_html + '\n</body>')
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    sops_dir = Path(__file__).parent.parent / "docs" / "sops"
    
    if not os.path.exists(sops_dir):
        print(f"Error: SOPs directory not found at {sops_dir}")
        return
    
    # Process ALL HTML files
    files = sorted(sops_dir.glob("*.html"))
    print(f"🎥 Processing {len(files)} SOP files...")
    
    updated_count = 0
    for filepath in files:
        if add_youtube_to_sop(filepath):
            updated_count += 1
            print(f"  ✅ {filepath.name}")
    
    print(f"\n🎉 Successfully added YouTube search to {updated_count} SOPs!")
    print(f"📊 Total SOPs: {len(files)}")

if __name__ == '__main__':
    main()

