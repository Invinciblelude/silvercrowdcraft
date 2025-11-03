#!/usr/bin/env python3
"""
Blueprint OCR to CAD Converter
Extracts EXACT data from blueprint images/PDFs using OCR
Then generates DXF files AutoCAD can open and edit
"""

import ezdxf
from ezdxf import colors
import cv2
import numpy as np
from PIL import Image
import pytesseract
import re
from pathlib import Path
import shutil

# Ensure tesseract is resolvable (Homebrew default)
if not shutil.which(getattr(pytesseract.pytesseract, 'tesseract_cmd', 'tesseract')):
    pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# Configure paths
BLUEPRINT_DIR = Path("blueprints/classified")
OUTPUT_DIR = Path("cad_outputs")

def extract_text_from_blueprint(image_path):
    """Use OCR to extract ALL text from blueprint image"""
    print(f"📄 Extracting text from: {image_path.name}")
    
    # Load image
    img = cv2.imread(str(image_path))
    if img is None:
        return []
    
    # Preprocess for OCR
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Enhance contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    # OCR - get all text with positions
    data = pytesseract.image_to_data(enhanced, output_type=pytesseract.Output.DICT)
    
    # Extract text with coordinates
    extracted = []
    n_boxes = len(data['text'])
    for i in range(n_boxes):
        text = data['text'][i].strip()
        if len(text) > 0:
            extracted.append({
                'text': text,
                'x': data['left'][i],
                'y': data['top'][i],
                'width': data['width'][i],
                'height': data['height'][i],
                'conf': data['conf'][i]
            })
    
    return extracted

def parse_dimensions(text_data):
    """Extract dimension strings like '14'-4"', '24'-2"', etc."""
    dimensions = []
    dimension_pattern = r"(\d+)[\s]*'[\s]*(\d+)[\s]*\""
    
    for item in text_data:
        matches = re.findall(dimension_pattern, item['text'])
        for feet, inches in matches:
            dim = {
                'value': f"{feet}'-{inches}\"",
                'inches': int(feet) * 12 + int(inches),
                'text': item['text'],
                'position': (item['x'], item['y'])
            }
            dimensions.append(dim)
    
    return dimensions

def parse_beam_schedule(text_data):
    """Extract beam schedule data (B1, B2, etc.)"""
    beams = {}
    current_beam = None
    
    for item in text_data:
        text = item['text'].strip()
        
        # Look for beam IDs (B1, B2, etc.)
        beam_match = re.match(r'B(\d+)', text)
        if beam_match:
            current_beam = f"B{beam_match.group(1)}"
            beams[current_beam] = {'id': current_beam}
        
        # Look for sizes (like "3-3/4" x 11"", "2x12", etc.)
        if current_beam:
            size_patterns = [
                r'(\d+)[- ](\d+)/(\d+)[\s]*"[\s]*x[\s]*(\d+)[\s]*"',  # 3-3/4" x 11"
                r'\((\d+)\)[\s]*2x(\d+)',  # (4) 2x12
                r'(\d+)[\s]*x[\s]*(\d+)',  # 5-1/8 x 12
            ]
            
            for pattern in size_patterns:
                match = re.search(pattern, text)
                if match:
                    beams[current_beam]['size_text'] = text
                    break
    
    return beams

def parse_window_door_schedule(text_data):
    """Extract window and door schedule"""
    schedule = {
        'windows': [],
        'doors': []
    }
    
    # Look for window/door markers and sizes
    for item in text_data:
        text = item['text'].strip()
        
        # Window patterns
        if re.search(r'window|win|W\d+', text, re.IGNORECASE):
            size_match = re.search(r'(\d+)[\s]*x[\s]*(\d+)', text)
            if size_match:
                schedule['windows'].append({
                    'marker': text,
                    'width': int(size_match.group(1)),
                    'height': int(size_match.group(2))
                })
        
        # Door patterns
        if re.search(r'door|D\d+', text, re.IGNORECASE):
            size_match = re.search(r'(\d+)[\s]*x[\s]*(\d+)', text)
            if size_match:
                schedule['doors'].append({
                    'marker': text,
                    'width': int(size_match.group(1)),
                    'height': int(size_match.group(2))
                })
    
    return schedule

def create_cad_wall(doc, start_point, end_point, wall_type='exterior', height=96):
    """
    Create a wall in CAD with exact specifications
    Returns msp (modelspace) reference
    """
    msp = doc.modelspace()
    
    # Wall line
    msp.add_line(start_point, end_point, dxfattribs={
        'layer': 'WALLS',
        'color': colors.BLUE if wall_type == 'exterior' else colors.CYAN
    })
    
    # Calculate length
    length = ((end_point[0] - start_point[0])**2 + (end_point[1] - start_point[1])**2)**0.5
    
    # Add studs at 16" O.C.
    spacing = 16.0
    num_studs = int(length / spacing) + 1
    
    # Calculate stud positions along wall
    dx = (end_point[0] - start_point[0]) / length
    dy = (end_point[1] - start_point[1]) / length
    
    stud_layer = 'STUDS_EXTERIOR' if wall_type == 'exterior' else 'STUDS_INTERIOR'
    
    for i in range(num_studs):
        distance = i * spacing
        if distance > length:
            break
        
        x = start_point[0] + (distance * dx)
        y = start_point[1] + (distance * dy)
        
        # Draw stud (small rectangle to represent)
        stud_size = 1.5 if wall_type == 'exterior' else 1.5
        msp.add_circle((x, y), stud_size/2, dxfattribs={
            'layer': stud_layer,
            'color': colors.YELLOW
        })
    
    return msp

def create_cad_opening(doc, wall_start, wall_end, opening_width, opening_center_dist, 
                       header_size='2x8', opening_type='window'):
    """Create window/door opening in CAD with header, king/jack studs"""
    msp = doc.modelspace()
    
    # Calculate wall length and direction
    wall_length = ((wall_end[0] - wall_start[0])**2 + 
                   (wall_end[1] - wall_start[1])**2)**0.5
    dx = (wall_end[0] - wall_start[0]) / wall_length
    dy = (wall_end[1] - wall_start[1]) / wall_length
    
    # Opening center point
    center_x = wall_start[0] + (opening_center_dist * dx)
    center_y = wall_start[1] + (opening_center_dist * dy)
    
    # Rough opening (add shrinkage)
    if opening_type == 'window':
        ro_width = opening_width + 1.0  # Add 1" for window
        ro_height = 80.0  # Typical window rough opening
    else:  # door
        ro_width = opening_width + 2.0  # Add 2" for door
        ro_height = 82.5  # Standard door rough opening
    
    # Opening rectangle
    half_width = ro_width / 2
    
    # King studs (outer)
    king_offset = 3.5 / 2  # Half stud width
    msp.add_circle((center_x - half_width - king_offset, center_y), 0.75, dxfattribs={
        'layer': 'KING_STUDS',
        'color': colors.MAGENTA
    })
    msp.add_circle((center_x + half_width + king_offset, center_y), 0.75, dxfattribs={
        'layer': 'KING_STUDS',
        'color': colors.MAGENTA
    })
    
    # Header
    header_height = 7.25 if '2x8' in header_size else 9.25 if '2x10' in header_size else 11.25
    msp.add_line(
        (center_x - half_width, center_y + ro_height/2),
        (center_x + half_width, center_y + ro_height/2),
        dxfattribs={'layer': 'HEADERS', 'color': colors.GREEN, 'lineweight': 50}
    )
    
    # Opening rectangle
    opening_points = [
        (center_x - half_width, center_y - ro_height/2),
        (center_x + half_width, center_y - ro_height/2),
        (center_x + half_width, center_y + ro_height/2),
        (center_x - half_width, center_y + ro_height/2),
        (center_x - half_width, center_y - ro_height/2)
    ]
    msp.add_lwpolyline([(p[0], p[1]) for p in opening_points], dxfattribs={
        'layer': 'OPENINGS',
        'color': colors.RED,
        'lineweight': 30
    })
    
    # Label
    msp.add_text(
        f"{opening_type.upper()}\n{opening_width}\"w",
        dxfattribs={
            'layer': 'TEXT',
            'height': 8,
            'insert': (center_x, center_y),
            'halign': 1,  # Center
            'valign': 1  # Middle
        }
    )
    
    return msp

def generate_room_cad(room_name, dimensions, room_data):
    """Generate complete CAD drawing for a room from extracted data"""
    doc = ezdxf.new('R2010')  # AutoCAD 2010 format
    
    # Setup layers
    doc.layers.add('WALLS', color=colors.BLUE)
    doc.layers.add('STUDS_EXTERIOR', color=colors.YELLOW)
    doc.layers.add('STUDS_INTERIOR', color=colors.CYAN)
    doc.layers.add('HEADERS', color=colors.GREEN)
    doc.layers.add('KING_STUDS', color=colors.MAGENTA)
    doc.layers.add('OPENINGS', color=colors.RED)
    doc.layers.add('TEXT', color=colors.WHITE)
    doc.layers.add('DIMENSIONS', color=colors.YELLOW)
    
    msp = doc.modelspace()
    
    # Parse dimensions
    width_str, length_str = dimensions.split(' x ')
    width = parse_dimension_to_inches(width_str)
    length = parse_dimension_to_inches(length_str)
    
    # Draw room outline (walls)
    origin = (0, 0)
    
    # Exterior walls (2x6)
    if room_data.get('wall_type') == 'exterior':
        # North wall
        create_cad_wall(doc, origin, (length, 0), 'exterior', 96)
        # East wall
        create_cad_wall(doc, (length, 0), (length, width), 'exterior', 96)
        # South wall
        create_cad_wall(doc, (length, width), (0, width), 'exterior', 96)
        # West wall
        create_cad_wall(doc, (0, width), origin, 'exterior', 96)
    else:
        # Interior walls (2x4)
        create_cad_wall(doc, origin, (length, 0), 'interior', 96)
        create_cad_wall(doc, (length, 0), (length, width), 'interior', 96)
        create_cad_wall(doc, (length, width), (0, width), 'interior', 96)
        create_cad_wall(doc, (0, width), origin, 'interior', 96)
    
    # Add room label
    msp.add_text(
        f"{room_name}\n{dimensions}",
        dxfattribs={
            'layer': 'TEXT',
            'height': 12,
            'insert': (length/2, width/2),
            'halign': 1,
            'valign': 1
        }
    )
    
    # Save
    output_path = OUTPUT_DIR / f"{room_name.replace(' ', '_')}_framing.dxf"
    doc.saveas(output_path)
    print(f"✅ Created: {output_path}")
    
    return output_path

def parse_dimension_to_inches(dim_str):
    """Convert '14'-4"' to inches (172)"""
    dim_str = dim_str.strip().replace("'", "'").replace('"', '"')
    match = re.match(r"(\d+)'[\s]*-?[\s]*(\d+)\"", dim_str)
    if match:
        feet = int(match.group(1))
        inches = int(match.group(2))
        return feet * 12 + inches
    return 0

def process_blueprint_for_cad(blueprint_path):
    """Complete workflow: OCR → Extract → Generate CAD"""
    print(f"\n🔍 Processing: {blueprint_path.name}")
    
    # Step 1: OCR
    text_data = extract_text_from_blueprint(blueprint_path)
    print(f"   Extracted {len(text_data)} text elements")
    
    # Step 2: Parse data
    dimensions = parse_dimensions(text_data)
    beams = parse_beam_schedule(text_data)
    schedule = parse_window_door_schedule(text_data)
    
    print(f"   Found {len(dimensions)} dimensions")
    print(f"   Found {len(beams)} beams")
    print(f"   Found {len(schedule['windows'])} windows, {len(schedule['doors'])} doors")
    
    # Step 3: Generate structured data
    extracted_data = {
        'source_file': blueprint_path.name,
        'dimensions': dimensions,
        'beam_schedule': beams,
        'window_door_schedule': schedule,
        'raw_text': [item['text'] for item in text_data]
    }
    
    return extracted_data

def main():
    """Main execution"""
    print("🏗️  Blueprint OCR to CAD Converter")
    print("=" * 60)
    
    # Ensure output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Process floor plan
    floor_plan = BLUEPRINT_DIR / "ARCH" / "07-Proposed-FloorPlan.jpg"
    if floor_plan.exists():
        data = process_blueprint_for_cad(floor_plan)
        
        # Save extracted data
        import json
        data_file = OUTPUT_DIR / "extracted_blueprint_data.json"
        with open(data_file, 'w') as f:
            # Convert to JSON-serializable
            json_data = {
                'source_file': data['source_file'],
                'dimensions': data['dimensions'],
                'beam_schedule': data['beam_schedule'],
                'window_door_schedule': data['window_door_schedule']
            }
            json.dump(json_data, f, indent=2)
        print(f"✅ Saved extracted data: {data_file}")
    
    # Generate CAD for Office (example)
    office_data = {
        'dimensions': "12'-8\" x 11'-4\"",
        'wall_type': 'mixed',
        'name': 'Office'
    }
    generate_room_cad('Office', office_data['dimensions'], office_data)
    
    print("\n✅ Complete! Check 'cad_outputs' directory")

if __name__ == "__main__":
    main()

