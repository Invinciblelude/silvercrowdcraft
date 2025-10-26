#!/usr/bin/env python3
"""
Generate REAL construction plan based on actual 728 Cortlandt Drive blueprints.
This extracts specific dimensions, materials, and requirements from the plans.
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

OUTPUT_DIR = Path("/Users/invinciblelude/728 Cordant project/docs/assets")
SOPS_DIR = Path("/Users/invinciblelude/728 Cordant project/docs/sops")

# REAL PROJECT DATA FROM BLUEPRINTS
PROJECT_DATA = {
    "name": "728 Cortlandt Drive Addition",
    "address": "728 Cortlandt Drive, Sacramento, CA 95864",
    "parcel": "292-0162-010-0000",
    "architect": "Eric Knutson",
    "permit_date": "6/1/2025",
    "existing_sf": 2611,
    "new_addition_sf": 3200,
    "total_sf": 5811,
    "construction_type": "Single Family Residential Addition",
    "scope": "3,200 SF addition including: Primary Suite, 2 Bedrooms, 2 Baths, Kitchen, Great Room, Dining Room, Office, Laundry Room, Entry, and covered patio"
}

# REAL CONSTRUCTION TASKS FROM BLUEPRINTS
REAL_TASKS = [
    {
        "id": "DEMO-001",
        "phase": "Demolition & Site Prep",
        "name": "Demolish Existing Wood Fences",
        "description": "Remove existing wood fencing as shown on plans to clear for new addition",
        "duration_hours": 8,
        "crew_size": 2,
        "from_plans": "Page 8 (A1.01) - Floor Plan shows 'DEMO. (E) WD. FENCE' in three locations",
        "materials": [
            "Dumpster (10-yard)",
            "Hand tools for demolition"
        ],
        "steps": [
            "Verify fence locations marked on plan match field conditions",
            "Remove three sections of existing wood fence as shown",
            "Load debris into dumpster",
            "Clear and grade area for new construction",
            "Verify property lines before proceeding"
        ],
        "qc_checks": [
            "All marked fencing removed",
            "Area cleared of debris",
            "No damage to existing structures to remain"
        ],
        "related_drawings": ["A1.01 Proposed Floor Plan"]
    },
    {
        "id": "FOUND-001",
        "phase": "Foundation",
        "name": "Layout & Excavation for 3,200 SF Addition",
        "description": "Excavate for foundation footings of new 3,200 SF addition per structural plans",
        "duration_hours": 24,
        "crew_size": 3,
        "from_plans": "3,200 SF conditioned area addition shown on Floor Plan (A1.01)",
        "materials": [
            "String lines and stakes",
            "Marking paint",
            "Excavator rental",
            "Gravel for footing base (if required by soils report)"
        ],
        "dimensions": {
            "addition_size": "3,200 SF",
            "existing_to_remain": "2,611 SF",
            "total_project": "5,811 SF"
        },
        "steps": [
            "Call 811 for utility locates (48-72 hours advance)",
            "Stake out addition footprint per dimensioned floor plan",
            "Verify all dimensions from floor plan (primary bedroom, bedroom 2: 11'-6\" x 12', bedroom 3: 11'-6\" x 12', etc.)",
            "Excavate for continuous footings around perimeter",
            "Excavate for interior foundation walls",
            "Dig trenches for new utilities (water, sewer, electrical conduits)",
            "Compact subgrade to 95%",
            "Install gravel base if required"
        ],
        "qc_checks": [
            "Layout dimensions match floor plan within ±1 inch",
            "Footing trenches are level and at correct depth",
            "Subgrade is compacted (visual test: no soft spots)",
            "All utilities located and marked"
        ],
        "inspections": ["Foundation layout inspection before concrete"],
        "related_drawings": ["A1.01 Proposed Floor Plan", "Structural Foundation Plan"]
    },
    {
        "id": "FOUND-002",
        "phase": "Foundation",
        "name": "Install Steel Columns & Beams",
        "description": "Install new steel columns and steel truss system as shown on structural plans",
        "duration_hours": 16,
        "crew_size": 4,
        "from_plans": "Floor plan shows '(N) STEEL COLUMN- TYP.', '(N) STEEL TRUSS- SEE ALSO STRUCTURAL', '(N) STEEL BM. EXTENSION TO MATCH (E)'",
        "materials": [
            "Steel columns (size and quantity per structural plans)",
            "Steel beams/trusses (per structural engineer)",
            "Anchor bolts and base plates",
            "Welding equipment (if field welding required)",
            "Crane or telehandler for setting"
        ],
        "steps": [
            "Review structural plans for steel member sizes and locations",
            "Set column base plates and anchor bolts in wet concrete (coordinate with foundation pour)",
            "Allow concrete to cure minimum 7 days",
            "Set steel columns plumb and brace temporarily",
            "Crane steel beams/truss into place",
            "Bolt or weld connections per structural details",
            "Apply rust-preventative paint to all steel",
            "Verify alignment with floor plan dimensions"
        ],
        "qc_checks": [
            "All columns are plumb (within 1/4 inch per 10 feet)",
            "Beam elevations match structural plans",
            "All connections are tight and properly fastened",
            "Steel members match specified sizes on plans"
        ],
        "inspections": ["Structural steel inspection before framing"],
        "related_drawings": ["A1.01 Floor Plan", "Structural Plans", "Steel Details"]
    },
    {
        "id": "FRAME-001",
        "phase": "Framing",
        "name": "Frame 2x8 Exterior Walls",
        "description": "Frame new 2x8 exterior walls per floor plan notation",
        "duration_hours": 40,
        "crew_size": 4,
        "from_plans": "Floor plan shows '(N) 2x8 WALL- SEE STRUCT.- TYP.'",
        "materials": [
            "2x8 studs (quantity per takeoff)",
            "2x8 top plates (double)",
            "2x8 bottom plates (pressure-treated where on concrete)",
            "16d nails or framing screws",
            "Hurricane ties/straps",
            "Sheathing (OSB or plywood per code)",
            "House wrap"
        ],
        "steps": [
            "Snap chalk lines on slab/floor deck for wall locations",
            "Install pressure-treated 2x8 bottom plates",
            "Cut 2x8 studs to height (typically 92-5/8\" for 8' ceiling)",
            "Frame walls flat on deck, then raise and brace",
            "Install double 2x8 top plates (lap at corners minimum 4')",
            "Frame window and door openings per floor plan dimensions",
            "Install headers sized per span tables",
            "Sheath exterior walls with OSB/plywood",
            "Apply house wrap over sheathing"
        ],
        "qc_checks": [
            "Walls are plumb (check every 10 feet)",
            "All studs are 2x8 as specified (not 2x6)",
            "Stud spacing is 16\" O.C. unless noted otherwise",
            "Wall layout matches floor plan dimensions",
            "All openings match window/door schedule"
        ],
        "inspections": ["Framing inspection before insulation"],
        "related_drawings": ["A1.01 Floor Plan", "Structural Plans", "Wall Sections"]
    },
    {
        "id": "FRAME-002",
        "phase": "Framing",
        "name": "Frame Interior Partition Walls",
        "description": "Frame all interior walls to create rooms per floor plan",
        "duration_hours": 32,
        "crew_size": 4,
        "from_plans": "Floor plan shows all room layouts with dimensions",
        "room_dimensions": {
            "Bedroom 2": "11'-6\" x 12'",
            "Bedroom 3": "11'-6\" x 12'",
            "Primary Bedroom": "Per plan (vaulted ceiling)",
            "Primary Bath": "Per plan (flat ceiling)",
            "Bath 2": "Per plan (flat ceiling)",
            "Powder Room": "Per plan",
            "Kitchen": "Per plan (vaulted ceiling)",
            "Kitchen Lounge": "Per plan (coffered ceiling)",
            "Great Room": "Per plan (vaulted ceiling)",
            "Dining Room": "Per plan (coffered ceiling)",
            "Office": "Per plan (vaulted ceiling)",
            "Laundry Room": "Per plan",
            "Entry": "Per plan",
            "Halls": "Various (flat ceilings)"
        },
        "materials": [
            "2x4 studs for interior walls",
            "2x4 plates (top and bottom)",
            "16d nails or screws",
            "Sound insulation (between bedrooms/baths)"
        ],
        "steps": [
            "Snap chalk lines for all interior walls per floor plan",
            "Frame walls to create each room per dimensions above",
            "Verify bedroom sizes: Bedroom 2 = 11'-6\" x 12', Bedroom 3 = 11'-6\" x 12'",
            "Frame closet walls as shown",
            "Install backing for cabinets and fixtures (kitchen, baths)",
            "Frame soffit areas for coffered ceilings (dining room, kitchen lounge)",
            "Provide clearance for plumbing vents in wall cavities",
            "Install fire blocking at mid-height per code"
        ],
        "qc_checks": [
            "All room dimensions match floor plan (±1/2 inch tolerance)",
            "Walls are straight and plumb",
            "Door openings are sized correctly for specified doors",
            "Backing installed for all cabinets and grab bars"
        ],
        "inspections": ["Framing inspection"],
        "related_drawings": ["A1.01 Floor Plan"]
    },
    {
        "id": "ROOF-001",
        "phase": "Roofing",
        "name": "Frame Roof - Vaulted & Flat Ceilings",
        "description": "Frame roof with vaulted ceilings (Great Room, Bedrooms, Kitchen, Office) and flat ceilings (Baths, Halls, Laundry)",
        "duration_hours": 48,
        "crew_size": 4,
        "from_plans": "Floor plan indicates 'VOL. CEIL.' for Great Room, Primary Bedroom, Bedrooms 2 & 3, Kitchen, Office. 'FLAT CEIL.' for Baths and Halls. 'COFFERED CEIL.' for Dining Room and Kitchen Lounge",
        "ceiling_types": {
            "Vaulted": ["Great Room", "Primary Bedroom", "Bedroom 2", "Bedroom 3", "Kitchen", "Office"],
            "Flat": ["Primary Bath", "Bath 2", "Powder Room", "Halls", "Laundry Room", "Back Entry Hall"],
            "Coffered": ["Dining Room", "Kitchen Lounge"]
        },
        "materials": [
            "Roof trusses or rafters (per structural plans)",
            "Ceiling joists for flat ceiling areas",
            "Framing for coffered ceiling details",
            "2x blocking and nailers",
            "Hurricane ties",
            "Roof sheathing (OSB or plywood)",
            "Roofing felt or synthetic underlayment"
        ],
        "steps": [
            "Crane or hand-set roof trusses per structural plan spacing",
            "Install ceiling joists in flat ceiling areas",
            "Frame coffered ceiling recesses in dining room and kitchen lounge",
            "Ensure vaulted ceiling areas have proper ventilation paths",
            "Install roof sheathing (typically 7/16\" or 1/2\" OSB)",
            "Apply roofing underlayment",
            "Install drip edge at eaves and rakes",
            "Frame patio roof extension to match existing"
        ],
        "qc_checks": [
            "Roof pitch matches existing structure",
            "All vaulted ceiling areas are framed per plan",
            "Flat ceiling areas are level",
            "Coffered ceiling details match architectural intent",
            "Roof sheathing is nailed per code (6\" edges, 12\" field)"
        ],
        "inspections": ["Roof framing inspection"],
        "related_drawings": ["A1.01 Floor Plan", "A1.02 Roof Plan", "Roof framing plan"]
    },
    {
        "id": "PLUMB-001",
        "phase": "Plumbing",
        "name": "Install Plumbing Rough-In",
        "description": "Rough-in all plumbing for bathrooms, kitchen, and laundry room per floor plan",
        "duration_hours": 40,
        "crew_size": 2,
        "from_plans": "Floor plan shows 3 bathrooms (Primary Bath, Bath 2, Powder Room), Kitchen with island, and Laundry Room",
        "fixtures_count": {
            "Toilets": "3 (K-3324 Kathryn Vitreous China per plan)",
            "Sinks": "Multiple (Kitchen: island sink + bar sink, Primary Bath: 2 sinks, Bath 2: sink, Powder Room: sink)",
            "Showers": "2 (Primary Bath: W. SHOW., Bath 2)",
            "Kitchen appliances": "Dishwasher, Ice Maker, Range",
            "Laundry": "Washer connections"
        },
        "materials": [
            "PEX or copper supply lines",
            "PVC drain lines (3\", 2\", 1-1/2\")",
            "Vent pipes",
            "Shut-off valves for each fixture",
            "Water heater (size TBD based on fixture count)",
            "Drain assemblies for all fixtures",
            "Rough-in boxes for shower valves"
        ],
        "steps": [
            "Run main water line from meter to water heater location",
            "Install water heater",
            "Run hot and cold supply lines to all fixture locations per floor plan",
            "Stub out supplies for: 3 toilets, multiple sinks, 2 showers, dishwasher, ice maker, washing machine",
            "Install drain lines: 3\" main drains, 2\" for showers/tubs, 1-1/2\" for sinks",
            "Install vent pipes for all drains (up through roof)",
            "Rough-in kitchen island plumbing (sink and dishwasher)",
            "Install laundry room connections (hot, cold, drain)",
            "Pressure test all supply lines (50 PSI for 24 hours)"
        ],
        "qc_checks": [
            "All fixtures have hot and cold supplies",
            "Toilet rough-ins are 12\" from wall",
            "Shower valve heights are 48\" AFF (typical)",
            "All drains have proper slope (1/4\" per foot minimum)",
            "No leaks in pressure test"
        ],
        "inspections": ["Plumbing rough-in inspection"],
        "related_drawings": ["A1.01 Floor Plan", "Plumbing Plans"]
    },
    {
        "id": "ELEC-001",
        "phase": "Electrical",
        "name": "Install Electrical Rough-In & Subpanel",
        "description": "Install new electrical subpanel and all circuits for addition",
        "duration_hours": 48,
        "crew_size": 2,
        "from_plans": "Floor plan shows '(N) ELECT. SUBPANEL' location",
        "materials": [
            "Electrical subpanel (size per load calc, typically 100A or 150A)",
            "Romex cable (12/2, 14/2, 14/3)",
            "Electrical boxes (outlets, switches, ceiling fixtures)",
            "Circuit breakers",
            "Conduit for subpanel feed",
            "Grounding electrodes"
        ],
        "circuits_required": {
            "Kitchen": "2 x 20A small appliance circuits, 1 x 20A refrigerator, 1 x 50A range, 1 x 20A dishwasher, 1 x 15A disposal, 1 x 20A microwave",
            "Bathrooms": "2 x 20A GFCI circuits (Primary Bath, Bath 2/Powder)",
            "Laundry": "1 x 20A washer, 1 x 30A dryer (if electric)",
            "Bedrooms": "1 x 15A per bedroom (3 total)",
            "Living areas": "Multiple 15A or 20A general lighting circuits",
            "HVAC": "Dedicated circuits per equipment"
        },
        "steps": [
            "Install subpanel at location shown on floor plan",
            "Run feeder from main panel to subpanel",
            "Install outlet boxes: bedrooms (minimum 1 per 12' of wall), kitchen (every 4' counter), baths (GFCI required)",
            "Install switch boxes for all lights (per reflected ceiling plan)",
            "Run circuits for kitchen appliances (range, dishwasher, disposal, microwave, refrigerator)",
            "Install dedicated 20A bathroom circuits with GFCI protection",
            "Run laundry room circuits",
            "Install smoke detectors (interconnected, per code)",
            "Label all circuits clearly at subpanel"
        ],
        "qc_checks": [
            "All boxes are securely fastened",
            "Cable is stapled within 8\" of boxes and every 4' along run",
            "Proper wire size for circuit amperage (12 AWG for 20A, 14 AWG for 15A)",
            "GFCI protection in all required locations (baths, kitchen counters, laundry)",
            "Subpanel is properly grounded"
        ],
        "inspections": ["Electrical rough-in inspection"],
        "related_drawings": ["A1.01 Floor Plan", "Electrical Plans"]
    },
    {
        "id": "FINISH-001",
        "phase": "Finish Work",
        "name": "Install Kitchen per Plan",
        "description": "Install complete kitchen with island, appliances, and fixtures per floor plan",
        "duration_hours": 32,
        "crew_size": 3,
        "from_plans": "Floor plan shows detailed kitchen layout with island dimensions and appliance locations",
        "kitchen_features": {
            "Island": "Tim's Island (per plan) with sink",
            "Appliances": "Range, Dishwasher, Microwave above/Oven below, Refrigerator, Freezer, Ice Maker",
            "Cabinets": "Pantry, Wine Cabinet, Drink Cabinet, Trash/Recycle Pull-outs",
            "Counters": "Per plan dimensions (specific measurements shown on floor plan)"
        },
        "materials": [
            "Kitchen cabinets (per cabinet schedule)",
            "Countertops (material TBD)",
            "Kitchen island (custom or pre-made)",
            "Appliances: Range, D/W, Microwave, Oven, Refer., Freezer, Ice Maker",
            "Kitchen sink and faucet",
            "Cabinet hardware"
        ],
        "steps": [
            "Install base cabinets following floor plan layout",
            "Install pantry cabinets",
            "Install wine cabinet, drink cabinet per plan",
            "Install trash/recycle pull-outs (location shown on plan)",
            "Set 'Tim's Island' in position per dimensions on plan",
            "Install countertops (field measure and order)",
            "Cut sink opening in island",
            "Install sink and plumbing connections",
            "Set appliances: Range, Dishwasher, Microwave/Oven combo, Refrigerator, Freezer, Ice Maker",
            "Connect all appliances to electrical and plumbing rough-ins",
            "Install upper cabinets (if any)",
            "Install cabinet hardware"
        ],
        "qc_checks": [
            "All cabinet dimensions match floor plan",
            "Island is level and secure",
            "All appliances fit in designated spaces",
            "Plumbing connections are leak-free",
            "Electrical connections are proper (no extension cords)",
            "All drawers and doors operate smoothly"
        ],
        "inspections": ["Final inspection (kitchen included)"],
        "related_drawings": ["A1.01 Floor Plan", "Kitchen elevations (if provided)"]
    },
    {
        "id": "FINISH-002",
        "phase": "Finish Work",
        "name": "Install Bathroom Fixtures",
        "description": "Install all bathroom fixtures including specified K-3324 Kathryn toilets",
        "duration_hours": 24,
        "crew_size": 2,
        "from_plans": "Floor plan specifies 'K-3324 KATHRYN TOILET VITREOUS CHINA' for all 3 bathrooms",
        "fixtures": {
            "Primary Bath": "2 sinks, 1 K-3324 toilet, walk-in shower (W. SHOW.)",
            "Bath 2": "1 sink, 1 K-3324 toilet, shower (W.C. 2)",
            "Powder Room": "1 sink, 1 K-3324 toilet (W.C.)"
        },
        "materials": [
            "K-3324 Kathryn toilets (3 units - exact model specified on plans)",
            "Bathroom sinks and faucets (4 total: 2 in Primary Bath, 1 in Bath 2, 1 in Powder)",
            "Shower fixtures (2 sets)",
            "Wax rings and toilet mounting hardware",
            "Sink drains and P-traps",
            "Shower doors or curtain rods",
            "Caulk and plumber's putty"
        ],
        "from_plans": "Floor plan specifies K-3324 Kathryn toilet model for all 3 bathrooms",
        "steps": [
            "Install bathroom vanities per locations on floor plan",
            "Set sinks and connect faucets",
            "Install all 3 K-3324 Kathryn toilets (verify model number before ordering)",
            "Connect toilets to water supply and drain",
            "Install shower valves and trim (Primary Bath and Bath 2)",
            "Install shower heads and fixtures",
            "Tile showers (if not done earlier)",
            "Install shower doors",
            "Caulk all fixtures",
            "Test all fixtures for leaks"
        ],
        "qc_checks": [
            "All 3 toilets are K-3324 Kathryn model as specified",
            "No leaks at any connection",
            "Toilets flush properly",
            "Shower drains properly",
            "All fixtures are level and secure"
        ],
        "inspections": ["Final plumbing inspection"],
        "related_drawings": ["A1.01 Floor Plan", "Plumbing fixture schedule"]
    }
]

def calculate_schedule(tasks, crew_size=7, hours_per_day=8, days_per_week=5):
    """Calculate project schedule based on crew size and work hours."""
    start_date = datetime(2025, 10, 27)  # Start date
    current_date = start_date
    
    schedule = []
    
    for task in tasks:
        # Calculate days needed
        task_hours = task['duration_hours']
        effective_crew = min(task['crew_size'], crew_size)  # Can't use more crew than task requires
        daily_hours = effective_crew * hours_per_day
        days_needed = (task_hours / daily_hours)
        
        # Round up to nearest half day
        days_needed = round(days_needed * 2) / 2
        
        # Skip weekends
        while current_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
            current_date += timedelta(days=1)
        
        end_date = current_date
        days_added = 0
        while days_added < days_needed:
            end_date += timedelta(days=1)
            if end_date.weekday() < 5:  # Only count weekdays
                days_added += 1
        
        schedule.append({
            **task,
            'start_date': current_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'days': days_needed,
            'crew_assigned': effective_crew
        })
        
        current_date = end_date
    
    return schedule

def main():
    print("🏗️ Generating REAL Construction Plan for 728 Cortlandt Drive")
    print("=" * 80)
    
    # Calculate schedule
    scheduled_tasks = calculate_schedule(REAL_TASKS, crew_size=7, hours_per_day=8)
    
    # Summary
    total_hours = sum(t['duration_hours'] for t in REAL_TASKS)
    total_days = sum(t['days'] for t in scheduled_tasks)
    
    output = {
        'project': PROJECT_DATA,
        'tasks': scheduled_tasks,
        'summary': {
            'total_tasks': len(REAL_TASKS),
            'total_hours': total_hours,
            'total_working_days': total_days,
            'estimated_weeks': round(total_days / 5, 1),
            'crew_size': 7,
            'work_schedule': 'Monday-Friday, 7:30 AM - 4:00 PM (8 hours/day)',
            'project_start': scheduled_tasks[0]['start_date'],
            'project_end': scheduled_tasks[-1]['end_date']
        }
    }
    
    # Save to JSON
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_DIR / 'real_construction_plan.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"✅ Generated {len(REAL_TASKS)} tasks based on actual blueprints")
    print(f"📊 Total estimated hours: {total_hours}")
    print(f"📅 Total working days: {total_days}")
    print(f"📅 Estimated duration: {round(total_days / 5, 1)} weeks")
    print(f"📅 Project start: {scheduled_tasks[0]['start_date']}")
    print(f"📅 Project end: {scheduled_tasks[-1]['end_date']}")
    print(f"\n📁 Saved to: {OUTPUT_DIR / 'real_construction_plan.json'}")
    
    # Print task breakdown
    print("\n📋 TASK BREAKDOWN:")
    for task in scheduled_tasks:
        print(f"  {task['id']}: {task['name']}")
        print(f"     Duration: {task['days']} days | Crew: {task['crew_assigned']} | {task['start_date']} to {task['end_date']}")

if __name__ == "__main__":
    main()

