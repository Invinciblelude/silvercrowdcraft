#!/usr/bin/env python3
"""
Blueprint to CAD Converter
Converts blueprint images (JPG/PNG) to DXF CAD files

Usage:
    python3 blueprint_to_cad.py

Requirements:
    pip3 install opencv-python numpy ezdxf
"""

import cv2
import numpy as np
import ezdxf
import os

# =============================================================================
# CONFIGURATION - ADJUST THESE FOR YOUR BLUEPRINT
# =============================================================================

INPUT_IMAGE = 'blueprints/classified/ARCH/07-Proposed-FloorPlan.jpg'
OUTPUT_DXF = '728-cordant-CONVERTED.dxf'

# Hough Transform Parameters (TUNE THESE!)
THRESHOLD = 100          # Lower = more lines detected (80-150 recommended)
MIN_LINE_LENGTH = 50     # Minimum line length in pixels (50-100 recommended)
MAX_LINE_GAP = 10        # Max gap to connect lines (10-20 recommended)

# Pre-processing
BINARY_THRESHOLD = 180   # 0-255, adjust if lines are too thick/thin (150-200 recommended)
BLUR_SIZE = 3           # Noise reduction (3 or 5, must be odd number)

# Output options
SHOW_PREVIEW = True      # Set to False to skip visual preview
SCALE_FACTOR = 1.0       # Scale the output (1.0 = original size)

# =============================================================================
# FUNCTIONS
# =============================================================================

def preprocess_image(image_path):
    """
    Load and prepare the blueprint image for line detection.
    Returns a clean black/white image.
    """
    print(f"📥 Loading image: {image_path}")
    
    # Check if file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ Image not found: {image_path}")
    
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"❌ Could not read image: {image_path}")
    
    print(f"   Image size: {img.shape[1]} x {img.shape[0]} pixels")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to get pure black/white
    # THRESH_BINARY_INV inverts it (dark lines on light background become white on black)
    _, binary = cv2.threshold(gray, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY_INV)
    
    # Remove noise with median blur
    binary = cv2.medianBlur(binary, BLUR_SIZE)
    
    print("✅ Image preprocessed successfully")
    return img, binary


def detect_lines(binary_image):
    """
    Use Hough Line Transform to detect straight lines in the image.
    Returns list of line segments as [(x1, y1, x2, y2), ...]
    """
    print("🔍 Detecting lines...")
    
    # Detect lines using Probabilistic Hough Transform
    lines = cv2.HoughLinesP(
        binary_image,
        rho=1,                      # Distance resolution (1 pixel)
        theta=np.pi/180,            # Angular resolution (1 degree)
        threshold=THRESHOLD,        # Min votes needed
        minLineLength=MIN_LINE_LENGTH,  # Min length
        maxLineGap=MAX_LINE_GAP     # Max gap to bridge
    )
    
    if lines is None:
        print("⚠️  No lines detected! Try lowering THRESHOLD")
        return []
    
    # Convert from numpy array to simple list
    line_list = [line[0] for line in lines]
    
    print(f"✅ Found {len(line_list)} line segments")
    return line_list


def preview_lines(original_image, lines):
    """
    Display the detected lines overlaid on the original image.
    Press any key to close the preview.
    """
    if not SHOW_PREVIEW:
        return
    
    print("👁️  Showing preview... (press any key to continue)")
    
    # Create a copy to draw on
    preview = original_image.copy()
    
    # Draw all detected lines in red
    for x1, y1, x2, y2 in lines:
        cv2.line(preview, (x1, y1), (x2, y2), (0, 0, 255), 2)
    
    # Resize if too large for screen
    height, width = preview.shape[:2]
    if width > 1920 or height > 1080:
        scale = min(1920/width, 1080/height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        preview = cv2.resize(preview, (new_width, new_height))
    
    # Show the window
    cv2.imshow('Detected Lines (Red) - Press any key to continue', preview)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def create_dxf(lines, output_path, image_height):
    """
    Create a DXF CAD file from the detected lines.
    """
    print(f"📝 Creating DXF file: {output_path}")
    
    # Create new DXF document
    doc = ezdxf.new('R2010')  # AutoCAD 2010 format (widely compatible)
    msp = doc.modelspace()
    
    # Create layers for organization
    doc.layers.add('DETECTED-LINES', color=7)  # White/black
    
    # Add each line to the DXF
    for x1, y1, x2, y2 in lines:
        # Flip Y coordinate (image coordinates start top-left, CAD starts bottom-left)
        y1_flipped = image_height - y1
        y2_flipped = image_height - y2
        
        # Apply scale factor
        x1_scaled = x1 * SCALE_FACTOR
        y1_scaled = y1_flipped * SCALE_FACTOR
        x2_scaled = x2 * SCALE_FACTOR
        y2_scaled = y2_flipped * SCALE_FACTOR
        
        # Add line to DXF
        msp.add_line(
            (x1_scaled, y1_scaled),
            (x2_scaled, y2_scaled),
            dxfattribs={'layer': 'DETECTED-LINES'}
        )
    
    # Save the DXF file
    doc.saveas(output_path)
    print(f"✅ DXF file created successfully!")
    print(f"   Location: {os.path.abspath(output_path)}")


def print_tuning_guide():
    """Print instructions for tuning the parameters."""
    print("\n" + "="*70)
    print("🎯 TUNING GUIDE")
    print("="*70)
    print("If results aren't perfect, adjust these parameters at the top of the script:\n")
    print(f"Current settings:")
    print(f"  THRESHOLD = {THRESHOLD}          (Lower = more lines detected)")
    print(f"  MIN_LINE_LENGTH = {MIN_LINE_LENGTH}     (Higher = only longer lines)")
    print(f"  MAX_LINE_GAP = {MAX_LINE_GAP}        (Higher = connects broken lines)")
    print(f"  BINARY_THRESHOLD = {BINARY_THRESHOLD}  (Adjust if lines too thick/thin)")
    print("\nCommon issues:")
    print("  • Missing lines? → Decrease THRESHOLD")
    print("  • Too many tiny lines? → Increase MIN_LINE_LENGTH")
    print("  • Broken lines? → Increase MAX_LINE_GAP")
    print("  • Lines too thick? → Increase BINARY_THRESHOLD")
    print("  • Lines too thin? → Decrease BINARY_THRESHOLD")
    print("="*70 + "\n")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    print("\n" + "="*70)
    print("🏗️  BLUEPRINT TO CAD CONVERTER")
    print("="*70 + "\n")
    
    try:
        # Step 1: Load and preprocess image
        original_img, binary_img = preprocess_image(INPUT_IMAGE)
        image_height = original_img.shape[0]
        
        # Step 2: Detect lines
        detected_lines = detect_lines(binary_img)
        
        if not detected_lines:
            print("\n❌ No lines detected. Check tuning guide below.")
            print_tuning_guide()
            return
        
        # Step 3: Preview (optional)
        preview_lines(original_img, detected_lines)
        
        # Step 4: Create DXF file
        create_dxf(detected_lines, OUTPUT_DXF, image_height)
        
        print("\n" + "="*70)
        print("✅ SUCCESS! Your DXF file is ready.")
        print("="*70)
        print(f"\n📂 Next steps:")
        print(f"   1. Open {OUTPUT_DXF} in AutoCAD Web (upload it)")
        print(f"   2. The detected lines will appear as white/black lines")
        print(f"   3. You can now trace over them or clean them up")
        print("\n💡 If the results aren't perfect, see tuning guide below:\n")
        print_tuning_guide()
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure the image file exists at the specified path")
        print("  2. Install required libraries: pip3 install opencv-python numpy ezdxf")
        print("  3. Check that Python 3 is installed: python3 --version")


if __name__ == "__main__":
    main()


