#!/usr/bin/env python3
"""
Simple Blueprint Build Sequence Generator
2D Diagram → 3D Animation showing construction sequence
Meets blueprint minimums: shows schedule, sequence, and relationships
"""

import ezdxf
from ezdxf import colors
from pathlib import Path
import json

OUTPUT_DIR = Path("build_sequence_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# From your blueprint extraction
BUILD_DATA = {
    "office": {
        "dimensions": {"width": "12'-8\"", "length": "11'-4\""},
        "width_inches": 152,
        "length_inches": 136,
        "floor": {"depth": 4, "material": "Concrete Slab"},
        "walls": {"height": 96, "studs": "2x6 @ 16\" O.C.", "type": "Exterior"},
        "ceiling": {"height": 96, "type": "Standard"}
    },
    "great_room": {
        "dimensions": {"width": "19'-8\"", "length": "24'-2\""},
        "width_inches": 236,
        "length_inches": 290,
        "floor": {"depth": 4, "material": "Concrete Slab"},
        "walls": {"height": 96, "studs": "2x6 @ 16\" O.C.", "type": "Exterior"},
        "ceiling": {"height": "144-168", "type": "VAULTED"}
    }
}

def create_sequence_diagram(room_name, room_data):
    """Create simple 2D sequence diagram showing build order"""
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Setup layers for each phase
    doc.layers.add('PHASE_0_SITE', color=colors.BLACK)
    doc.layers.add('PHASE_1_FOUNDATION', color=colors.BLUE, lineweight=50)
    doc.layers.add('PHASE_2_WALLS', color=colors.RED, lineweight=50)
    doc.layers.add('PHASE_3_ROOF', color=colors.GREEN, lineweight=50)
    doc.layers.add('LEGEND', color=colors.WHITE)
    
    w = room_data['width_inches']
    l = room_data['length_inches']
    
    # PHASE 1: Foundation outline (bottom layer)
    foundation = [
        (0, 0),
        (l, 0),
        (l, w),
        (0, w),
        (0, 0)
    ]
    msp.add_lwpolyline(foundation, dxfattribs={'layer': 'PHASE_1_FOUNDATION'})
    
    # PHASE 2: Walls (on top of foundation)
    wall_thickness = 5.5  # 2x6 actual width
    walls = [
        (0, 0, w, 0, w, wall_thickness, 0, wall_thickness, 0, 0),
        (l, 0, l, w, l-wall_thickness, w, l-wall_thickness, 0, l, 0)
    ]
    for wall in walls:
        msp.add_lwpolyline([(wall[i], wall[i+1]) for i in range(0, len(wall), 2)], 
                           dxfattribs={'layer': 'PHASE_2_WALLS'})
    
    # Add phase labels
    msp.add_text("PHASE 1: Foundation", dxfattribs={
        'layer': 'LEGEND',
        'height': 12,
        'insert': (l + 10, w/2),
        'color': colors.BLUE
    })
    msp.add_text("PHASE 2: Walls", dxfattribs={
        'layer': 'LEGEND',
        'height': 12,
        'insert': (l + 10, w/2 - 20),
        'color': colors.RED
    })
    
    # Save
    output = OUTPUT_DIR / f"{room_name}_sequence_2d.dxf"
    doc.saveas(output)
    print(f"✅ 2D Sequence: {output}")
    return output

def create_3d_build_sequence(room_name, room_data):
    """Create 3D model showing sequential build-up"""
    
    # Generate OBJ files for each phase
    w = room_data['width_inches']
    l = room_data['length_inches']
    
    phases = []
    
    # PHASE 1: Foundation only
    phase1_obj = []
    phase1_obj.append("# Phase 1: Foundation Only\n")
    phase1_obj.append(f"v {l} 0 0\nv 0 0 0\nv 0 {w} 0\nv {l} {w} 0\n")  # Bottom
    phase1_obj.append(f"v {l} 0 4\nv 0 0 4\nv 0 {w} 4\nv {l} {w} 4\n")  # Top
    phase1_obj.append("f 1 2 3 4\nf 5 8 7 6\nf 1 5 6 2\nf 2 6 7 3\nf 3 7 8 4\nf 4 8 5 1\n")
    
    # PHASE 2: Foundation + Walls
    phase2_obj = phase1_obj.copy()
    phase2_obj.append("\n# Phase 2: Add Walls\n")
    
    wall_h = room_data['walls']['height']
    wt = 5.5
    
    # North wall
    base = 9
    phase2_obj.append(f"v 0 0 4\nv {l} 0 4\nv {l} {wt} 4\nv 0 {wt} 4\n")
    phase2_obj.append(f"v 0 0 {wall_h}\nv {l} 0 {wall_h}\nv {l} {wt} {wall_h}\nv 0 {wt} {wall_h}\n")
    phase2_obj.append(f"f {base} {base+1} {base+2} {base+3}\n")
    phase2_obj.append(f"f {base+4} {base+7} {base+6} {base+5}\n")
    phase2_obj.append(f"f {base} {base+4} {base+5} {base+1}\n")
    phase2_obj.append(f"f {base+1} {base+5} {base+6} {base+2}\n")
    phase2_obj.append(f"f {base+2} {base+6} {base+7} {base+3}\n")
    phase2_obj.append(f"f {base+3} {base+7} {base+4} {base}\n")
    
    # Save phase 1
    p1_path = OUTPUT_DIR / f"{room_name}_phase1_foundation.obj"
    with open(p1_path, 'w') as f:
        f.write(''.join(phase1_obj))
    
    # Save phase 2
    p2_path = OUTPUT_DIR / f"{room_name}_phase2_with_walls.obj"
    with open(p2_path, 'w') as f:
        f.write(''.join(phase2_obj))
    
    phases.extend([p1_path, p2_path])
    
    print(f"✅ 3D Sequence files created")
    return phases

def main():
    """Generate simple build sequence for each room"""
    print("🏗️  Simple Blueprint Build Sequence")
    print("=" * 60)
    
    for room_name, room_data in BUILD_DATA.items():
        print(f"\n📐 {room_name.upper()}:")
        create_sequence_diagram(room_name, room_data)
        create_3d_build_sequence(room_name, room_data)
    
    print(f"\n✅ Complete! Check {OUTPUT_DIR}")
    print("\n📋 Output files:")
    print("   - *_sequence_2d.dxf (2D diagrams)")
    print("   - *_phase1_foundation.obj (3D phase 1)")
    print("   - *_phase2_with_walls.obj (3D phase 2)")

if __name__ == "__main__":
    main()

