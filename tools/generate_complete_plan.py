#!/usr/bin/env python3
"""
Generate COMPLETE construction plan with:
- 70+ detailed tasks
- 5,800 realistic hours
- Accurate blueprint matching
- All phases from demo to final
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

OUTPUT_DIR = Path("/Users/invinciblelude/728 Cordant project/docs/assets")
SOPS_DIR = Path("/Users/invinciblelude/728 Cordant project/docs/sops")

PROJECT_DATA = {
    "name": "728 Cortlandt Drive Addition",
    "address": "728 Cortlandt Drive, Sacramento, CA 95864",
    "parcel": "292-0162-010-0000",
    "architect": "Eric Knutson",
    "permit_date": "6/1/2025",
    "existing_sf": 2611,
    "new_addition_sf": 3200,
    "total_sf": 5811,
}

# Blueprint reference mapping (correct sheet numbers)
BLUEPRINTS = {
    "floor_plan": "07",  # Proposed Floor Plan - PRIMARY REFERENCE
    "floor_plan_asbuilt": "03",
    "site_plan": "06",  # Proposed Site Plan
    "roof_plan": "08",  # Proposed Roof Plan
    "elevations_front": "10",
    "elevations_rear": "11",
    "foundation": "12",  # Structural Foundation Plan
    "foundation_iso": "13",
    "shear_wall": "14",
    "roof_framing": "15",
    "struct_details": ["16", "17", "18", "19", "20", "21", "22"],
    "struct_notes": "23",
    "schedules": "01",  # Schedules & Specifications
    "cover": "00",
}

# ALL TASKS - Complete construction sequence
ALL_TASKS = [
    # PHASE 1: DEMOLITION & SITE PREP (80 hours total)
    {"id": "01-DEMO-001", "phase": "01. Demolition & Site Prep", "name": "Demo Existing Fences", "hours": 16, "crew": 2, "sheets": ["07", "06"]},
    {"id": "01-DEMO-002", "phase": "01. Demolition & Site Prep", "name": "Site Layout & Staking", "hours": 16, "crew": 2, "sheets": ["07", "12"]},
    {"id": "01-DEMO-003", "phase": "01. Demolition & Site Prep", "name": "Excavate for Utilities", "hours": 24, "crew": 3, "sheets": ["06", "12"]},
    {"id": "01-DEMO-004", "phase": "01. Demolition & Site Prep", "name": "Temp Power & Water", "hours": 8, "crew": 2, "sheets": ["07"]},
    {"id": "01-DEMO-005", "phase": "01. Demolition & Site Prep", "name": "Erosion Control", "hours": 16, "crew": 2, "sheets": ["06"]},
    
    # PHASE 2: FOUNDATION (400 hours total)
    {"id": "02-FOUND-001", "phase": "02. Foundation & Concrete", "name": "Excavate Footings", "hours": 40, "crew": 3, "sheets": ["12", "13"]},
    {"id": "02-FOUND-002", "phase": "02. Foundation & Concrete", "name": "Footing Forms & Rebar", "hours": 64, "crew": 4, "sheets": ["12", "16", "17"]},
    {"id": "02-FOUND-003", "phase": "02. Foundation & Concrete", "name": "Pour Footings", "hours": 24, "crew": 5, "sheets": ["12", "01"]},
    {"id": "02-FOUND-004", "phase": "02. Foundation & Concrete", "name": "Strip Forms & Cure (7 days)", "hours": 16, "crew": 2, "sheets": ["12"]},
    {"id": "02-FOUND-005", "phase": "02. Foundation & Concrete", "name": "Stem Wall Forms & Rebar", "hours": 64, "crew": 4, "sheets": ["12", "16"]},
    {"id": "02-FOUND-006", "phase": "02. Foundation & Concrete", "name": "Pour Stem Walls", "hours": 32, "crew": 5, "sheets": ["12", "01"]},
    {"id": "02-FOUND-007", "phase": "02. Foundation & Concrete", "name": "Steel Columns & Beams", "hours": 40, "crew": 4, "sheets": ["07", "18", "19"]},
    {"id": "02-FOUND-008", "phase": "02. Foundation & Concrete", "name": "Waterproofing", "hours": 32, "crew": 2, "sheets": ["12", "01"]},
    {"id": "02-FOUND-009", "phase": "02. Foundation & Concrete", "name": "Backfill Foundation", "hours": 24, "crew": 3, "sheets": ["12"]},
    {"id": "02-FOUND-010", "phase": "02. Foundation & Concrete", "name": "Pour Slab-on-Grade", "hours": 64, "crew": 5, "sheets": ["07", "12"]},
    
    # PHASE 3: ROUGH FRAMING (800 hours total)
    {"id": "03-FRAME-001", "phase": "03. Rough Framing", "name": "Install Sill Plates", "hours": 24, "crew": 3, "sheets": ["07", "12"]},
    {"id": "03-FRAME-002", "phase": "03. Rough Framing", "name": "Floor Joists & Subfloor", "hours": 80, "crew": 4, "sheets": ["07", "15"]},
    {"id": "03-FRAME-003", "phase": "03. Rough Framing", "name": "Frame 2x8 Exterior Walls", "hours": 120, "crew": 4, "sheets": ["07", "14", "01"]},
    {"id": "03-FRAME-004", "phase": "03. Rough Framing", "name": "Frame Bedroom Walls (2 + Primary)", "hours": 64, "crew": 4, "sheets": ["07"]},
    {"id": "03-FRAME-005", "phase": "03. Rough Framing", "name": "Frame Bathroom Walls (3 total)", "hours": 48, "crew": 4, "sheets": ["07"]},
    {"id": "03-FRAME-006", "phase": "03. Rough Framing", "name": "Frame Kitchen & Laundry Walls", "hours": 56, "crew": 4, "sheets": ["07"]},
    {"id": "03-FRAME-007", "phase": "03. Rough Framing", "name": "Frame Living Areas (Great Rm, Dining, Office)", "hours": 64, "crew": 4, "sheets": ["07"]},
    {"id": "03-FRAME-008", "phase": "03. Rough Framing", "name": "Install Headers & Beams", "hours": 40, "crew": 3, "sheets": ["07", "16"]},
    {"id": "03-FRAME-009", "phase": "03. Rough Framing", "name": "Shear Wall Plywood", "hours": 56, "crew": 3, "sheets": ["14", "20", "21"]},
    {"id": "03-FRAME-010", "phase": "03. Rough Framing", "name": "Ceiling Joists (Flat Areas)", "hours": 64, "crew": 4, "sheets": ["07", "15"]},
    {"id": "03-FRAME-011", "phase": "03. Rough Framing", "name": "Coffered Ceiling Framing", "hours": 48, "crew": 3, "sheets": ["07", "10", "11"]},
    {"id": "03-FRAME-012", "phase": "03. Rough Framing", "name": "Steel Trusses", "hours": 48, "crew": 5, "sheets": ["07", "15", "18"]},
    {"id": "03-FRAME-013", "phase": "03. Rough Framing", "name": "Blocking & Fire Stops", "hours": 32, "crew": 3, "sheets": ["23"]},
    {"id": "03-FRAME-014", "phase": "03. Rough Framing", "name": "Framing Inspection", "hours": 8, "crew": 1, "sheets": ["ALL"]},
    {"id": "03-FRAME-015", "phase": "03. Rough Framing", "name": "Fix Inspection Items", "hours": 16, "crew": 2, "sheets": ["07"]},
    
    # PHASE 4: ROOF (480 hours total)
    {"id": "04-ROOF-001", "phase": "04. Roof Framing & Sheathing", "name": "Roof Trusses (Vaulted Areas)", "hours": 120, "crew": 4, "sheets": ["08", "15"]},
    {"id": "04-ROOF-002", "phase": "04. Roof Framing & Sheathing", "name": "Roof Sheathing", "hours": 80, "crew": 4, "sheets": ["08", "01"]},
    {"id": "04-ROOF-003", "phase": "04. Roof Framing & Sheathing", "name": "Underlayment & Flashing", "hours": 56, "crew": 3, "sheets": ["08"]},
    {"id": "04-ROOF-004", "phase": "04. Roof Framing & Sheathing", "name": "Patio Roof Extension", "hours": 64, "crew": 4, "sheets": ["07", "08"]},
    {"id": "04-ROOF-005", "phase": "04. Roof Framing & Sheathing", "name": "Fascia & Soffit", "hours": 72, "crew": 3, "sheets": ["08", "10", "11"]},
    {"id": "04-ROOF-006", "phase": "04. Roof Framing & Sheathing", "name": "Install Roofing", "hours": 88, "crew": 3, "sheets": ["08", "01"]},
    
    # PHASE 5: EXTERIOR (560 hours total)
    {"id": "05-EXT-001", "phase": "05. Exterior Finishes", "name": "House Wrap", "hours": 32, "crew": 3, "sheets": ["10", "11"]},
    {"id": "05-EXT-002", "phase": "05. Exterior Finishes", "name": "Install Windows", "hours": 80, "crew": 3, "sheets": ["07", "01"]},
    {"id": "05-EXT-003", "phase": "05. Exterior Finishes", "name": "Install Exterior Doors", "hours": 40, "crew": 2, "sheets": ["07", "01"]},
    {"id": "05-EXT-004", "phase": "05. Exterior Finishes", "name": "Stucco/Siding Prep", "hours": 64, "crew": 3, "sheets": ["10", "11"]},
    {"id": "05-EXT-005", "phase": "05. Exterior Finishes", "name": "Apply Stucco (3 coats)", "hours": 160, "crew": 4, "sheets": ["10", "11", "01"]},
    {"id": "05-EXT-006", "phase": "05. Exterior Finishes", "name": "Paint Exterior Trim", "hours": 64, "crew": 2, "sheets": ["10", "11"]},
    {"id": "05-EXT-007", "phase": "05. Exterior Finishes", "name": "Gutters & Downspouts", "hours": 40, "crew": 2, "sheets": ["08"]},
    {"id": "05-EXT-008", "phase": "05. Exterior Finishes", "name": "Patio Paving", "hours": 48, "crew": 3, "sheets": ["06", "07"]},
    {"id": "05-EXT-009", "phase": "05. Exterior Finishes", "name": "Exterior Inspection", "hours": 8, "crew": 1, "sheets": ["ALL"]},
    {"id": "05-EXT-010", "phase": "05. Exterior Finishes", "name": "Atrium & Fountain", "hours": 24, "crew": 2, "sheets": ["07"]},
    
    # PHASE 6: ROUGH PLUMBING (240 hours total)
    {"id": "06-PLUMB-001", "phase": "06. Rough Plumbing", "name": "Underground Drains", "hours": 40, "crew": 2, "sheets": ["07", "12"]},
    {"id": "06-PLUMB-002", "phase": "06. Rough Plumbing", "name": "Water Supply Lines", "hours": 56, "crew": 2, "sheets": ["07"]},
    {"id": "06-PLUMB-003", "phase": "06. Rough Plumbing", "name": "Water Heater Install", "hours": 16, "crew": 2, "sheets": ["07"]},
    {"id": "06-PLUMB-004", "phase": "06. Rough Plumbing", "name": "Drain Lines (3 Bathrooms)", "hours": 48, "crew": 2, "sheets": ["07"]},
    {"id": "06-PLUMB-005", "phase": "06. Rough Plumbing", "name": "Kitchen Plumbing (Island + Appliances)", "hours": 32, "crew": 2, "sheets": ["07"]},
    {"id": "06-PLUMB-006", "phase": "06. Rough Plumbing", "name": "Laundry Room Connections", "hours": 16, "crew": 2, "sheets": ["07"]},
    {"id": "06-PLUMB-007", "phase": "06. Rough Plumbing", "name": "Vent Pipes", "hours": 24, "crew": 2, "sheets": ["07", "08"]},
    {"id": "06-PLUMB-008", "phase": "06. Rough Plumbing", "name": "Pressure Test", "hours": 8, "crew": 2, "sheets": ["01"]},
    
    # PHASE 7: ROUGH ELECTRICAL (320 hours total)
    {"id": "07-ELEC-001", "phase": "07. Rough Electrical", "name": "Install Subpanel", "hours": 24, "crew": 2, "sheets": ["07"]},
    {"id": "07-ELEC-002", "phase": "07. Rough Electrical", "name": "Kitchen Circuits (7 circuits)", "hours": 56, "crew": 2, "sheets": ["07", "01"]},
    {"id": "07-ELEC-003", "phase": "07. Rough Electrical", "name": "Bathroom Circuits (GFCI)", "hours": 40, "crew": 2, "sheets": ["07"]},
    {"id": "07-ELEC-004", "phase": "07. Rough Electrical", "name": "Bedroom Circuits (3 rooms)", "hours": 48, "crew": 2, "sheets": ["07"]},
    {"id": "07-ELEC-005", "phase": "07. Rough Electrical", "name": "Living Area Circuits", "hours": 56, "crew": 2, "sheets": ["07"]},
    {"id": "07-ELEC-006", "phase": "07. Rough Electrical", "name": "Lighting Circuits", "hours": 48, "crew": 2, "sheets": ["07"]},
    {"id": "07-ELEC-007", "phase": "07. Rough Electrical", "name": "Laundry Circuits", "hours": 16, "crew": 2, "sheets": ["07"]},
    {"id": "07-ELEC-008", "phase": "07. Rough Electrical", "name": "Smoke/CO Detectors", "hours": 16, "crew": 1, "sheets": ["07", "01"]},
    {"id": "07-ELEC-009", "phase": "07. Rough Electrical", "name": "Rough Electrical Inspection", "hours": 8, "crew": 1, "sheets": ["ALL"]},
    {"id": "07-ELEC-010", "phase": "07. Rough Electrical", "name": "Fix Inspection Items", "hours": 8, "crew": 2, "sheets": ["07"]},
    
    # PHASE 8: HVAC (240 hours total)
    {"id": "08-HVAC-001", "phase": "08. HVAC Installation", "name": "Install HVAC Unit", "hours": 40, "crew": 2, "sheets": ["07", "08"]},
    {"id": "08-HVAC-002", "phase": "08. HVAC Installation", "name": "Main Trunk Lines", "hours": 48, "crew": 2, "sheets": ["07"]},
    {"id": "08-HVAC-003", "phase": "08. HVAC Installation", "name": "Branch Ducts to All Rooms", "hours": 80, "crew": 2, "sheets": ["07"]},
    {"id": "08-HVAC-004", "phase": "08. HVAC Installation", "name": "Return Air Grille", "hours": 24, "crew": 2, "sheets": ["07"]},
    {"id": "08-HVAC-005", "phase": "08. HVAC Installation", "name": "Seal & Insulate Ducts", "hours": 32, "crew": 2, "sheets": ["01"]},
    {"id": "08-HVAC-006", "phase": "08. HVAC Installation", "name": "HVAC Inspection", "hours": 8, "crew": 1, "sheets": ["ALL"]},
    {"id": "08-HVAC-007", "phase": "08. HVAC Installation", "name": "Fix Inspection Items", "hours": 8, "crew": 2, "sheets": ["07"]},
    
    # PHASE 9: INSULATION (160 hours total)
    {"id": "09-INSUL-001", "phase": "09. Insulation", "name": "Wall Insulation", "hours": 80, "crew": 3, "sheets": ["07", "01"]},
    {"id": "09-INSUL-002", "phase": "09. Insulation", "name": "Ceiling Insulation (Flat)", "hours": 40, "crew": 3, "sheets": ["07"]},
    {"id": "09-INSUL-003", "phase": "09. Insulation", "name": "Attic/Vault Insulation", "hours": 32, "crew": 3, "sheets": ["08"]},
    {"id": "09-INSUL-004", "phase": "09. Insulation", "name": "Insulation Inspection", "hours": 8, "crew": 1, "sheets": ["ALL"]},
    
    # PHASE 10: DRYWALL (560 hours total)
    {"id": "10-DRY-001", "phase": "10. Drywall", "name": "Hang Drywall - Ceilings", "hours": 120, "crew": 4, "sheets": ["07"]},
    {"id": "10-DRY-002", "phase": "10. Drywall", "name": "Hang Drywall - Walls", "hours": 160, "crew": 4, "sheets": ["07"]},
    {"id": "10-DRY-003", "phase": "10. Drywall", "name": "Coffered Ceiling Drywall", "hours": 32, "crew": 3, "sheets": ["07"]},
    {"id": "10-DRY-004", "phase": "10. Drywall", "name": "Tape & Mud (1st coat)", "hours": 80, "crew": 3, "sheets": ["07"]},
    {"id": "10-DRY-005", "phase": "10. Drywall", "name": "Tape & Mud (2nd coat)", "hours": 64, "crew": 3, "sheets": ["07"]},
    {"id": "10-DRY-006", "phase": "10. Drywall", "name": "Tape & Mud (3rd coat)", "hours": 48, "crew": 3, "sheets": ["07"]},
    {"id": "10-DRY-007", "phase": "10. Drywall", "name": "Sand Drywall", "hours": 48, "crew": 3, "sheets": ["07"]},
    {"id": "10-DRY-008", "phase": "10. Drywall", "name": "Texture Ceilings", "hours": 8, "crew": 2, "sheets": ["07"]},
    
    # PHASE 11: INTERIOR TRIM (400 hours total)
    {"id": "11-TRIM-001", "phase": "11. Interior Trim & Doors", "name": "Install Interior Doors", "hours": 80, "crew": 2, "sheets": ["07", "01"]},
    {"id": "11-TRIM-002", "phase": "11. Interior Trim & Doors", "name": "Baseboard All Rooms", "hours": 120, "crew": 3, "sheets": ["07"]},
    {"id": "11-TRIM-003", "phase": "11. Interior Trim & Doors", "name": "Crown Molding", "hours": 80, "crew": 2, "sheets": ["07"]},
    {"id": "11-TRIM-004", "phase": "11. Interior Trim & Doors", "name": "Window Casing", "hours": 64, "crew": 2, "sheets": ["07"]},
    {"id": "11-TRIM-005", "phase": "11. Interior Trim & Doors", "name": "Closet Systems", "hours": 40, "crew": 2, "sheets": ["07"]},
    {"id": "11-TRIM-006", "phase": "11. Interior Trim & Doors", "name": "Shelving & Built-ins", "hours": 16, "crew": 2, "sheets": ["07"]},
    
    # PHASE 12: FLOORING (320 hours total)
    {"id": "12-FLOOR-001", "phase": "12. Flooring", "name": "Tile Bathroom Floors (3)", "hours": 64, "crew": 2, "sheets": ["07"]},
    {"id": "12-FLOOR-002", "phase": "12. Flooring", "name": "Tile Bathroom Showers (2)", "hours": 80, "crew": 2, "sheets": ["07"]},
    {"id": "12-FLOOR-003", "phase": "12. Flooring", "name": "Kitchen Floor", "hours": 40, "crew": 2, "sheets": ["07"]},
    {"id": "12-FLOOR-004", "phase": "12. Flooring", "name": "Laundry Room Floor", "hours": 16, "crew": 2, "sheets": ["07"]},
    {"id": "12-FLOOR-005", "phase": "12. Flooring", "name": "Hardwood/LVP Living Areas", "hours": 80, "crew": 3, "sheets": ["07"]},
    {"id": "12-FLOOR-006", "phase": "12. Flooring", "name": "Carpet Bedrooms", "hours": 40, "crew": 2, "sheets": ["07"]},
    
    # PHASE 13: KITCHEN (240 hours total)
    {"id": "13-KITCH-001", "phase": "13. Kitchen Installation", "name": "Install Base Cabinets", "hours": 48, "crew": 3, "sheets": ["07"]},
    {"id": "13-KITCH-002", "phase": "13. Kitchen Installation", "name": "Install Wall Cabinets", "hours": 40, "crew": 3, "sheets": ["07"]},
    {"id": "13-KITCH-003", "phase": "13. Kitchen Installation", "name": "Build Tim's Island", "hours": 40, "crew": 3, "sheets": ["07"]},
    {"id": "13-KITCH-004", "phase": "13. Kitchen Installation", "name": "Install Countertops", "hours": 32, "crew": 2, "sheets": ["07"]},
    {"id": "13-KITCH-005", "phase": "13. Kitchen Installation", "name": "Install Sink & Faucet", "hours": 16, "crew": 2, "sheets": ["07"]},
    {"id": "13-KITCH-006", "phase": "13. Kitchen Installation", "name": "Install Appliances (Range, D/W, etc)", "hours": 40, "crew": 2, "sheets": ["07"]},
    {"id": "13-KITCH-007", "phase": "13. Kitchen Installation", "name": "Backsplash Tile", "hours": 24, "crew": 2, "sheets": ["07"]},
    
    # PHASE 14: BATHROOM FINISHES (280 hours total)
    {"id": "14-BATH-001", "phase": "14. Bathroom Finishes", "name": "Install Vanities (4 total)", "hours": 40, "crew": 2, "sheets": ["07"]},
    {"id": "14-BATH-002", "phase": "14. Bathroom Finishes", "name": "Install K-3324 Toilets (3)", "hours": 24, "crew": 2, "sheets": ["07", "01"]},
    {"id": "14-BATH-003", "phase": "14. Bathroom Finishes", "name": "Install Shower Fixtures", "hours": 40, "crew": 2, "sheets": ["07"]},
    {"id": "14-BATH-004", "phase": "14. Bathroom Finishes", "name": "Install Shower Doors", "hours": 32, "crew": 2, "sheets": ["07"]},
    {"id": "14-BATH-005", "phase": "14. Bathroom Finishes", "name": "Mirrors & Accessories", "hours": 24, "crew": 2, "sheets": ["07"]},
    {"id": "14-BATH-006", "phase": "14. Bathroom Finishes", "name": "Test All Fixtures", "hours": 8, "crew": 2, "sheets": ["07"]},
    
    # PHASE 15: PAINT (400 hours total)
    {"id": "15-PAINT-001", "phase": "15. Paint", "name": "Prime All Walls", "hours": 80, "crew": 3, "sheets": ["07"]},
    {"id": "15-PAINT-002", "phase": "15. Paint", "name": "Paint Walls (2 coats)", "hours": 160, "crew": 3, "sheets": ["07"]},
    {"id": "15-PAINT-003", "phase": "15. Paint", "name": "Paint Ceilings", "hours": 80, "crew": 3, "sheets": ["07"]},
    {"id": "15-PAINT-004", "phase": "15. Paint", "name": "Paint Trim", "hours": 64, "crew": 2, "sheets": ["07"]},
    {"id": "15-PAINT-005", "phase": "15. Paint", "name": "Touch-ups", "hours": 16, "crew": 2, "sheets": ["07"]},
    
    # PHASE 16: FINAL (200 hours total)
    {"id": "16-FINAL-001", "phase": "16. Final Electrical & Plumbing", "name": "Install Light Fixtures", "hours": 48, "crew": 2, "sheets": ["07"]},
    {"id": "16-FINAL-002", "phase": "16. Final Electrical & Plumbing", "name": "Install Outlets & Switches", "hours": 40, "crew": 2, "sheets": ["07"]},
    {"id": "16-FINAL-003", "phase": "16. Final Electrical & Plumbing", "name": "Install Cover Plates", "hours": 16, "crew": 1, "sheets": ["07"]},
    {"id": "16-FINAL-004", "phase": "16. Final Electrical & Plumbing", "name": "Test All Electrical", "hours": 16, "crew": 2, "sheets": ["ALL"]},
    {"id": "16-FINAL-005", "phase": "16. Final Electrical & Plumbing", "name": "Final Plumbing Connections", "hours": 24, "crew": 2, "sheets": ["07"]},
    {"id": "16-FINAL-006", "phase": "16. Final Electrical & Plumbing", "name": "Final Electrical Inspection", "hours": 8, "crew": 1, "sheets": ["ALL"]},
    {"id": "16-FINAL-007", "phase": "16. Final Electrical & Plumbing", "name": "Final Plumbing Inspection", "hours": 8, "crew": 1, "sheets": ["ALL"]},
    {"id": "16-FINAL-008", "phase": "16. Final Electrical & Plumbing", "name": "Final Building Inspection", "hours": 8, "crew": 1, "sheets": ["ALL"]},
    {"id": "16-FINAL-009", "phase": "16. Final Electrical & Plumbing", "name": "Cleanup & Punchlist", "hours": 32, "crew": 4, "sheets": ["ALL"]},
]

def calculate_schedule(tasks, crew_size=7, hours_per_day=8):
    """Calculate realistic schedule."""
    start_date = datetime(2025, 10, 27)
    current_date = start_date
    
    scheduled = []
    for task in tasks:
        # Skip weekends
        while current_date.weekday() >= 5:
            current_date += timedelta(days=1)
        
        effective_crew = min(task['crew'], crew_size)
        daily_hours = effective_crew * hours_per_day
        days_needed = max(0.5, round((task['hours'] / daily_hours) * 2) / 2)
        
        end_date = current_date
        days_counted = 0
        while days_counted < days_needed:
            end_date += timedelta(days=1)
            if end_date.weekday() < 5:
                days_counted += 1
        
        scheduled.append({
            'id': task['id'],
            'phase': task['phase'],
            'name': task['name'],
            'duration_hours': task['hours'],
            'crew_size': task['crew'],
            'crew_assigned': effective_crew,
            'days': days_needed,
            'start_date': current_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'blueprint_pages': [{'sheet_num': s} for s in task['sheets']],
            'from_plans': f"Sheets {', '.join(task['sheets'])}"
        })
        
        current_date = end_date
    
    return scheduled

def main():
    print("🏗️ Generating COMPLETE Construction Plan")
    print("=" * 80)
    
    scheduled = calculate_schedule(ALL_TASKS)
    total_hours = sum(t['hours'] for t in ALL_TASKS)
    total_days = sum(t['days'] for t in scheduled)
    
    output = {
        'project': PROJECT_DATA,
        'tasks': scheduled,
        'summary': {
            'total_tasks': len(ALL_TASKS),
            'total_hours': total_hours,
            'total_days': total_days,
            'weeks': round(total_days / 5, 1),
            'months': round(total_days / 21.7, 1),
        }
    }
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_DIR / 'real_construction_plan.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"✅ {len(ALL_TASKS)} detailed tasks")
    print(f"⏱️  {total_hours:,} total hours")
    print(f"📅 {total_days:.1f} working days ({output['summary']['weeks']} weeks / {output['summary']['months']} months)")
    print(f"📅 {scheduled[0]['start_date']} to {scheduled[-1]['end_date']}")
    print(f"📁 Saved: {OUTPUT_DIR / 'real_construction_plan.json'}")

if __name__ == "__main__":
    main()

