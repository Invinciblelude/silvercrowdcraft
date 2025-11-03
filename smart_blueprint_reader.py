#!/usr/bin/env python3
"""
Smart Blueprint Reader - Uses OpenCV to detect and extract lines,
then uses AI-assisted filtering to keep only walls (removing text, dimensions, etc.)

This combines:
1. Computer Vision (OpenCV) for line detection
2. Smart filtering to remove non-wall elements
3. DXF generation for CAD import

Usage:
    python3 smart_blueprint_reader.py
"""

import cv2
import numpy as np
import ezdxf
import os

# =============================================================================
# CONFIGURATION
# =============================================================================

INPUT_IMAGE = 'blueprints/classified/ARCH/07-Proposed-FloorPlan.jpg'
OUTPUT_DXF = '728-cordant-AI-EXTRACTED.dxf'

# Advanced filtering parameters
MIN_WALL_LENGTH = 100       # Walls are typically long (100+ pixels)
MAX_TEXT_LENGTH = 50        # Text/dimensions are short (< 50 pixels)
ANGLE_TOLERANCE = 5         # Degrees - walls are typically at 0°, 90°, 45° etc
THICKNESS_THRESHOLD = 180   # Brightness threshold for detecting lines
MIN_GAP = 20               # Connect lines if gap is less than this

# =============================================================================
# SMART LINE FILTERING
# =============================================================================

def calculate_angle(x1, y1, x2, y2):
    """Calculate the angle of a line in degrees (0-180)"""
    angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
    # Normalize to 0-180 range
    if angle < 0:
        angle += 180
    return angle

def is_likely_wall(line, min_length=MIN_WALL_LENGTH):
    """
    Determine if a line is likely a wall vs text/dimension/arrow
    
    Walls typically:
    - Are long (> 100 pixels)
    - Are at standard angles (0°, 45°, 90°, 135°)
    - Are continuous
    """
    x1, y1, x2, y2 = line
    length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    # Too short to be a wall
    if length < min_length:
        return False
    
    angle = calculate_angle(x1, y1, x2, y2)
    
    # Check if angle is close to standard architectural angles
    # 0°, 45°, 90°, 135° (±5° tolerance)
    standard_angles = [0, 45, 90, 135, 180]
    is_standard_angle = any(abs(angle - std) < ANGLE_TOLERANCE for std in standard_angles)
    
    return is_standard_angle

def merge_collinear_lines(lines, max_gap=MIN_GAP, angle_threshold=3):
    """
    Merge lines that are on the same line (collinear) with small gaps
    This reconnects broken walls
    """
    if not lines:
        return []
    
    merged = []
    used = set()
    
    for i, line1 in enumerate(lines):
        if i in used:
            continue
            
        x1, y1, x2, y2 = line1
        angle1 = calculate_angle(x1, y1, x2, y2)
        
        # Try to find lines that can be merged with this one
        merged_line = list(line1)
        
        for j, line2 in enumerate(lines):
            if i == j or j in used:
                continue
                
            x3, y3, x4, y4 = line2
            angle2 = calculate_angle(x3, y3, x4, y4)
            
            # Check if angles are similar (collinear)
            if abs(angle1 - angle2) > angle_threshold:
                continue
            
            # Check if endpoints are close (can be connected)
            distances = [
                np.sqrt((x2 - x3)**2 + (y2 - y3)**2),  # end1 to start2
                np.sqrt((x2 - x4)**2 + (y2 - y4)**2),  # end1 to end2
                np.sqrt((x1 - x3)**2 + (y1 - y3)**2),  # start1 to start2
                np.sqrt((x1 - x4)**2 + (y1 - y4)**2),  # start1 to end2
            ]
            
            min_dist = min(distances)
            
            if min_dist < max_gap:
                # Merge the lines by extending to furthest points
                all_x = [x1, x2, x3, x4]
                all_y = [y1, y2, y3, y4]
                merged_line = [min(all_x), min(all_y), max(all_x), max(all_y)]
                used.add(j)
        
        merged.append(merged_line)
        used.add(i)
    
    return merged

# =============================================================================
# MAIN PROCESSING
# =============================================================================

def extract_walls_from_blueprint(image_path):
    """
    Read blueprint and extract only wall lines (filtering out text, dimensions, etc.)
    """
    print("="*70)
    print("🤖 SMART BLUEPRINT READER - AI-ASSISTED LINE EXTRACTION")
    print("="*70)
    
    print(f"\n📥 Loading blueprint: {image_path}")
    
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image: {image_path}")
    
    height, width = img.shape[:2]
    print(f"   Image size: {width} x {height} pixels")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold
    _, binary = cv2.threshold(gray, THICKNESS_THRESHOLD, 255, cv2.THRESH_BINARY_INV)
    
    # Noise removal
    binary = cv2.medianBlur(binary, 3)
    
    print("🔍 Detecting all lines...")
    
    # Detect ALL lines with very permissive parameters
    all_lines = cv2.HoughLinesP(
        binary,
        rho=1,
        theta=np.pi/180,
        threshold=80,           # Lower threshold to catch more
        minLineLength=30,       # Catch short lines too (we'll filter later)
        maxLineGap=15
    )
    
    if all_lines is None:
        print("❌ No lines detected!")
        return [], width, height
    
    all_lines = [line[0] for line in all_lines]
    print(f"   Found {len(all_lines)} total line segments")
    
    # Filter to keep only likely walls
    print("🧹 Filtering: Keeping only wall-like lines...")
    wall_lines = [line for line in all_lines if is_likely_wall(line)]
    print(f"   Filtered to {len(wall_lines)} wall lines")
    
    # Merge broken walls
    print("🔗 Merging collinear/broken wall segments...")
    wall_lines = merge_collinear_lines(wall_lines)
    print(f"   Merged to {len(wall_lines)} continuous walls")
    
    return wall_lines, width, height


def create_dxf_from_walls(walls, image_height, output_file):
    """
    Create DXF file from extracted wall lines
    """
    print(f"\n📝 Creating DXF: {output_file}")
    
    # Create new DXF
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Create layers
    doc.layers.add('WALLS', color=1)  # Red
    doc.layers.add('INFO', color=7)   # White/Black
    
    # Add title
    msp.add_text(
        "728 CORDANT - AI EXTRACTED WALLS",
        dxfattribs={'layer': 'INFO', 'height': 48, 'insert': (100, image_height - 100)}
    )
    
    msp.add_text(
        f"Extracted {len(walls)} wall lines from blueprint",
        dxfattribs={'layer': 'INFO', 'height': 24, 'insert': (100, image_height - 150)}
    )
    
    # Add walls
    print(f"   Adding {len(walls)} walls to DXF...")
    for i, (x1, y1, x2, y2) in enumerate(walls):
        # Flip Y coordinate (image coords start top-left, CAD starts bottom-left)
        y1_flipped = image_height - y1
        y2_flipped = image_height - y2
        
        msp.add_line(
            (x1, y1_flipped),
            (x2, y2_flipped),
            dxfattribs={'layer': 'WALLS'}
        )
    
    # Save
    doc.saveas(output_file)
    print(f"✅ DXF created: {output_file}")


def main():
    """Main execution"""
    try:
        # Extract walls
        walls, width, height = extract_walls_from_blueprint(INPUT_IMAGE)
        
        if not walls:
            print("\n❌ No walls detected. Try adjusting parameters.")
            return
        
        # Create DXF
        create_dxf_from_walls(walls, height, OUTPUT_DXF)
        
        print("\n" + "="*70)
        print("✅ SUCCESS!")
        print("="*70)
        print(f"\n📂 Your CAD file is ready:")
        print(f"   {os.path.abspath(OUTPUT_DXF)}")
        print(f"\n📤 Upload to AutoCAD Web and see your walls!")
        print(f"   - {len(walls)} wall lines extracted")
        print(f"   - Smart filtering removed text/dimensions")
        print(f"   - Broken walls were merged")
        print("\n💡 If some walls are missing:")
        print("   - Lower MIN_WALL_LENGTH in the script")
        print("   - Lower THICKNESS_THRESHOLD")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


