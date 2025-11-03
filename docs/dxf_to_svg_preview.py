#!/usr/bin/env python3
"""
Convert DXF files to SVG previews for web display
Creates visual 2D diagrams from CAD files
"""

import ezdxf
from pathlib import Path
import xml.etree.ElementTree as ET

OUTPUT_DIR = Path("docs/assets/cad-previews")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

def dxf_to_svg(dxf_path, svg_path, width=800, height=600):
    """Convert DXF to SVG for web display"""
    try:
        doc = ezdxf.readfile(dxf_path)
        msp = doc.modelspace()
        
        # Calculate bounding box
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')
        
        entities = list(msp)
        if not entities:
            return None
        
        for entity in entities:
            if entity.dxftype() == 'LINE':
                min_x = min(min_x, entity.dxf.start.x, entity.dxf.end.x)
                min_y = min(min_y, entity.dxf.start.y, entity.dxf.end.y)
                max_x = max(max_x, entity.dxf.start.x, entity.dxf.end.x)
                max_y = max(max_y, entity.dxf.start.y, entity.dxf.end.y)
            elif entity.dxftype() == 'CIRCLE':
                cx, cy = entity.dxf.center.x, entity.dxf.center.y
                r = entity.dxf.radius
                min_x = min(min_x, cx - r)
                min_y = min(min_y, cy - r)
                max_x = max(max_x, cx + r)
                max_y = max(max_y, cy + r)
            elif entity.dxftype() == 'LWPOLYLINE':
                for point in entity.vertices():
                    min_x = min(min_x, point[0])
                    min_y = min(min_y, point[1])
                    max_x = max(max_x, point[0])
                    max_y = max(max_y, point[1])
        
        # Calculate scale
        if max_x - min_x == 0 or max_y - min_y == 0:
            return None
        
        scale_x = (width - 40) / (max_x - min_x)
        scale_y = (height - 40) / (max_y - min_y)
        scale = min(scale_x, scale_y)
        
        # Offset to center
        offset_x = (width - (max_x - min_x) * scale) / 2 - min_x * scale
        offset_y = (height - (max_y - min_y) * scale) / 2 - min_y * scale
        
        # Create SVG
        svg = ET.Element('svg', {
            'width': str(width),
            'height': str(height),
            'xmlns': 'http://www.w3.org/2000/svg',
            'style': 'background:#0a0e27'
        })
        
        # Color mapping
        color_map = {
            'BOTTOM_PLATE': '#fb923c',
            'TOP_PLATES': '#ef4444',
            'STUDS_2X6': '#fbbf24',
            'STUDS_2X4': '#60a5fa',
            'WALLS_EXTERIOR': '#2563eb',
            'WALLS_INTERIOR': '#3b82f6',
            'ANCHOR_BOLTS': '#ef4444',
            'TEXT': '#ffffff'
        }
        
        # Process entities
        for entity in entities:
            layer = entity.dxf.layer
            color = color_map.get(layer, '#ffffff')
            
            if entity.dxftype() == 'LINE':
                x1 = entity.dxf.start.x * scale + offset_x
                y1 = height - (entity.dxf.start.y * scale + offset_y)
                x2 = entity.dxf.end.x * scale + offset_x
                y2 = height - (entity.dxf.end.y * scale + offset_y)
                
                line = ET.SubElement(svg, 'line', {
                    'x1': str(x1),
                    'y1': str(y1),
                    'x2': str(x2),
                    'y2': str(y2),
                    'stroke': color,
                    'stroke-width': '2'
                })
            
            elif entity.dxftype() == 'CIRCLE':
                cx = entity.dxf.center.x * scale + offset_x
                cy = height - (entity.dxf.center.y * scale + offset_y)
                r = entity.dxf.radius * scale
                
                circle = ET.SubElement(svg, 'circle', {
                    'cx': str(cx),
                    'cy': str(cy),
                    'r': str(r),
                    'fill': color,
                    'stroke': '#000000',
                    'stroke-width': '1'
                })
            
            elif entity.dxftype() == 'LWPOLYLINE':
                points = []
                for point in entity.vertices():
                    x = point[0] * scale + offset_x
                    y = height - (point[1] * scale + offset_y)
                    points.append(f"{x},{y}")
                
                polyline = ET.SubElement(svg, 'polyline', {
                    'points': ' '.join(points),
                    'fill': 'none',
                    'stroke': color,
                    'stroke-width': '3',
                    'stroke-linejoin': 'round'
                })
        
        # Write SVG
        tree = ET.ElementTree(svg)
        ET.indent(tree, space="  ")
        tree.write(svg_path, encoding='utf-8', xml_declaration=True)
        
        return svg_path
    except Exception as e:
        print(f"Error converting {dxf_path}: {e}")
        return None

def main():
    """Convert all DXF files to SVG"""
    dxf_dir = Path("docs/build_sequence_outputs")
    svg_dir = OUTPUT_DIR
    
    print("🎨 Converting DXF to SVG previews...")
    
    for dxf_file in dxf_dir.glob("*.dxf"):
        svg_file = svg_dir / f"{dxf_file.stem}.svg"
        result = dxf_to_svg(dxf_file, svg_file)
        if result:
            print(f"✅ {dxf_file.name} → {svg_file.name}")
        else:
            print(f"⚠️  Failed: {dxf_file.name}")
    
    # Also convert CAD files
    cad_dir = Path("docs/cad_outputs")
    if cad_dir.exists():
        for dxf_file in cad_dir.glob("*.dxf"):
            svg_file = svg_dir / f"{dxf_file.stem}.svg"
            result = dxf_to_svg(dxf_file, svg_file, width=1000, height=800)
            if result:
                print(f"✅ {dxf_file.name} → {svg_file.name}")

if __name__ == "__main__":
    main()

