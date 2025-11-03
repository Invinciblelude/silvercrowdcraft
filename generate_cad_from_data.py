#!/usr/bin/env python3
"""
Generate AutoCAD DXF files from 728 Cordant Blueprint Data
Uses EXACT data from BLUEPRINT_DATA_EXTRACTION.md
No OCR needed - uses verified extracted data
"""

import ezdxf
from ezdxf import colors
import re
from pathlib import Path

OUTPUT_DIR = Path("cad_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# Room data from BLUEPRINT_DATA_EXTRACTION.md
ROOMS = {
    'Office': {
        'dimensions': "12'-8\" x 11'-4\"",
        'wall_type': 'mixed',
        'location': 'Southwest corner'
    },
    'Bedroom_2': {
        'dimensions': "14'-4\" x 10'-8\"",
        'wall_type': 'interior',
        'ceiling': '8-0'
    },
    'Bedroom_3': {
        'dimensions': "14'-4\" x 10'-8\"",
        'wall_type': 'interior',
        'ceiling': '8-0'
    },
    'Great_Room': {
        'dimensions': "24'-2\" x 19'-8\"",
        'wall_type': 'exterior',
        'ceiling': 'vaulted',
        'height_peak': '12-14'
    },
    'Master_Bedroom': {
        'dimensions': "15'-6\" x 14'-8\"",
        'wall_type': 'exterior',
        'ceiling': '8-0'
    },
    'Kitchen': {
        'dimensions': "14'-6\" x 17'-4\"",
        'wall_type': 'mixed'
    }
}

# Beam Schedule from blueprints
BEAM_SCHEDULE = {
    'B1': {'size': "3-3/4\" x 11\"", 'type': 'GLU. LAM.', 'species': 'DF/DF'},
    'B2': {'size': "3-1/8\" x 12\"", 'type': 'LAM.'},
    'B3': {'size': "5-1/8\" x 12\"", 'type': 'GLU. LAM.', 'species': 'DF/DF'},
    'B5': {'size': "(4) 2x12", 'type': 'HEADER'},
    'B9': {'size': "(5) 2x10", 'type': 'HEADER'},
}

def parse_dimension_to_inches(dim_str):
    """Convert '12'-8"' to inches"""
    dim_str = dim_str.strip().replace("'", "'").replace('"', '"')
    match = re.match(r"(\d+)'[\s]*-?[\s]*(\d+)\"", dim_str)
    if match:
        feet = int(match.group(1))
        inches = int(match.group(2))
        return feet * 12 + inches
    return 0

def create_cad_document(room_name):
    """Create new DXF document with proper layers"""
    doc = ezdxf.new('R2010')  # AutoCAD 2010 format
    
    # Create layers
    doc.layers.add('WALLS_EXTERIOR', color=colors.BLUE, lineweight=40)
    doc.layers.add('WALLS_INTERIOR', color=colors.CYAN, lineweight=30)
    doc.layers.add('STUDS_2X6', color=colors.YELLOW)
    doc.layers.add('STUDS_2X4', color=colors.CYAN)
    doc.layers.add('BOTTOM_PLATE', color=colors.MAGENTA, lineweight=50)
    doc.layers.add('TOP_PLATES', color=colors.RED, lineweight=50)
    doc.layers.add('HEADERS', color=colors.GREEN, lineweight=60)
    doc.layers.add('KING_STUDS', color=colors.MAGENTA)
    doc.layers.add('JACK_STUDS', color=colors.MAGENTA)
    doc.layers.add('OPENINGS', color=colors.RED)
    doc.layers.add('TEXT', color=colors.WHITE)
    doc.layers.add('DIMENSIONS', color=colors.YELLOW)
    doc.layers.add('ANCHOR_BOLTS', color=colors.RED)
    
    return doc

def draw_wall_with_studs(msp, start, end, wall_type='exterior', height=96):
    """Draw wall with studs at exact 16" O.C. spacing"""
    x1, y1 = start
    x2, y2 = end
    
    # Calculate wall length and direction
    length = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    dx = (x2 - x1) / length
    dy = (y2 - y1) / length
    
    # Wall line (bottom plate)
    msp.add_line(start, end, dxfattribs={
        'layer': 'BOTTOM_PLATE',
        'lineweight': 50
    })
    
    # Calculate stud positions (16" O.C. starting from first stud at edge)
    spacing = 16.0
    num_spacings = int(length / spacing)
    
    stud_layer = 'STUDS_2X6' if wall_type == 'exterior' else 'STUDS_2X4'
    stud_size = 1.5  # Actual 2x6 width
    
    stud_positions = []
    
    # First stud at start (accounting for stud half-width)
    first_stud_dist = 0.75  # Half stud width
    stud_x = x1 + (first_stud_dist * dx)
    stud_y = y1 + (first_stud_dist * dy)
    stud_positions.append((stud_x, stud_y))
    
    # Remaining studs at 16" intervals
    for i in range(1, num_spacings + 2):
        distance = first_stud_dist + (i * spacing)
        if distance > length - 0.75:  # Don't place beyond wall end
            break
        
        stud_x = x1 + (distance * dx)
        stud_y = y1 + (distance * dy)
        stud_positions.append((stud_x, stud_y))
    
    # Last stud at end
    last_stud_dist = length - 0.75
    if last_stud_dist > first_stud_dist:
        stud_x = x1 + (last_stud_dist * dx)
        stud_y = y1 + (last_stud_dist * dy)
        if (stud_x, stud_y) not in stud_positions:
            stud_positions.append((stud_x, stud_y))
    
    # Draw studs
    for sx, sy in stud_positions:
        # Stud circle (representing 2x6 or 2x4)
        msp.add_circle((sx, sy), stud_size/2, dxfattribs={
            'layer': stud_layer,
            'color': colors.YELLOW
        })
    
    # Top plates
    # Perpendicular offset for top plate (3" above bottom plate)
    perp_dx = -dy * 3.0  # Perpendicular offset
    perp_dy = dx * 3.0
    
    top_start = (x1 + perp_dx, y1 + perp_dy)
    top_end = (x2 + perp_dx, y2 + perp_dy)
    
    # Double top plate (two lines)
    msp.add_line(top_start, top_end, dxfattribs={
        'layer': 'TOP_PLATES',
        'lineweight': 50
    })
    msp.add_line(
        (top_start[0] + perp_dx*0.33, top_start[1] + perp_dy*0.33),
        (top_end[0] + perp_dx*0.33, top_end[1] + perp_dy*0.33),
        dxfattribs={
            'layer': 'TOP_PLATES',
            'lineweight': 50
        }
    )
    
    # Anchor bolts (exterior walls only, max 6'-0" spacing)
    if wall_type == 'exterior':
        bolt_spacing = 72.0  # 6'-0" max
        num_bolts = int(length / bolt_spacing) + 1
        
        for i in range(num_bolts + 1):
            bolt_dist = i * bolt_spacing
            if bolt_dist > length:
                break
            
            bolt_x = x1 + (bolt_dist * dx)
            bolt_y = y1 + (bolt_dist * dy)
            
            msp.add_circle((bolt_x, bolt_y), 0.3125, dxfattribs={  # 5/8" bolt
                'layer': 'ANCHOR_BOLTS',
                'color': colors.RED
            })
    
    return stud_positions

def generate_room_cad(room_name, room_data):
    """Generate complete CAD drawing for a room"""
    print(f"\n📐 Generating CAD for: {room_name}")
    
    # Parse dimensions
    dims = room_data['dimensions'].split(' x ')
    width_str = dims[1] if len(dims) > 1 else dims[0]
    length_str = dims[0]
    
    width = parse_dimension_to_inches(width_str)
    length = parse_dimension_to_inches(length_str)
    
    print(f"   Dimensions: {length}\" x {width}\" ({room_data['dimensions']})")
    
    # Create document
    doc = create_cad_document(room_name)
    msp = doc.modelspace()
    
    # Room outline (starting at origin)
    origin = (0, 0)
    corners = [
        origin,                          # Southwest
        (length, 0),                     # Southeast
        (length, width),                 # Northeast
        (0, width),                      # Northwest
        origin                           # Close rectangle
    ]
    
    # Determine wall types
    wall_type = room_data.get('wall_type', 'interior')
    is_exterior = wall_type == 'exterior' or 'mixed' in wall_type
    
    # Draw walls with studs
    walls = [
        ((0, 0), (length, 0), 'north'),      # North wall
        ((length, 0), (length, width), 'east'),  # East wall
        ((length, width), (0, width), 'south'), # South wall
        ((0, width), (0, 0), 'west')         # West wall
    ]
    
    for start, end, direction in walls:
        this_wall_type = 'exterior' if is_exterior else 'interior'
        stud_positions = draw_wall_with_studs(msp, start, end, this_wall_type, 96)
        print(f"   {direction.capitalize()} wall: {len(stud_positions)} studs @ 16\" O.C.")
    
    # Add room label
    msp.add_text(
        room_name.replace('_', ' '),
        dxfattribs={
            'layer': 'TEXT',
            'height': 24,
            'insert': (length/2, width/2),
            'halign': 1,  # Center
            'valign': 1  # Middle
        }
    )
    
    # Add dimensions text
    msp.add_text(
        f"{room_data['dimensions']}",
        dxfattribs={
            'layer': 'TEXT',
            'height': 12,
            'insert': (length/2, width/2 - 20),
            'halign': 1
        }
    )
    
    # Add specifications
    spec_text = f"Wall Type: {'2x6 @ 16\" O.C.' if is_exterior else '2x4 @ 16\" O.C.'}\n"
    spec_text += f"Height: 8'-0\"\n"
    if room_data.get('ceiling') == 'vaulted':
        spec_text += f"Ceiling: VAULTED (12'-14' peak)"
    
    msp.add_text(
        spec_text,
        dxfattribs={
            'layer': 'TEXT',
            'height': 8,
            'insert': (length + 24, width/2),
            'halign': 0
        }
    )
    
    # Save file
    filename = f"{room_name}_framing.dxf"
    output_path = OUTPUT_DIR / filename
    doc.saveas(output_path)
    print(f"   ✅ Created: {output_path}")
    print(f"   📁 File size: {output_path.stat().st_size / 1024:.1f} KB")
    
    return output_path

def main():
    """Generate CAD files for all rooms"""
    print("🏗️  728 Cordant - CAD Generator")
    print("=" * 60)
    print("Using EXACT data from BLUEPRINT_DATA_EXTRACTION.md")
    print()
    
    generated = []
    
    # Generate for specific rooms
    rooms_to_generate = ['Office', 'Great_Room', 'Master_Bedroom']
    
    for room_name in rooms_to_generate:
        if room_name in ROOMS:
            output = generate_room_cad(room_name, ROOMS[room_name])
            generated.append(output)
    
    print("\n" + "=" * 60)
    print(f"✅ Generated {len(generated)} CAD files")
    print(f"\n📤 Upload these to AutoCAD:")
    for path in generated:
        print(f"   - {path}")
    print(f"\n🌐 Or open at: autocad.com")
    print()

if __name__ == "__main__":
    main()

