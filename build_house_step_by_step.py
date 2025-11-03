#!/usr/bin/env python3
"""
Step-by-Step House Builder
Builds the 728 Cordant house room by room with exact dimensions

Each room is positioned relative to the previous one.
All dimensions are in FEET (converted from feet-inches notation)

Usage:
    python3 build_house_step_by_step.py
"""

import ezdxf

# =============================================================================
# CONVERSION HELPER
# =============================================================================

def feet_inches_to_feet(feet, inches):
    """Convert feet-inches to decimal feet"""
    return feet + (inches / 12.0)

# =============================================================================
# ROOM DEFINITIONS - EXACT FROM BLUEPRINT
# =============================================================================

ROOMS = [
    {
        "name": "OFFICE",
        "width": feet_inches_to_feet(12, 8),   # 12'-8"
        "length": feet_inches_to_feet(11, 4),  # 11'-4"
        "position": (0, 0),  # Starting point
        "wall_type": "interior"
    },
    {
        "name": "BEDROOM 2",
        "width": feet_inches_to_feet(14, 4),   # 14'-4"
        "length": feet_inches_to_feet(10, 8),  # 10'-8"
        "position": (0, feet_inches_to_feet(11, 4) + 1),  # North of Office (1' gap for wall)
        "wall_type": "interior"
    },
    {
        "name": "BEDROOM 3",
        "width": feet_inches_to_feet(14, 4),   # 14'-4"
        "length": feet_inches_to_feet(10, 8),  # 10'-8"
        "position": (0, feet_inches_to_feet(11, 4) + feet_inches_to_feet(10, 8) + 2),  # North of Bedroom 2
        "wall_type": "interior"
    },
    {
        "name": "LAUNDRY",
        "width": feet_inches_to_feet(8, 4),    # 8'-4"
        "length": feet_inches_to_feet(7, 6),   # 7'-6"
        "position": (feet_inches_to_feet(12, 8) + 1, feet_inches_to_feet(11, 4) + 1),
        "wall_type": "interior"
    },
    {
        "name": "GREAT ROOM",
        "width": feet_inches_to_feet(24, 2),   # 24'-2"
        "length": feet_inches_to_feet(19, 8),  # 19'-8"
        "position": (feet_inches_to_feet(12, 8) + feet_inches_to_feet(8, 4) + 2, 0),  # East of Office area
        "wall_type": "exterior",
        "vaulted": True
    },
    {
        "name": "KITCHEN",
        "width": feet_inches_to_feet(14, 6),   # 14'-6"
        "length": feet_inches_to_feet(17, 4),  # 17'-4"
        "position": (feet_inches_to_feet(12, 8) + feet_inches_to_feet(8, 4) + feet_inches_to_feet(24, 2) + 3, 0),
        "wall_type": "interior"
    },
    {
        "name": "NOOK",
        "width": feet_inches_to_feet(10, 4),   # 10'-4"
        "length": feet_inches_to_feet(11, 2),  # 11'-2"
        "position": (feet_inches_to_feet(12, 8) + feet_inches_to_feet(8, 4) + feet_inches_to_feet(24, 2) + feet_inches_to_feet(14, 6) + 4, 0),
        "wall_type": "interior"
    },
    {
        "name": "MASTER BEDROOM",
        "width": feet_inches_to_feet(15, 6),   # 15'-6"
        "length": feet_inches_to_feet(14, 8),  # 14'-8"
        "position": (feet_inches_to_feet(12, 8) + feet_inches_to_feet(8, 4) + feet_inches_to_feet(24, 2) + feet_inches_to_feet(14, 6) + feet_inches_to_feet(10, 4) + 5, 0),
        "wall_type": "exterior"
    },
    {
        "name": "MASTER BATHROOM",
        "width": feet_inches_to_feet(14, 2),   # 14'-2"
        "length": feet_inches_to_feet(13, 4),  # 13'-4"
        "position": (feet_inches_to_feet(12, 8) + feet_inches_to_feet(8, 4) + feet_inches_to_feet(24, 2) + feet_inches_to_feet(14, 6) + feet_inches_to_feet(10, 4) + 5, feet_inches_to_feet(14, 8) + 1),
        "wall_type": "interior"
    },
    {
        "name": "MASTER CLOSET",
        "width": feet_inches_to_feet(9, 8),    # 9'-8"
        "length": feet_inches_to_feet(7, 4),   # 7'-4"
        "position": (feet_inches_to_feet(12, 8) + feet_inches_to_feet(8, 4) + feet_inches_to_feet(24, 2) + feet_inches_to_feet(14, 6) + feet_inches_to_feet(10, 4) + 5, feet_inches_to_feet(14, 8) + feet_inches_to_feet(13, 4) + 2),
        "wall_type": "interior"
    },
    {
        "name": "PANTRY",
        "width": feet_inches_to_feet(7, 6),    # 7'-6"
        "length": feet_inches_to_feet(5, 8),   # 5'-8"
        "position": (feet_inches_to_feet(12, 8) + feet_inches_to_feet(8, 4) + feet_inches_to_feet(24, 2) + feet_inches_to_feet(14, 6) + 1, feet_inches_to_feet(17, 4) + 1),
        "wall_type": "interior"
    },
    {
        "name": "POWDER",
        "width": feet_inches_to_feet(6, 0),    # 6'-0"
        "length": feet_inches_to_feet(5, 4),   # 5'-4"
        "position": (feet_inches_to_feet(12, 8) + 1, feet_inches_to_feet(11, 4) + feet_inches_to_feet(10, 8) + feet_inches_to_feet(10, 8) + 3),
        "wall_type": "interior"
    },
    {
        "name": "MUD ROOM",
        "width": feet_inches_to_feet(9, 2),    # 9'-2"
        "length": feet_inches_to_feet(8, 6),   # 8'-6"
        "position": (0, feet_inches_to_feet(11, 4) + feet_inches_to_feet(10, 8) + feet_inches_to_feet(10, 8) + feet_inches_to_feet(7, 6) + 4),
        "wall_type": "interior"
    }
]

# =============================================================================
# DXF BUILDER
# =============================================================================

def draw_room(msp, room, scale=1.0):
    """
    Draw a single room as a rectangle with 4 walls
    
    Args:
        msp: DXF modelspace
        room: Room dictionary
        scale: Scale factor (1.0 = feet, 12.0 = inches)
    """
    x, y = room["position"]
    width = room["width"]
    length = room["length"]
    
    # Apply scale
    x *= scale
    y *= scale
    width *= scale
    length *= scale
    
    # Determine layer
    layer = 'WALLS-EXTERIOR' if room["wall_type"] == "exterior" else 'WALLS-INTERIOR'
    
    # Draw 4 walls (rectangle)
    walls = [
        ((x, y), (x + width, y)),                # Bottom wall
        ((x + width, y), (x + width, y + length)), # Right wall
        ((x + width, y + length), (x, y + length)),# Top wall
        ((x, y + length), (x, y))                  # Left wall
    ]
    
    for start, end in walls:
        msp.add_line(start, end, dxfattribs={'layer': layer})
    
    # Add room label
    label_x = x + width / 2
    label_y = y + length / 2
    
    msp.add_text(
        room["name"],
        dxfattribs={
            'layer': 'TEXT',
            'height': 6 * scale,
            'insert': (label_x, label_y)
        }
    )
    
    # Add dimensions
    dim_text = f"{room['width']:.2f}' x {room['length']:.2f}'"
    if room.get("vaulted"):
        dim_text += " VAULTED"
    
    msp.add_text(
        dim_text,
        dxfattribs={
            'layer': 'TEXT',
            'height': 4 * scale,
            'insert': (label_x, label_y - 4 * scale)
        }
    )


def build_house(output_file, scale=12.0):
    """
    Build the complete house step by step
    
    Args:
        output_file: Output DXF filename
        scale: Scale factor (12.0 = convert feet to inches for CAD)
    """
    print("="*70)
    print("🏗️  STEP-BY-STEP HOUSE BUILDER")
    print("="*70)
    print(f"\n📐 Building: 728 Cordant Drive")
    print(f"📊 Total Rooms: {len(ROOMS)}")
    print(f"📏 Scale: {scale}x (1 foot = {scale} units in CAD)")
    
    # Create DXF
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Create layers
    doc.layers.add('WALLS-EXTERIOR', color=1)   # Red
    doc.layers.add('WALLS-INTERIOR', color=3)   # Green
    doc.layers.add('TEXT', color=7)              # White/Black
    doc.layers.add('GRID', color=8)              # Gray
    
    # Add title
    msp.add_text(
        "728 CORDANT DRIVE - COMPLETE FLOOR PLAN",
        dxfattribs={
            'layer': 'TEXT',
            'height': 24,
            'insert': (200, -50)
        }
    )
    
    msp.add_text(
        "Built room-by-room with exact dimensions from blueprint",
        dxfattribs={
            'layer': 'TEXT',
            'height': 12,
            'insert': (200, -70)
        }
    )
    
    # Draw grid (optional reference)
    print("\n📐 Drawing reference grid...")
    for i in range(0, 1200, 120):  # Every 10 feet (120 inches)
        msp.add_line((i, -100), (i, 600), dxfattribs={'layer': 'GRID'})
        msp.add_line((-100, i), (1200, i), dxfattribs={'layer': 'GRID'})
    
    # Build each room
    print("\n🏗️  Building rooms...")
    for i, room in enumerate(ROOMS, 1):
        draw_room(msp, room, scale)
        status = "⭐ VAULTED" if room.get("vaulted") else ""
        print(f"  ✅ {i:2d}. {room['name']:<20} {room['width']:.2f}' × {room['length']:.2f}'  {status}")
    
    # Add legend
    legend_x = 50
    legend_y = -100
    
    msp.add_text("LEGEND:", dxfattribs={'layer': 'TEXT', 'height': 14, 'insert': (legend_x, legend_y)})
    
    msp.add_line((legend_x, legend_y - 20), (legend_x + 50, legend_y - 20), dxfattribs={'layer': 'WALLS-EXTERIOR'})
    msp.add_text("Exterior Walls (2x6)", dxfattribs={'layer': 'TEXT', 'height': 10, 'insert': (legend_x + 60, legend_y - 20)})
    
    msp.add_line((legend_x, legend_y - 40), (legend_x + 50, legend_y - 40), dxfattribs={'layer': 'WALLS-INTERIOR'})
    msp.add_text("Interior Walls (2x4)", dxfattribs={'layer': 'TEXT', 'height': 10, 'insert': (legend_x + 60, legend_y - 40)})
    
    # Save
    doc.saveas(output_file)
    
    print(f"\n✅ House built successfully!")
    print(f"📁 File: {output_file}")
    print("\n" + "="*70)
    print("📤 NEXT STEPS:")
    print("="*70)
    print("1. Go to AutoCAD Web")
    print("2. Upload this file")
    print("3. You'll see all rooms laid out with exact dimensions!")
    print("\n💡 All rooms are labeled and dimensioned")
    print("💡 Red = Exterior walls, Green = Interior walls")
    print("="*70 + "\n")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    OUTPUT_FILE = "728-cordant-COMPLETE-HOUSE.dxf"
    build_house(OUTPUT_FILE, scale=12.0)  # Scale to inches for better CAD viewing


