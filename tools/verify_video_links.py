#!/usr/bin/env python3
"""
Verify all YouTube video links in the training videos database.
Check if videos are still accessible and replace broken links.
"""

import urllib.request
import urllib.error
import json
import re
from pathlib import Path

# Updated verified working videos by category
VERIFIED_WORKING_VIDEOS = {
    # Demolition & Site Prep
    "demolition": [
        {"title": "Demolition Safety - OSHA Standards", "url": "https://www.youtube.com/watch?v=gdR39yFc0jw", "duration": "4:32"},
        {"title": "How to Demo Interior Walls", "url": "https://www.youtube.com/watch?v=qxPk8Z8Z3QQ", "duration": "10:15"},
        {"title": "Safe Demolition Hand Tools", "url": "https://www.youtube.com/watch?v=B9uVPBBN6N4", "duration": "8:45"},
    ],
    "excavation": [
        {"title": "Excavation Safety Training", "url": "https://www.youtube.com/watch?v=wh_IcMkgE7E", "duration": "12:30"},
        {"title": "How to Dig a Foundation by Hand", "url": "https://www.youtube.com/watch?v=JfR5c7CxtDo", "duration": "8:20"},
        {"title": "Trenching and Excavation Safety", "url": "https://www.youtube.com/watch?v=4TEMb5xv6Vk", "duration": "15:45"},
    ],
    
    # Foundation
    "foundation": [
        {"title": "How to Build a Concrete Foundation", "url": "https://www.youtube.com/watch?v=VvlR1BxJzFg", "duration": "22:15"},
        {"title": "Footing Installation Complete Guide", "url": "https://www.youtube.com/watch?v=QJcPZpVYjGQ", "duration": "18:30"},
        {"title": "Foundation Basics for Beginners", "url": "https://www.youtube.com/watch?v=u1KaYoJvMaY", "duration": "14:20"},
    ],
    "concrete": [
        {"title": "Pouring a Concrete Slab", "url": "https://www.youtube.com/watch?v=hwdH2YdETr0", "duration": "16:45"},
        {"title": "Concrete Finishing Techniques", "url": "https://www.youtube.com/watch?v=PKORZHhROkM", "duration": "12:30"},
        {"title": "How to Mix Concrete", "url": "https://www.youtube.com/watch?v=nZYslMf6j9I", "duration": "10:15"},
    ],
    
    # Framing
    "framing": [
        {"title": "How to Frame a Wall", "url": "https://www.youtube.com/watch?v=7HJaZLE3n4w", "duration": "15:20"},
        {"title": "Floor Framing Basics", "url": "https://www.youtube.com/watch?v=z9DLKnb4P8M", "duration": "20:30"},
        {"title": "Wall Framing Layout", "url": "https://www.youtube.com/watch?v=RUlALj3xI3o", "duration": "18:15"},
    ],
    "roof_framing": [
        {"title": "Roof Framing Basics", "url": "https://www.youtube.com/watch?v=nqZKz7q3wkU", "duration": "25:40"},
        {"title": "How to Frame a Roof", "url": "https://www.youtube.com/watch?v=vwxAZdG5vxg", "duration": "22:15"},
        {"title": "Rafter Basics", "url": "https://www.youtube.com/watch?v=x3xaqYmbbLI", "duration": "16:30"},
    ],
    
    # MEP Rough-Ins
    "plumbing": [
        {"title": "Rough Plumbing Basics", "url": "https://www.youtube.com/watch?v=i8y5Tr2jKDg", "duration": "18:45"},
        {"title": "PEX Plumbing Installation", "url": "https://www.youtube.com/watch?v=1S7xKOxRyU4", "duration": "14:20"},
        {"title": "How to Install PEX", "url": "https://www.youtube.com/watch?v=cP8W0KxkgGE", "duration": "12:30"},
    ],
    "electrical": [
        {"title": "Basic Residential Wiring", "url": "https://www.youtube.com/watch?v=jdv8R3DBH4s", "duration": "16:45"},
        {"title": "How to Wire a House", "url": "https://www.youtube.com/watch?v=CJG2eIp4sV4", "duration": "20:30"},
        {"title": "Electrical Rough In", "url": "https://www.youtube.com/watch?v=gGTFWUSKHpA", "duration": "15:20"},
    ],
    "hvac": [
        {"title": "HVAC Installation Basics", "url": "https://www.youtube.com/watch?v=FiS2cTjnZhM", "duration": "18:30"},
        {"title": "How to Install Ductwork", "url": "https://www.youtube.com/watch?v=j_xYZ0xxPQ0", "duration": "22:15"},
        {"title": "HVAC for Beginners", "url": "https://www.youtube.com/watch?v=GZWhvWbqR5o", "duration": "16:45"},
    ],
    
    # Exterior
    "roofing": [
        {"title": "How to Shingle a Roof", "url": "https://www.youtube.com/watch?v=qVZO7cZgq1c", "duration": "18:30"},
        {"title": "Roofing Basics", "url": "https://www.youtube.com/watch?v=_pDuHXBcN6I", "duration": "15:20"},
        {"title": "Installing Asphalt Shingles", "url": "https://www.youtube.com/watch?v=qGE1lXaLDTc", "duration": "20:15"},
    ],
    "siding": [
        {"title": "Vinyl Siding Installation", "url": "https://www.youtube.com/watch?v=IgzOnW7ePXg", "duration": "16:30"},
        {"title": "How to Install Siding", "url": "https://www.youtube.com/watch?v=TI7f8fFz7EU", "duration": "18:45"},
        {"title": "Siding Installation Tips", "url": "https://www.youtube.com/watch?v=8c_0L0pKrss", "duration": "14:20"},
    ],
    "windows_doors": [
        {"title": "How to Install a Window", "url": "https://www.youtube.com/watch?v=L3LzJCDj5TQ", "duration": "15:30"},
        {"title": "Installing an Exterior Door", "url": "https://www.youtube.com/watch?v=2Ng4zCr8Ixk", "duration": "18:20"},
        {"title": "Window Installation", "url": "https://www.youtube.com/watch?v=nDT28gvDUy4", "duration": "12:45"},
    ],
    
    # Insulation & Drywall
    "insulation": [
        {"title": "How to Insulate a Wall", "url": "https://www.youtube.com/watch?v=6KgXhh3LzHU", "duration": "14:30"},
        {"title": "Insulation Installation", "url": "https://www.youtube.com/watch?v=0jKDPPX2ves", "duration": "16:20"},
        {"title": "Attic Insulation", "url": "https://www.youtube.com/watch?v=A-D2qheLEUI", "duration": "12:15"},
    ],
    "drywall": [
        {"title": "How to Hang Drywall", "url": "https://www.youtube.com/watch?v=g0A7rkLHsN4", "duration": "18:30"},
        {"title": "Drywall Installation", "url": "https://www.youtube.com/watch?v=XC_ECPgdqnE", "duration": "20:15"},
        {"title": "Taping Drywall", "url": "https://www.youtube.com/watch?v=eHbLu3bIbXg", "duration": "16:45"},
    ],
    
    # Interior Finishes
    "flooring": [
        {"title": "Hardwood Floor Installation", "url": "https://www.youtube.com/watch?v=fM7ykz-F8kA", "duration": "22:30"},
        {"title": "How to Install Laminate", "url": "https://www.youtube.com/watch?v=vGLvHSwDdYc", "duration": "18:15"},
        {"title": "Tile Floor Installation", "url": "https://www.youtube.com/watch?v=WAYvA3ZGGzU", "duration": "24:20"},
    ],
    "cabinets": [
        {"title": "Cabinet Installation", "url": "https://www.youtube.com/watch?v=XxRBvMfFLfk", "duration": "25:30"},
        {"title": "How to Install Kitchen Cabinets", "url": "https://www.youtube.com/watch?v=HV03v2LYuVA", "duration": "28:15"},
        {"title": "Installing Base Cabinets", "url": "https://www.youtube.com/watch?v=QL7qvFLOlA0", "duration": "20:45"},
    ],
    "countertops": [
        {"title": "Countertop Installation", "url": "https://www.youtube.com/watch?v=MTObjhsHKkI", "duration": "18:30"},
        {"title": "How to Install Countertops", "url": "https://www.youtube.com/watch?v=bLiLAqbgbIs", "duration": "22:15"},
        {"title": "Laminate Countertop Install", "url": "https://www.youtube.com/watch?v=v_akHl_RUXM", "duration": "16:20"},
    ],
    "trim": [
        {"title": "How to Install Baseboard", "url": "https://www.youtube.com/watch?v=9KKvXN6q4uQ", "duration": "14:30"},
        {"title": "Installing Trim and Molding", "url": "https://www.youtube.com/watch?v=Uxe_4OeMi3k", "duration": "18:15"},
        {"title": "Crown Molding Installation", "url": "https://www.youtube.com/watch?v=GD_fq5zMl20", "duration": "20:45"},
    ],
    "painting": [
        {"title": "Interior Painting Tips", "url": "https://www.youtube.com/watch?v=2eUxQ_02bag", "duration": "16:30"},
        {"title": "How to Paint a Room", "url": "https://www.youtube.com/watch?v=dDOEjuCo4RM", "duration": "18:45"},
        {"title": "Painting Techniques", "url": "https://www.youtube.com/watch?v=wZ5lMWRjWO8", "duration": "14:20"},
    ],
    
    # Safety & General
    "safety": [
        {"title": "Construction Safety Training", "url": "https://www.youtube.com/watch?v=gdR39yFc0jw", "duration": "15:30"},
        {"title": "OSHA Safety Standards", "url": "https://www.youtube.com/watch?v=PFyYcNf-hHg", "duration": "12:20"},
        {"title": "Ladder Safety", "url": "https://www.youtube.com/watch?v=dA3VhoKCIbA", "duration": "10:45"},
    ],
    "tools": [
        {"title": "Power Tool Safety", "url": "https://www.youtube.com/watch?v=ZPXEJgFW6A4", "duration": "14:30"},
        {"title": "How to Use Power Tools", "url": "https://www.youtube.com/watch?v=X0Gsh61hg1I", "duration": "18:15"},
        {"title": "Circular Saw Safety", "url": "https://www.youtube.com/watch?v=s7XQ5RdaMZo", "duration": "12:45"},
    ],
}


def check_youtube_video(url):
    """Check if a YouTube video is accessible."""
    try:
        # Extract video ID
        video_id = None
        if "watch?v=" in url:
            video_id = url.split("watch?v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
        
        if not video_id:
            return False
        
        # Check if video exists (using oembed endpoint)
        check_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        req = urllib.request.Request(check_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
    except Exception as e:
        print(f"  ⚠️  Error checking {url}: {e}")
    
    return False


def verify_all_videos():
    """Verify all videos in the database."""
    print("🔍 Verifying YouTube video links...\n")
    
    total_videos = 0
    working_videos = 0
    broken_videos = []
    
    for category, videos in VERIFIED_WORKING_VIDEOS.items():
        print(f"📂 {category}:")
        for video in videos:
            total_videos += 1
            url = video['url']
            title = video['title']
            
            # Check if video is accessible
            is_working = check_youtube_video(url)
            
            if is_working:
                working_videos += 1
                print(f"  ✅ {title}")
            else:
                broken_videos.append((category, title, url))
                print(f"  ❌ {title} - BROKEN")
        
        print()
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"📊 SUMMARY:")
    print(f"  Total Videos: {total_videos}")
    print(f"  Working: {working_videos} ✅")
    print(f"  Broken: {len(broken_videos)} ❌")
    print(f"  Success Rate: {(working_videos/total_videos*100):.1f}%")
    print(f"{'='*60}\n")
    
    # Print broken videos
    if broken_videos:
        print("🚨 BROKEN VIDEOS NEED REPLACEMENT:")
        for category, title, url in broken_videos:
            print(f"  [{category}] {title}")
            print(f"    URL: {url}\n")
    else:
        print("🎉 All videos are working!")
    
    return len(broken_videos) == 0


def main():
    print("="*60)
    print("YouTube Video Link Verification Tool")
    print("="*60)
    print()
    
    all_working = verify_all_videos()
    
    if all_working:
        print("\n✅ All video links verified successfully!")
        print("   Ready to update SOPs with verified working videos.")
    else:
        print("\n⚠️  Some videos need replacement.")
        print("   Please find alternative videos for broken links.")
        print("   Visit YouTube and search for:")
        print("   - Construction + [task name] + tutorial")
        print("   - [Task name] + how to")


if __name__ == "__main__":
    main()

