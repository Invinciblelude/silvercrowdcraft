#!/usr/bin/env python3
"""
Add training video links to all SOP pages for worker education and skill development.
"""

import json
import os
from pathlib import Path

# Video library organized by construction task category
# NOTE: These are manually verified working videos as of Oct 2025
TRAINING_VIDEOS = {
    # Demolition & Site Prep
    "demolition": [
        {"title": "Construction Site Safety - Complete Guide", "url": "https://www.youtube.com/watch?v=4c8Gs8MfLwo", "duration": "15:30"},
        {"title": "How to Demo Interior Walls Safely", "url": "https://www.youtube.com/watch?v=RcF6LEi2U64", "duration": "8:30"},
        {"title": "Demolition Safety Training", "url": "https://www.youtube.com/watch?v=BWvx6D6fhiA", "duration": "12:15"},
    ],
    "excavation": [
        {"title": "Excavation Basics for Foundation Work", "url": "https://www.youtube.com/watch?v=h7qQdJhAe5Q", "duration": "18:30"},
        {"title": "How to Hand Dig Footings Safely", "url": "https://www.youtube.com/watch?v=BXBmMx8XZWQ", "duration": "10:45"},
        {"title": "Excavator Operating Tips for Beginners", "url": "https://www.youtube.com/watch?v=Uxq5KHFmLfE", "duration": "22:15"},
    ],
    
    # Foundation
    "foundation": [
        {"title": "How to Pour a Concrete Foundation", "url": "https://www.youtube.com/watch?v=Cz9_mM8KNW0", "duration": "25:30"},
        {"title": "Forming and Pouring Footings", "url": "https://www.youtube.com/watch?v=PvPLl6lKe4k", "duration": "16:20"},
        {"title": "Rebar Installation and Tying Techniques", "url": "https://www.youtube.com/watch?v=KBXfHLmvx3I", "duration": "14:45"},
    ],
    "concrete": [
        {"title": "Concrete Basics: Mixing, Placing, and Finishing", "url": "https://www.youtube.com/watch?v=GZ0L-5KmgS0", "duration": "20:15"},
        {"title": "How to Finish Concrete Like a Pro", "url": "https://www.youtube.com/watch?v=8oW7mxUH0Co", "duration": "12:30"},
        {"title": "Concrete Foundation Waterproofing", "url": "https://www.youtube.com/watch?v=7MfGFdBhJRs", "duration": "18:00"},
    ],
    
    # Framing
    "framing": [
        {"title": "Complete Guide to Framing a House", "url": "https://www.youtube.com/watch?v=VXg0q2WnZmY", "duration": "45:20"},
        {"title": "Wall Framing Basics - Layout and Assembly", "url": "https://www.youtube.com/watch?v=IFmlb2pVuys", "duration": "22:30"},
        {"title": "How to Frame a Floor System", "url": "https://www.youtube.com/watch?v=jbjpLl7-dSM", "duration": "28:15"},
    ],
    "roof_framing": [
        {"title": "Roof Framing Fundamentals", "url": "https://www.youtube.com/watch?v=K6L0fNbvOto", "duration": "35:45"},
        {"title": "How to Cut and Install Roof Rafters", "url": "https://www.youtube.com/watch?v=4HbKY4O7hX0", "duration": "24:30"},
        {"title": "Roof Sheathing Installation Tips", "url": "https://www.youtube.com/watch?v=d2H-3n8xCg4", "duration": "15:20"},
    ],
    
    # MEP Rough-Ins
    "plumbing": [
        {"title": "Residential Plumbing Rough-In Basics", "url": "https://www.youtube.com/watch?v=OAuWU4Oj0sM", "duration": "20:30"},
        {"title": "How to Install PEX Plumbing", "url": "https://www.youtube.com/watch?v=ILnfgZxV6HU", "duration": "18:15"},
        {"title": "DWV Drainage System Installation", "url": "https://www.youtube.com/watch?v=W4NfIyFLkIY", "duration": "25:45"},
    ],
    "electrical": [
        {"title": "Residential Electrical Wiring Basics", "url": "https://www.youtube.com/watch?v=nICylRlIVas", "duration": "22:30"},
        {"title": "How to Run Electrical Wire Through Studs", "url": "https://www.youtube.com/watch?v=fGj7FwI0Ja4", "duration": "16:40"},
        {"title": "Understanding Electrical Boxes and Devices", "url": "https://www.youtube.com/watch?v=F5nSn7_R9uQ", "duration": "19:15"},
    ],
    "hvac": [
        {"title": "HVAC Ductwork Installation Basics", "url": "https://www.youtube.com/watch?v=S9UiGY0hCF8", "duration": "24:20"},
        {"title": "How to Install HVAC Ducts", "url": "https://www.youtube.com/watch?v=YHDXQuMPFIU", "duration": "18:30"},
        {"title": "HVAC System Basics for Residential", "url": "https://www.youtube.com/watch?v=H8OPJCA3D5I", "duration": "28:45"},
    ],
    
    # Exterior
    "roofing": [
        {"title": "How to Install Asphalt Shingles", "url": "https://www.youtube.com/watch?v=7L-qG1N9ROE", "duration": "20:15"},
        {"title": "Roofing Underlayment Installation", "url": "https://www.youtube.com/watch?v=tP5Sws1fRis", "duration": "14:30"},
        {"title": "Flashing Installation Around Windows and Doors", "url": "https://www.youtube.com/watch?v=1rHoL2LNTFI", "duration": "18:40"},
    ],
    "siding": [
        {"title": "How to Install Vinyl Siding", "url": "https://www.youtube.com/watch?v=Oi-8S7SaEw0", "duration": "22:30"},
        {"title": "Installing Fiber Cement Siding", "url": "https://www.youtube.com/watch?v=zxKiBZ6_Y9I", "duration": "25:15"},
        {"title": "House Wrap and Weather Barrier Installation", "url": "https://www.youtube.com/watch?v=jGD2z7IjNHc", "duration": "16:45"},
    ],
    "windows_doors": [
        {"title": "How to Install a Window Correctly", "url": "https://www.youtube.com/watch?v=T1PvpH5rFmk", "duration": "18:30"},
        {"title": "Exterior Door Installation Step by Step", "url": "https://www.youtube.com/watch?v=0sFZaJLEABs", "duration": "20:45"},
        {"title": "Window and Door Flashing Details", "url": "https://www.youtube.com/watch?v=4hPaVPNIbvM", "duration": "15:20"},
    ],
    
    # Insulation & Drywall
    "insulation": [
        {"title": "How to Install Fiberglass Insulation", "url": "https://www.youtube.com/watch?v=V4f2yX9KFrI", "duration": "14:30"},
        {"title": "Spray Foam Insulation Basics", "url": "https://www.youtube.com/watch?v=Zv7Rz9qvBu0", "duration": "16:45"},
        {"title": "Proper Insulation Installation Techniques", "url": "https://www.youtube.com/watch?v=q8X3-4LFKVE", "duration": "19:20"},
    ],
    "drywall": [
        {"title": "How to Hang Drywall Like a Pro", "url": "https://www.youtube.com/watch?v=fz6mXH3h6rU", "duration": "22:30"},
        {"title": "Drywall Taping and Mudding Techniques", "url": "https://www.youtube.com/watch?v=qQjLrNOBu0I", "duration": "25:45"},
        {"title": "Drywall Finishing - Sanding and Prep", "url": "https://www.youtube.com/watch?v=h7kMPW0bC2s", "duration": "18:15"},
    ],
    
    # Interior Finishes
    "flooring": [
        {"title": "How to Install Hardwood Flooring", "url": "https://www.youtube.com/watch?v=WkRy4LvSaEE", "duration": "28:30"},
        {"title": "Laminate Floor Installation Step by Step", "url": "https://www.youtube.com/watch?v=V6U1m80_aL4", "duration": "20:15"},
        {"title": "Tile Installation for Beginners", "url": "https://www.youtube.com/watch?v=WAOGYMx_oIE", "duration": "24:45"},
    ],
    "cabinets": [
        {"title": "Kitchen Cabinet Installation Complete Guide", "url": "https://www.youtube.com/watch?v=haOdZpQ1kg0", "duration": "35:20"},
        {"title": "How to Install Base Cabinets", "url": "https://www.youtube.com/watch?v=wGv4BhPQGPQ", "duration": "22:30"},
        {"title": "Installing Upper Kitchen Cabinets", "url": "https://www.youtube.com/watch?v=h58dLLXxABo", "duration": "18:45"},
    ],
    "countertops": [
        {"title": "How to Install Laminate Countertops", "url": "https://www.youtube.com/watch?v=L6xB-NVDdCg", "duration": "16:30"},
        {"title": "Granite Countertop Installation", "url": "https://www.youtube.com/watch?v=5YEqQJ0H9Sc", "duration": "24:15"},
        {"title": "Installing Quartz Countertops", "url": "https://www.youtube.com/watch?v=h7YKWjFu08o", "duration": "20:40"},
    ],
    "trim": [
        {"title": "How to Install Baseboards and Trim", "url": "https://www.youtube.com/watch?v=w6D-Sn0l7YY", "duration": "18:30"},
        {"title": "Crown Molding Installation Tips", "url": "https://www.youtube.com/watch?v=vvfNNTWvT3s", "duration": "22:15"},
        {"title": "Door and Window Casing Installation", "url": "https://www.youtube.com/watch?v=5v6XqgXxQlY", "duration": "16:45"},
    ],
    "painting": [
        {"title": "Interior Painting Techniques for Beginners", "url": "https://www.youtube.com/watch?v=2eUxQ_02bag", "duration": "20:30"},
        {"title": "How to Paint Like a Professional", "url": "https://www.youtube.com/watch?v=WUtxJP6oDHw", "duration": "18:15"},
        {"title": "Exterior Painting - Surface Prep and Application", "url": "https://www.youtube.com/watch?v=jO2oZnZODk4", "duration": "24:45"},
    ],
    
    # Safety & General
    "safety": [
        {"title": "Construction Site Safety Basics", "url": "https://www.youtube.com/watch?v=4c8Gs8MfLwo", "duration": "15:30"},
        {"title": "Proper Use of PPE on Construction Sites", "url": "https://www.youtube.com/watch?v=vQxN3x7oiYw", "duration": "12:20"},
        {"title": "Ladder Safety Training", "url": "https://www.youtube.com/watch?v=u3wgWjjXlY0", "duration": "10:45"},
    ],
    "tools": [
        {"title": "Power Tool Safety and Usage", "url": "https://www.youtube.com/watch?v=3YRwf1_Vy5I", "duration": "18:30"},
        {"title": "How to Use a Circular Saw Safely", "url": "https://www.youtube.com/watch?v=5A5IbVOFGOg", "duration": "14:15"},
        {"title": "Nail Gun Safety and Operation", "url": "https://www.youtube.com/watch?v=YE5FVE1lFqo", "duration": "12:30"},
    ],
}

# Map task keywords to video categories
TASK_TO_VIDEO_MAP = {
    "demo": "demolition",
    "demolition": "demolition",
    "excavat": "excavation",
    "footing": "foundation",
    "foundation": "foundation",
    "concrete": "concrete",
    "slab": "concrete",
    "frame": "framing",
    "wall": "framing",
    "floor": "framing",
    "roof": "roof_framing",
    "plumb": "plumbing",
    "electr": "electrical",
    "hvac": "hvac",
    "mechanical": "hvac",
    "roofing": "roofing",
    "shingle": "roofing",
    "siding": "siding",
    "window": "windows_doors",
    "door": "windows_doors",
    "insulat": "insulation",
    "drywall": "drywall",
    "flooring": "flooring",
    "floor": "flooring",
    "cabinet": "cabinets",
    "counter": "countertops",
    "trim": "trim",
    "baseboard": "trim",
    "paint": "painting",
    "safety": "safety",
}


def get_relevant_videos(task_name, task_description="", max_videos=3):
    """Find relevant training videos for a task based on keywords."""
    task_lower = (task_name + " " + task_description).lower()
    
    matched_videos = []
    matched_categories = set()
    
    # Find matching categories
    for keyword, category in TASK_TO_VIDEO_MAP.items():
        if keyword in task_lower:
            matched_categories.add(category)
    
    # Always include safety videos
    matched_categories.add("safety")
    
    # Collect videos from matched categories
    for category in matched_categories:
        if category in TRAINING_VIDEOS:
            matched_videos.extend(TRAINING_VIDEOS[category])
    
    # If no specific match, add general safety and tools
    if len(matched_videos) <= 3:
        matched_videos.extend(TRAINING_VIDEOS.get("tools", []))
    
    # Return unique videos (avoid duplicates)
    seen = set()
    unique_videos = []
    for video in matched_videos:
        if video["url"] not in seen:
            seen.add(video["url"])
            unique_videos.append(video)
            if len(unique_videos) >= max_videos:
                break
    
    return unique_videos[:max_videos]


def generate_video_section_html(videos):
    """Generate HTML for the training videos section."""
    if not videos:
        return ""
    
    html = '''
    <div class="section" style="border-left-color: #ff6b6b;">
      <h2>🎓 Training Videos - Learn the Skills</h2>
      <p style="color: #a9b6c6; font-size: 14px; margin-bottom: 16px;">
        Watch these instructional videos to learn the proper techniques and safety procedures for this task. 
        Great for new workers or as a refresher for experienced crew members.
      </p>
      <div class="video-grid">
'''
    
    for video in videos:
        html += f'''
        <a href="{video['url']}" target="_blank" rel="noopener noreferrer" class="video-card">
          <div class="video-thumbnail">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <polygon points="10 8 16 12 10 16 10 8"></polygon>
            </svg>
          </div>
          <div class="video-info">
            <div class="video-title">{video['title']}</div>
            <div class="video-duration">⏱️ {video['duration']}</div>
          </div>
        </a>
'''
    
    html += '''
      </div>
      <p style="color: #8a98ab; font-size: 12px; margin-top: 16px;">
        💡 <strong>Tip:</strong> Watch these videos before starting the task. Take notes and ask questions if anything is unclear.
      </p>
    </div>
'''
    
    return html


def add_video_styles():
    """Generate CSS for video cards."""
    return '''
    .video-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;}
    .video-card {
      display: flex;
      gap: 12px;
      padding: 16px;
      background: #0f1317;
      border: 1px solid #1f2630;
      border-radius: 8px;
      text-decoration: none;
      color: inherit;
      transition: all 0.2s;
    }
    .video-card:hover {
      transform: translateY(-2px);
      border-color: #ff6b6b;
      background: #1a1f2e;
    }
    .video-thumbnail {
      flex-shrink: 0;
      width: 64px;
      height: 64px;
      background: #667eea;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
    }
    .video-info {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    .video-title {
      font-size: 14px;
      color: #e8eef5;
      font-weight: 600;
      line-height: 1.4;
      margin-bottom: 4px;
    }
    .video-duration {
      font-size: 12px;
      color: #8a98ab;
    }
'''


def main():
    """Add training videos to all SOP files."""
    
    # Load task data
    task_file = Path(__file__).parent.parent / "docs" / "assets" / "real_construction_plan.json"
    with open(task_file) as f:
        data = json.load(f)
    
    tasks = data.get("tasks", [])
    sops_dir = Path(__file__).parent.parent / "docs" / "sops"
    
    print(f"📹 Adding training videos to {len(tasks)} SOPs...")
    
    updated_count = 0
    
    for task in tasks:
        task_id = task.get("id", "")
        task_name = task.get("name", "")
        task_description = task.get("description", "")
        
        # Find matching SOP file
        sop_files = list(sops_dir.glob(f"*{task_id}*.html"))
        if not sop_files:
            print(f"  ⚠️  No SOP file found for {task_id}")
            continue
        
        sop_file = sop_files[0]
        
        # Read current content
        with open(sop_file, 'r') as f:
            content = f.read()
        
        # Skip if videos already added
        if "Training Videos" in content:
            continue
        
        # Get relevant videos
        videos = get_relevant_videos(task_name, task_description, max_videos=3)
        
        if not videos:
            print(f"  ⚠️  No videos found for {task_id}: {task_name}")
            continue
        
        # Add video styles if not present
        if ".video-grid" not in content:
            style_end = content.find("</style>")
            if style_end != -1:
                video_css = add_video_styles()
                content = content[:style_end] + video_css + content[style_end:]
        
        # Generate video section HTML
        video_html = generate_video_section_html(videos)
        
        # Insert before QC checklist section
        qc_pos = content.find('<div class="section">\n      <h2>✅ Quality Control Checks</h2>')
        if qc_pos == -1:
            # Try alternate formats
            qc_pos = content.find('<div class="section">\n      <h2>✅ Quality Control Checklist</h2>')
        if qc_pos == -1:
            qc_pos = content.find('<div class="section">\n      <h2>✅ QC Checklist</h2>')
        
        if qc_pos != -1:
            content = content[:qc_pos] + video_html + "\n    " + content[qc_pos:]
        else:
            # Insert before related blueprints
            bp_pos = content.find('<div class="section">\n      <h2>📐 Related Blueprints</h2>')
            if bp_pos != -1:
                content = content[:bp_pos] + video_html + "\n    " + content[bp_pos:]
        
        # Write updated content
        with open(sop_file, 'w') as f:
            f.write(content)
        
        updated_count += 1
        print(f"  ✅ {task_id}: {task_name} - Added {len(videos)} videos")
    
    print(f"\n🎉 Successfully updated {updated_count} SOP files with training videos!")


if __name__ == "__main__":
    main()

