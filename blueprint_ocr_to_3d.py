#!/usr/bin/env python3
"""
Complete Blueprint OCR → 2D CAD → 3D Model System
Extracts EXACT data from blueprint PDFs/images using OCR
Then generates both 2D CAD (DXF) and 3D models (GLTF/OBJ)
"""

import ezdxf
from ezdxf import colors
import cv2
import numpy as np
from PIL import Image
import re
from pathlib import Path
import json
import math
import shutil

# Try to import OCR libraries (optional)
try:
    import pytesseract
    # Pick first available tesseract path (Homebrew/MacPorts/intel)
    CANDIDATE_PATHS = [
        "/opt/homebrew/bin/tesseract",   # Apple Silicon (Homebrew)
        "/usr/local/bin/tesseract",      # Intel Homebrew
        "/opt/local/bin/tesseract",      # MacPorts
        "tesseract"                       # PATH
    ]
    for cand in CANDIDATE_PATHS:
        if cand == "tesseract" and shutil.which('tesseract'):
            pytesseract.pytesseract.tesseract_cmd = 'tesseract'; break
        if cand != "tesseract" and Path(cand).exists():
            pytesseract.pytesseract.tesseract_cmd = cand; break
except ImportError:
    pytesseract = None

try:
    import pdf2image
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

BLUEPRINT_DIR = Path("blueprints")
PDF_PATH = BLUEPRINT_DIR / "incoming" / "728 Cortlandt Drive Plans actual.pdf"
OUTPUT_DIR = Path("cad_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# Structured data storage
EXTRACTED_DATA = {
    'rooms': {},
    'dimensions': {},
    'beam_schedule': {},
    'window_door_schedule': {},
    'wall_specifications': {},
    'notes': []
}

def extract_text_from_image(image_path):
    """Extract text from blueprint image using OCR"""
    if pytesseract is None:
        print("⚠️  pytesseract not installed")
        return []
    # Resolve actual binary path used
    tess_cmd = getattr(pytesseract.pytesseract, 'tesseract_cmd', 'tesseract')
    if tess_cmd == 'tesseract' and not shutil.which('tesseract'):
        print("⚠️  tesseract binary not found; expected one of /opt/homebrew/bin/tesseract, /usr/local/bin/tesseract")
        return []

    print(f"📄 OCR: Extracting from {image_path.name}")
    img = cv2.imread(str(image_path))
    if img is None:
        return []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)

    try:
        data = pytesseract.image_to_data(enhanced, output_type=pytesseract.Output.DICT)
        extracted = []
        for i in range(len(data['text'])):
            text = data['text'][i].strip()
            try:
                conf = float(data['conf'][i])
            except Exception:
                conf = 0.0
            if len(text) > 0 and conf >= 30:
                extracted.append({
                    'text': text,
                    'x': data['left'][i],
                    'y': data['top'][i],
                    'width': data['width'][i],
                    'height': data['height'][i],
                    'conf': conf
                })
        print(f"   ✅ Extracted {len(extracted)} text elements")
        return extracted
    except Exception as e:
        print(f"   ⚠️  OCR Error: {e}")
        return []

def extract_from_pdf(pdf_path):
    """Extract pages from PDF as images, then OCR. Skip if poppler/pdf2image missing."""
    if not PDF_AVAILABLE or not pdf_path.exists():
        return []
    try:
        pages = pdf2image.convert_from_path(pdf_path, dpi=300)
        print(f"   Found {len(pages)} pages")
        all_extracted = []
        for i, page in enumerate(pages):
            temp_path = OUTPUT_DIR / f"temp_page_{i+1}.png"
            page.save(temp_path, 'PNG')
            extracted = extract_text_from_image(temp_path)
            all_extracted.extend(extracted)
            temp_path.unlink(missing_ok=True)
        return all_extracted
    except Exception as e:
        print(f"   ⚠️  PDF Error: {e}")
        return []

def parse_dimension_string(dim_str):
    """Parse architectural dimensions: '14'-4"' → {'feet': 14, 'inches': 4, 'total_inches': 172}"""
    dim_str = dim_str.strip().replace("'", "'").replace('"', '"')
    
    patterns = [
        r"(\d+)'[\s]*-?[\s]*(\d+)\"",  # 14'-4"
        r"(\d+)['\s]+(\d+)\"",          # 14' 4"
        r"(\d+)['\s]+(\d+)\s*-\s*(\d+)\"",  # 14' 4-1/2"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, dim_str)
        if match:
            feet = int(match.group(1))
            inches = int(match.group(2))
            return {
                'feet': feet,
                'inches': inches,
                'total_inches': feet * 12 + inches,
                'formatted': f"{feet}'-{inches}\""
            }
    
    return None

def extract_room_data(text_data):
    """Extract room dimensions and names from OCR text"""
    rooms = {}
    current_room = None
    
    # Room name patterns
    room_patterns = [
        r'(BEDROOM|BEDROOM\s+\d+|MASTER|OFFICE|KITCHEN|GREAT\s+ROOM|LAUNDRY|MUD\s+ROOM|POWDER|CLOSET|BATHROOM)',
        r'(BED\s+\d+|BR\s+\d+)'
    ]
    
    for item in text_data:
        text = item['text'].strip()
        
        # Check if it's a room name
        for pattern in room_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                current_room = match.group(1).upper().replace(' ', '_')
                rooms[current_room] = {
                    'name': match.group(1),
                    'position': (item['x'], item['y'])
                }
                break
        
        # Check for dimensions near room names
        if current_room:
            dim = parse_dimension_string(text)
            if dim:
                if 'dimensions' not in rooms[current_room]:
                    rooms[current_room]['dimensions'] = []
                rooms[current_room]['dimensions'].append(dim)
    
    return rooms

def extract_beam_schedule(text_data):
    """Extract beam schedule (B1, B2, etc.) from structural plans"""
    beams = {}
    current_beam = None
    
    for item in text_data:
        text = item['text'].strip()
        
        # Beam ID pattern
        beam_match = re.match(r'B(\d+)', text.upper())
        if beam_match:
            current_beam = f"B{beam_match.group(1)}"
            beams[current_beam] = {
                'id': current_beam,
                'position': (item['x'], item['y'])
            }
        
        # Beam size patterns
        if current_beam:
            size_patterns = [
                r'(\d+)[- ](\d+)/(\d+)[\s]*"[\s]*x[\s]*(\d+)[\s]*"',  # 3-3/4" x 11"
                r'\((\d+)\)[\s]*2x(\d+)',  # (4) 2x12
                r'(\d+\.?\d*)[\s]*x[\s]*(\d+\.?\d*)',  # 5.25 x 12
            ]
            
            for pattern in size_patterns:
                match = re.search(pattern, text)
                if match:
                    beams[current_beam]['size_text'] = text
                    break
    
    return beams

def create_2d_cad_from_extracted(room_data, output_path):
    """Create 2D CAD (DXF) from extracted room data"""
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Setup layers
    doc.layers.add('WALLS_EXTERIOR', color=colors.BLUE, lineweight=40)
    doc.layers.add('STUDS_2X6', color=colors.YELLOW)
    doc.layers.add('BOTTOM_PLATE', color=colors.MAGENTA, lineweight=50)
    doc.layers.add('TOP_PLATES', color=colors.RED, lineweight=50)
    doc.layers.add('TEXT', color=colors.WHITE)
    
    # Get dimensions
    if 'dimensions' in room_data and len(room_data['dimensions']) >= 2:
        width = room_data['dimensions'][0]['total_inches']
        length = room_data['dimensions'][1]['total_inches']
        
        # Draw walls
        corners = [(0, 0), (length, 0), (length, width), (0, width)]
        
        for i in range(4):
            start = corners[i]
            end = corners[(i + 1) % 4]
            
            # Bottom plate
            msp.add_line(start, end, dxfattribs={
                'layer': 'BOTTOM_PLATE',
                'lineweight': 50
            })
            
            # Studs @ 16" O.C.
            wall_length = ((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5
            spacing = 16.0
            num_studs = int(wall_length / spacing) + 1
            
            dx = (end[0] - start[0]) / wall_length if wall_length > 0 else 0
            dy = (end[1] - start[1]) / wall_length if wall_length > 0 else 0
            
            for j in range(num_studs):
                dist = j * spacing
                if dist <= wall_length:
                    stud_x = start[0] + (dist * dx)
                    stud_y = start[1] + (dist * dy)
                    msp.add_circle((stud_x, stud_y), 0.75, dxfattribs={
                        'layer': 'STUDS_2X6',
                        'color': colors.YELLOW
                    })
        
        # Room label
        room_name = room_data.get('name', 'Room')
        msp.add_text(
            f"{room_name}\n{width}\" x {length}\"",
            dxfattribs={
                'layer': 'TEXT',
                'height': 24,
                'insert': (length/2, width/2),
                'halign': 1,
                'valign': 1
            }
        )
    
    doc.saveas(output_path)
    print(f"✅ 2D CAD created: {output_path}")
    return output_path

def create_3d_model_from_2d(dxf_path, output_gltf_path):
    """Convert 2D DXF to 3D model (extrude walls)"""
    try:
        doc = ezdxf.readfile(dxf_path)
        msp = doc.modelspace()
        
        # Read wall lines
        walls = []
        studs = []
        
        for entity in msp:
            if entity.dxftype() == 'LINE':
                if entity.dxf.layer in ['BOTTOM_PLATE', 'WALLS_EXTERIOR']:
                    start = (entity.dxf.start.x, entity.dxf.start.y)
                    end = (entity.dxf.end.x, entity.dxf.end.y)
                    walls.append((start, end))
            
            elif entity.dxftype() == 'CIRCLE':
                if entity.dxf.layer == 'STUDS_2X6':
                    studs.append((entity.dxf.center.x, entity.dxf.center.y))
        
        # Generate 3D OBJ file (simple format)
        obj_content = []
        obj_content.append("# 3D Model from 728 Cordant Blueprints\n")
        obj_content.append("# Extruded from 2D CAD\n\n")
        
        vertex_count = 1
        wall_height = 96.0  # 8'-0" in inches
        
        # Extrude walls to 3D
        for (start, end) in walls:
            x1, y1 = start
            x2, y2 = end
            
            # Wall vertices (rectangle extruded)
            # Bottom face
            obj_content.append(f"v {x1} {y1} 0.0\n")
            obj_content.append(f"v {x2} {y2} 0.0\n")
            # Top face
            obj_content.append(f"v {x1} {y1} {wall_height}\n")
            obj_content.append(f"v {x2} {y2} {wall_height}\n")
            
            # Faces
            base = vertex_count
            obj_content.append(f"f {base} {base+1} {base+3} {base+2}\n")
            vertex_count += 4
        
        # Add studs as vertical columns
        stud_height = 90.5  # 96" - 5.5" (plates)
        stud_width = 1.5
        
        for sx, sy in studs[:20]:  # Limit to first 20 for simplicity
            # Stud vertices (small column)
            obj_content.append(f"v {sx-stud_width/2} {sy-stud_width/2} 0.0\n")
            obj_content.append(f"v {sx+stud_width/2} {sy-stud_width/2} 0.0\n")
            obj_content.append(f"v {sx+stud_width/2} {sy+stud_width/2} 0.0\n")
            obj_content.append(f"v {sx-stud_width/2} {sy+stud_width/2} 0.0\n")
            obj_content.append(f"v {sx-stud_width/2} {sy-stud_width/2} {stud_height}\n")
            obj_content.append(f"v {sx+stud_width/2} {sy-stud_width/2} {stud_height}\n")
            obj_content.append(f"v {sx+stud_width/2} {sy+stud_width/2} {stud_height}\n")
            obj_content.append(f"v {sx-stud_width/2} {sy+stud_width/2} {stud_height}\n")
            
            base = vertex_count
            # Bottom
            obj_content.append(f"f {base} {base+1} {base+2} {base+3}\n")
            # Top
            obj_content.append(f"f {base+4} {base+7} {base+6} {base+5}\n")
            # Sides
            obj_content.append(f"f {base} {base+4} {base+5} {base+1}\n")
            obj_content.append(f"f {base+1} {base+5} {base+6} {base+2}\n")
            obj_content.append(f"f {base+2} {base+6} {base+7} {base+3}\n")
            obj_content.append(f"f {base+3} {base+7} {base+4} {base}\n")
            
            vertex_count += 8
        
        # Save OBJ file
        obj_path = output_gltf_path.with_suffix('.obj')
        with open(obj_path, 'w') as f:
            f.write(''.join(obj_content))
        
        print(f"✅ 3D Model created: {obj_path}")
        return obj_path
        
    except Exception as e:
        print(f"⚠️  3D conversion error: {e}")
        return None

def main():
    """Main workflow: OCR → Extract → 2D CAD → 3D Model"""
    print("🏗️  Blueprint OCR → 2D CAD → 3D Model System")
    print("=" * 70)
    
    # Step 1: Extract from PDF
    if PDF_PATH.exists():
        print("\n📑 STEP 1: Extract from PDF")
        pdf_text = extract_from_pdf(PDF_PATH)
        EXTRACTED_DATA['pdf_text'] = pdf_text
    
    # Step 2: Extract from blueprint images
    print("\n📄 STEP 2: Extract from Blueprint Images")
    floor_plan = BLUEPRINT_DIR / "classified" / "ARCH" / "07-Proposed-FloorPlan.jpg"
    if floor_plan.exists():
        image_text = extract_text_from_image(floor_plan)
        EXTRACTED_DATA['floor_plan_text'] = image_text
        
        # Parse extracted data
        rooms = extract_room_data(image_text)
        beams = extract_beam_schedule(image_text)
        
        EXTRACTED_DATA['rooms'] = rooms
        EXTRACTED_DATA['beam_schedule'] = beams
        
        print(f"   ✅ Found {len(rooms)} rooms")
        print(f"   ✅ Found {len(beams)} beams")
    
    # Step 3: Generate 2D CAD from extracted data
    print("\n📐 STEP 3: Generate 2D CAD from Extracted Data")
    for room_name, room_data in EXTRACTED_DATA['rooms'].items():
        if 'dimensions' in room_data and len(room_data['dimensions']) >= 2:
            dxf_path = OUTPUT_DIR / f"{room_name}_from_ocr.dxf"
            create_2d_cad_from_extracted(room_data, dxf_path)
            
            # Step 4: Convert to 3D
            print(f"\n🎨 STEP 4: Convert {room_name} to 3D")
            gltf_path = OUTPUT_DIR / f"{room_name}_3d"
            create_3d_model_from_2d(dxf_path, gltf_path)
    
    # Save extracted data
    data_file = OUTPUT_DIR / "ocr_extracted_data.json"
    with open(data_file, 'w') as f:
        # Make JSON serializable
        json_data = {
            'rooms': {k: {**v} for k, v in EXTRACTED_DATA['rooms'].items()},
            'beam_schedule': EXTRACTED_DATA['beam_schedule']
        }
        json.dump(json_data, f, indent=2, default=str)
    
    print(f"\n✅ Complete! Extracted data saved to: {data_file}")
    print(f"\n📁 Output directory: {OUTPUT_DIR}")
    print("\n📝 Next: Use extracted data to generate accurate 2D/3D models")

if __name__ == "__main__":
    main()

