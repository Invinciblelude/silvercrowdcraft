#!/usr/bin/env python3
"""
Add an embedded YouTube search bar to all SOP pages.
Workers can search for any construction tutorial directly from the SOP.
"""

import json
from pathlib import Path

def generate_youtube_search_section(task_name):
    """Generate HTML for YouTube search section."""
    
    # Pre-fill with task name but let them modify it
    default_search = task_name.lower()
    
    html = f'''
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
            value="{default_search} tutorial"
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
          <button onclick="quickSearch('for beginners')" class="quick-search-btn">For Beginners</button>
          <button onclick="quickSearch('tips and tricks')" class="quick-search-btn">Tips & Tricks</button>
        </div>
        
        <p style="font-size: 12px; color: #8a98ab; margin-top: 8px;">
          💡 <strong>Tip:</strong> Add terms like "how to", "tutorial", "step by step", or specific tool names for better results.
        </p>
      </div>
      
      <script>
        function searchYouTube() {{
          const searchTerm = document.getElementById('youtubeSearchInput').value;
          const url = 'https://www.youtube.com/results?search_query=' + encodeURIComponent(searchTerm);
          window.open(url, '_blank');
        }}
        
        function quickSearch(modifier) {{
          const input = document.getElementById('youtubeSearchInput');
          const currentValue = input.value.replace(/ (how to|tutorial|step by step|for beginners|tips and tricks)$/i, '');
          input.value = currentValue + ' ' + modifier;
        }}
      </script>
      
      <style>
        .quick-search-btn {{
          padding: 6px 12px;
          background: #303947;
          color: #e8eef5;
          border: 1px solid #667eea;
          border-radius: 4px;
          font-size: 12px;
          cursor: pointer;
          transition: all 0.2s;
        }}
        .quick-search-btn:hover {{
          background: #667eea;
          transform: translateY(-1px);
        }}
      </style>
    </div>
'''
    
    return html


def add_youtube_search_to_sops():
    """Add YouTube search bar to all SOP files."""
    
    # Load task data
    task_file = Path(__file__).parent.parent / "docs" / "assets" / "real_construction_plan.json"
    with open(task_file) as f:
        data = json.load(f)
    
    tasks = data.get("tasks", [])
    sops_dir = Path(__file__).parent.parent / "docs" / "sops"
    
    print(f"🎥 Adding YouTube search bar to {len(tasks)} SOPs...")
    
    updated_count = 0
    
    for task in tasks:
        task_id = task.get("id", "")
        task_name = task.get("name", "")
        
        # Find matching SOP file
        sop_files = list(sops_dir.glob(f"*{task_id}*.html"))
        if not sop_files:
            continue
        
        sop_file = sop_files[0]
        
        # Read current content
        with open(sop_file, 'r') as f:
            content = f.read()
        
        # Skip if search bar already added
        if "youtubeSearchForm" in content:
            continue
        
        # Generate YouTube search section
        search_html = generate_youtube_search_section(task_name)
        
        # Insert after Training Videos section, before QC checklist
        # Look for the end of Training Videos section
        insertion_markers = [
            ('</div>\n    \n    <div class="section">\n      <h2>✅ Quality Control Checks</h2>', 0),
            ('</div>\n    \n    <div class="section">\n      <h2>📐 Related Blueprint', 0),
        ]
        
        inserted = False
        for marker, offset in insertion_markers:
            if marker in content:
                pos = content.find(marker) + offset
                content = content[:pos] + "\n    " + search_html + "\n    " + content[pos:]
                inserted = True
                break
        
        if not inserted:
            # Fallback: insert before closing body tag
            pos = content.rfind('</body>')
            if pos != -1:
                content = content[:pos] + search_html + "\n  " + content[pos:]
                inserted = True
        
        if inserted:
            # Write updated content
            with open(sop_file, 'w') as f:
                f.write(content)
            
            updated_count += 1
            print(f"  ✅ {task_id}: {task_name}")
    
    print(f"\n🎉 Successfully added YouTube search to {updated_count} SOP files!")
    print(f"\n💡 Workers can now:")
    print(f"   - Search YouTube directly from any SOP")
    print(f"   - Modify search terms as needed")
    print(f"   - Use quick search modifiers")
    print(f"   - Find the exact tutorials they need!")


if __name__ == "__main__":
    add_youtube_search_to_sops()

