#!/usr/bin/env python3
"""
Generate comprehensive task list with detailed SOPs for 728 Cortlandt project.
Each task includes: materials, tools, safety, step-by-step instructions, QC checks.
"""

import json
from pathlib import Path

BLUEPRINT_DATA = Path("/Users/invinciblelude/728 Cordant project/docs/assets/blueprint_data.json")
OUTPUT_TASKS = Path("/Users/invinciblelude/728 Cordant project/docs/assets/project_tasks.json")
OUTPUT_SOPS = Path("/Users/invinciblelude/728 Cordant project/docs/sops")

# Comprehensive construction task database
CONSTRUCTION_TASKS = {
    "Site & Civil": [
        {
            "id": "SITE-001",
            "name": "Site Survey & Layout",
            "trade": "Site & Civil",
            "duration_hours": 8,
            "crew_size": 2,
            "prerequisites": ["Permits approved", "Property corners identified"],
            "materials": ["Wooden stakes", "String line", "Marking paint", "Rebar markers"],
            "tools": ["Transit/Level", "Measuring tape (100ft)", "Sledgehammer", "Plumb bob"],
            "safety": ["High-vis vest", "Steel-toe boots", "Hard hat", "Traffic cones if near road"],
            "steps": [
                "Review site plan and locate property corners using survey markers",
                "Set up transit at benchmark elevation",
                "Drive corner stakes at building footprint corners per plan dimensions",
                "Run string lines between corner stakes to establish building outline",
                "Mark foundation excavation lines 2ft beyond building footprint",
                "Mark utility trenches (water, sewer, electric) per civil plans",
                "Spray paint all excavation boundaries with bright color",
                "Photograph staked layout for record"
            ],
            "qc_checks": [
                "Building corners are square (3-4-5 method or diagonal measurement)",
                "All dimensions match site plan within ±1 inch",
                "Elevation benchmarks established and recorded",
                "Photo documentation complete"
            ],
            "inspections": ["Layout approved by GC before excavation"],
            "related_sheets": ["Site & Civil"]
        },
        {
            "id": "SITE-002",
            "name": "Excavation & Grading",
            "trade": "Site & Civil",
            "duration_hours": 16,
            "crew_size": 1,
            "prerequisites": ["Layout complete", "Call 811 (utilities marked)", "Excavation permit"],
            "materials": ["None (equipment-based)"],
            "tools": ["Excavator", "Grading blade", "Compactor", "Hand shovels for cleanup"],
            "safety": ["Hard hat", "High-vis vest", "Excavation shoring if depth >4ft", "Keep personnel away from equipment"],
            "steps": [
                "Call 811 at least 2 days prior to confirm underground utilities marked",
                "Excavate to depth specified on foundation plan (typically 12-18 inches below grade for footing)",
                "Ensure bottom of excavation is level and compacted",
                "Remove any loose soil, roots, or organic material from bottom",
                "Compact subgrade with mechanical compactor (minimum 95% compaction)",
                "Grade site for drainage away from foundation (2% slope minimum)",
                "Stockpile topsoil for later landscaping use"
            ],
            "qc_checks": [
                "Excavation depth matches foundation plan",
                "Bottom is level and compacted (no soft spots)",
                "No underground utilities damaged",
                "Subgrade passes compaction test"
            ],
            "inspections": ["Footing trench inspection before concrete"],
            "related_sheets": ["Site & Civil", "Foundation"]
        }
    ],
    "Foundation": [
        {
            "id": "FOUND-001",
            "name": "Footing Forms & Rebar",
            "trade": "Foundation",
            "duration_hours": 24,
            "crew_size": 3,
            "prerequisites": ["Excavation complete", "Soil compaction test passed"],
            "materials": [
                "2x10 or 2x12 lumber for forms",
                "#4 rebar (per structural plan)",
                "Rebar chairs (2-3 inch)",
                "Form stakes (2x4)",
                "Duplex nails",
                "Tie wire",
                "Form release agent"
            ],
            "tools": ["Circular saw", "Hammer", "Level (4ft)", "Rebar cutter", "Measuring tape", "String line"],
            "safety": ["Cut-resistant gloves (rebar has sharp ends)", "Steel-toe boots", "Eye protection", "Hard hat"],
            "steps": [
                "Set bottom of footing forms to elevation per plan",
                "Install and brace 2x10/2x12 form boards using 2x4 stakes every 4ft",
                "Ensure forms are level and dimension matches plan (typically 12-24 inch width)",
                "Apply form release agent to inside of forms",
                "Cut and place #4 rebar per structural plan spacing (typically 2 bars continuous)",
                "Use rebar chairs to maintain 3-inch clear cover from bottom",
                "Tie rebar intersections with wire",
                "Install vertical dowels for stem wall connection per plan",
                "Double-check all dimensions and elevations"
            ],
            "qc_checks": [
                "Footing width and depth match structural plan",
                "Rebar spacing and size correct",
                "Rebar has proper cover (3 inches from soil)",
                "Forms are level and braced",
                "Dowels are plumb and spaced correctly"
            ],
            "inspections": ["Footing inspection required before concrete pour"],
            "related_sheets": ["Foundation"]
        },
        {
            "id": "FOUND-002",
            "name": "Footing Concrete Pour",
            "trade": "Foundation",
            "duration_hours": 8,
            "crew_size": 4,
            "prerequisites": ["Footing forms and rebar inspection passed"],
            "materials": [
                "Concrete (3000 PSI minimum per spec)",
                "Fiber mesh additive (optional)"
            ],
            "tools": ["Concrete vibrator", "Bull float", "Trowels", "Wheelbarrow", "Hose for water", "Screed board"],
            "safety": ["Rubber boots", "Gloves (concrete is caustic)", "Eye protection", "Long sleeves"],
            "steps": [
                "Schedule concrete delivery for early morning",
                "Have minimum 4-person crew ready",
                "Direct concrete truck chute or use wheelbarrows to fill forms",
                "Pour concrete in lifts, vibrating each lift to eliminate voids",
                "Fill forms to top, screed level with form tops",
                "Check that vertical dowels remain plumb during pour",
                "Float surface smooth",
                "Cover with plastic or wet burlap for curing",
                "Cure for minimum 7 days before loading"
            ],
            "qc_checks": [
                "Concrete slump test (4-5 inches typical)",
                "All forms filled completely, no voids",
                "Dowels remain in correct position",
                "Surface is level and smooth"
            ],
            "inspections": ["Concrete strength test (cylinders)", "Final footing inspection after strip"],
            "related_sheets": ["Foundation"]
        },
        {
            "id": "FOUND-003",
            "name": "Stem Wall & Foundation Wall",
            "trade": "Foundation",
            "duration_hours": 32,
            "crew_size": 3,
            "prerequisites": ["Footings cured (7 days minimum)", "Footing inspection passed"],
            "materials": [
                "Concrete blocks (CMU) or concrete for poured wall",
                "Rebar (vertical and horizontal per plan)",
                "Mortar or concrete",
                "Anchor bolts (1/2 inch, per plan)",
                "Form lumber if poured wall (2x10 or 2x12)",
                "Form ties and walers"
            ],
            "tools": ["Block saw", "Trowel", "Level", "String line", "Rebar cutter", "Drill for anchor bolts"],
            "safety": ["Back support belt (blocks are heavy)", "Gloves", "Steel-toe boots", "Eye protection"],
            "steps": [
                "Snap chalk line on footing for stem wall alignment",
                "If CMU: Lay first course on mortar bed, check level and plumb",
                "Continue courses, installing horizontal rebar in bond beams",
                "Fill block cores with grout and vertical rebar per plan",
                "Install anchor bolts in top course (typically 6ft spacing, 7 inches embedded)",
                "If poured: Erect forms, install rebar, pour and vibrate concrete",
                "Cure for 7 days",
                "Backfill against wall only after curing (use gravel for drainage)"
            ],
            "qc_checks": [
                "Wall is plumb and level",
                "Height matches plan",
                "Anchor bolts are vertical and at correct spacing",
                "Rebar is fully grouted (no voids)",
                "Top of wall is level for sill plate"
            ],
            "inspections": ["Foundation wall inspection before backfill"],
            "related_sheets": ["Foundation", "Structural"]
        }
    ],
    "Framing": [
        {
            "id": "FRAME-001",
            "name": "Sill Plate Installation",
            "trade": "Framing",
            "duration_hours": 8,
            "crew_size": 2,
            "prerequisites": ["Foundation complete and cured", "Foundation inspection passed"],
            "materials": [
                "Pressure-treated 2x6 sill plate (per plan)",
                "Sill seal foam gasket",
                "Nuts and washers for anchor bolts",
                "Construction adhesive"
            ],
            "tools": ["Drill with socket", "Hammer drill for adjustment holes", "Circular saw", "Level", "Chalk line"],
            "safety": ["Gloves", "Steel-toe boots", "Safety glasses", "Fall protection if foundation wall is high"],
            "steps": [
                "Clean top of foundation wall, remove debris",
                "Lay sill seal foam on top of foundation",
                "Measure and mark sill plate boards for anchor bolt locations",
                "Drill holes in sill plate slightly larger than anchor bolts (9/16 inch for 1/2 inch bolt)",
                "Place sill plate over anchor bolts",
                "Check sill plate is level and aligned with foundation edge",
                "Install washers and nuts, hand-tighten",
                "Torque nuts evenly to snug (do not overtighten and crack plate)",
                "Seal any gaps with construction adhesive"
            ],
            "qc_checks": [
                "Sill plate is level (shim if needed)",
                "Plate is pressure-treated (required by code)",
                "All anchor bolts have washers and are tight",
                "Foam sill seal is intact under plate"
            ],
            "inspections": ["Framing inspection (part of wall framing check)"],
            "related_sheets": ["Foundation", "Structural"]
        },
        {
            "id": "FRAME-002",
            "name": "Floor/Deck Framing",
            "trade": "Framing",
            "duration_hours": 40,
            "crew_size": 4,
            "prerequisites": ["Sill plate installed"],
            "materials": [
                "Rim joist lumber (2x10 or per plan)",
                "Floor joists (2x10 at 16 inch OC typical, per structural plan)",
                "Joist hangers",
                "3-inch deck screws or 16d nails",
                "Blocking (2x10 solid blocking at mid-span)",
                "3/4 inch T&G OSB or plywood subfloor",
                "Construction adhesive"
            ],
            "tools": ["Circular saw", "Framing nailer or hammer", "Drill", "Speed square", "Level", "Chalk line"],
            "safety": ["Hard hat", "Safety glasses", "Tool belt", "Fall protection if >6ft", "Steel-toe boots"],
            "steps": [
                "Install rim joist around perimeter, fastened to sill plate",
                "Mark joist spacing on rim joist (16 inch OC typical)",
                "Cut floor joists to length (span per plan)",
                "Install joists with joist hangers or toe-nailed to rim and bearing wall",
                "Crown each joist upward before fastening",
                "Install mid-span blocking between joists for lateral bracing",
                "Check floor frame is level and square",
                "Apply construction adhesive in zigzag pattern on top of joists",
                "Install subfloor panels perpendicular to joists, stagger seams",
                "Leave 1/8 inch gap between panels for expansion",
                "Fasten panels with screws every 6 inches on edges, 12 inches in field"
            ],
            "qc_checks": [
                "Joist spacing matches plan (16 inch or 24 inch OC)",
                "Floor is level within 1/4 inch over 10 feet",
                "All joists crowned upward",
                "Subfloor seams fall on joist centers",
                "No squeaks (adhesive prevents this)"
            ],
            "inspections": ["Framing inspection before insulation"],
            "related_sheets": ["Structural", "Architectural"]
        },
        {
            "id": "FRAME-003",
            "name": "Wall Framing",
            "trade": "Framing",
            "duration_hours": 60,
            "crew_size": 4,
            "prerequisites": ["Floor deck complete"],
            "materials": [
                "2x4 or 2x6 studs (per plan, typically 16 inch OC)",
                "2x4 or 2x6 top and bottom plates (3 plates total: bottom, top, double top)",
                "Headers (sized per span table for openings)",
                "Jack studs and king studs for openings",
                "Cripple studs above/below openings",
                "16d nails or framing screws",
                "Hurricane ties/straps for top plate connection"
            ],
            "tools": ["Circular saw", "Framing nailer", "Hammer", "Level (4ft and 8ft)", "Speed square", "Chalk line", "Measuring tape"],
            "safety": ["Hard hat", "Safety glasses", "Tool belt", "Fall protection if >6ft", "Steel-toe boots", "Gloves"],
            "steps": [
                "Snap chalk lines on deck for wall locations per architectural plan",
                "Cut bottom plate and top plates to length for each wall",
                "Mark stud locations on plates (16 inch OC typical)",
                "Mark door and window openings on plates",
                "Cut studs to length (typically 92-5/8 inches for 8ft ceiling)",
                "Assemble wall flat on deck: nail studs between bottom and top plates",
                "Install headers, jack studs, king studs, and cripples at openings",
                "Raise wall and brace plumb",
                "Nail bottom plate to deck/sill plate",
                "Nail double top plate (lapping corners for tie-in)",
                "Install blocking/fire blocking at mid-height if required by code",
                "Repeat for all walls",
                "Connect walls at corners with 3-stud corners or equivalent",
                "Install hurricane ties or straps at top plate/rafter connection"
            ],
            "qc_checks": [
                "All walls are plumb (check every 10 feet)",
                "Stud spacing is consistent (16 inch OC)",
                "Headers are sized correctly for span",
                "Corners are square and nailed properly",
                "Double top plate laps at corners (minimum 4ft lap)",
                "Opening dimensions match plan"
            ],
            "inspections": ["Framing inspection before sheathing/insulation"],
            "related_sheets": ["Architectural", "Structural"]
        },
        {
            "id": "FRAME-004",
            "name": "Roof Framing",
            "trade": "Framing",
            "duration_hours": 48,
            "crew_size": 4,
            "prerequisites": ["Wall framing complete and inspected"],
            "materials": [
                "Rafters or trusses (per plan)",
                "Ridge board (if stick-framed)",
                "Ceiling joists (if not using trusses)",
                "Hurricane ties for rafter connections",
                "Fascia board",
                "Soffit material",
                "Frieze blocking",
                "3/2 inch ring shank nails"
            ],
            "tools": ["Circular saw", "Framing nailer", "Hammer", "Level", "Chalk line", "Speed square", "Ladder or scaffolding"],
            "safety": ["Fall protection (harness and lifeline)", "Hard hat", "Safety glasses", "Non-slip boots", "Tool belt"],
            "steps": [
                "If trusses: Crane or multiple crew lift trusses into place, space per plan (typically 24 inch OC)",
                "If stick-framed: Install ceiling joists first, then ridge board, then cut and install rafters",
                "Attach rafters to top plate with hurricane ties (critical for wind resistance)",
                "Install collar ties or rafter ties per code (typically every 4ft)",
                "Check roof plane is straight (no dips or humps)",
                "Install fascia board at rafter tails",
                "Install frieze blocking between rafters at top plate",
                "Install soffit and vents for attic ventilation"
            ],
            "qc_checks": [
                "Roof pitch matches plan",
                "All rafters/trusses are plumb and spaced correctly",
                "Hurricane ties installed at every connection",
                "Ridge board is straight",
                "Overhangs are consistent",
                "Soffit vents provide adequate attic ventilation (1:150 ratio)"
            ],
            "inspections": ["Framing inspection before sheathing"],
            "related_sheets": ["Roofing", "Structural"]
        }
    ],
    "Roofing": [
        {
            "id": "ROOF-001",
            "name": "Roof Sheathing",
            "trade": "Roofing",
            "duration_hours": 24,
            "crew_size": 3,
            "prerequisites": ["Roof framing inspection passed"],
            "materials": [
                "7/16 inch or 1/2 inch OSB or plywood (per plan)",
                "8d ring shank nails or screws",
                "H-clips for panel edges (if required)"
            ],
            "tools": ["Circular saw", "Nailer", "Chalk line", "Speed square", "Harness and lifeline"],
            "safety": ["Fall protection (100% tie-off)", "Hard hat", "Non-slip boots", "Safety glasses"],
            "steps": [
                "Start at bottom edge (eave), install panels perpendicular to rafters",
                "Leave 1/8 inch gap between panels for expansion",
                "Stagger panel seams (offset by at least 4ft)",
                "Install H-clips between panels if rafters are 24 inch OC",
                "Nail every 6 inches on edges, 12 inches in field",
                "Cut around vents and chimneys",
                "Ensure all panel edges land on rafter centers",
                "Work way up to ridge"
            ],
            "qc_checks": [
                "All seams fall on rafter centers",
                "No bounce or soft spots",
                "Panel gaps are consistent",
                "All edges are nailed securely"
            ],
            "inspections": ["Sheathing inspection (if required)"],
            "related_sheets": ["Roofing"]
        },
        {
            "id": "ROOF-002",
            "name": "Underlayment & Flashing",
            "trade": "Roofing",
            "duration_hours": 16,
            "crew_size": 2,
            "prerequisites": ["Roof sheathing complete"],
            "materials": [
                "Roofing felt (30lb) or synthetic underlayment",
                "Ice and water shield (eaves and valleys)",
                "Drip edge flashing (eave and rake)",
                "Step flashing for chimneys/walls",
                "Roofing nails or cap nails"
            ],
            "tools": ["Hammer", "Utility knife", "Chalk line", "Tin snips", "Harness and lifeline"],
            "safety": ["Fall protection (100% tie-off)", "Hard hat", "Non-slip boots", "Safety glasses", "Gloves"],
            "steps": [
                "Install ice and water shield at eaves (6ft minimum, or per code)",
                "Install drip edge at eaves over underlayment",
                "Roll out underlayment horizontally starting at eave, overlap 6 inches",
                "Fasten underlayment with cap nails or staples",
                "Install ice and water shield in all valleys",
                "Install step flashing at walls and chimneys (weave with shingles later)",
                "Install drip edge at rakes over underlayment",
                "Ensure underlayment is wrinkle-free and secure"
            ],
            "qc_checks": [
                "Ice and water shield covers eaves and valleys completely",
                "Drip edge installed correctly (eave edge under, rake edge over)",
                "Underlayment overlaps are correct (6 inches min)",
                "No tears or gaps in underlayment"
            ],
            "inspections": ["None typically, but document with photos"],
            "related_sheets": ["Roofing", "Details"]
        },
        {
            "id": "ROOF-003",
            "name": "Shingle Installation",
            "trade": "Roofing",
            "duration_hours": 32,
            "crew_size": 3,
            "prerequisites": ["Underlayment and flashing complete", "Dry weather forecast"],
            "materials": [
                "Asphalt shingles (30-year architectural grade typical)",
                "Starter strip shingles",
                "Ridge cap shingles",
                "Roofing nails (1-1/4 inch)",
                "Roofing cement for penetrations"
            ],
            "tools": ["Roofing nailer", "Utility knife", "Chalk line", "Hammer", "Harness and lifeline"],
            "safety": ["Fall protection (100% tie-off)", "Hard hat", "Non-slip boots", "Knee pads", "Safety glasses"],
            "steps": [
                "Install starter strip along eave (adhesive strip facing up)",
                "Snap horizontal chalk lines for shingle courses (every 5 inches typically)",
                "Install first course of shingles along eave, overhang drip edge by 1/2 inch",
                "Nail each shingle with 4-6 nails per manufacturer instructions",
                "Offset each course by 6 inches (half-tab) for pattern",
                "Work up roof, following chalk lines",
                "Cut and weave step flashing at wall intersections",
                "At ridge, install ridge cap shingles with overlap, nail on downslope side",
                "Seal all penetrations (vents, pipes) with roofing cement and boot flashings"
            ],
            "qc_checks": [
                "All shingles are aligned and nailed correctly",
                "Shingle exposure is consistent (typically 5 inches)",
                "Ridge caps are sealed and nailed properly",
                "All penetrations are sealed and flashed",
                "No exposed nail heads"
            ],
            "inspections": ["Final roofing inspection"],
            "related_sheets": ["Roofing"]
        }
    ],
    "Electrical": [
        {
            "id": "ELEC-001",
            "name": "Electrical Rough-In",
            "trade": "Electrical",
            "duration_hours": 40,
            "crew_size": 2,
            "prerequisites": ["Framing inspection passed", "Wall and ceiling cavities accessible"],
            "materials": [
                "Romex cable (12/2, 14/2, 14/3 per circuit plan)",
                "Electrical boxes (outlet, switch, ceiling)",
                "Box nails or screws",
                "Wire staples",
                "Breaker panel (if not already installed)",
                "Breakers (per electrical plan)",
                "Grounding wire/rods"
            ],
            "tools": ["Drill with spade bits", "Wire strippers", "Cable cutters", "Fish tape", "Voltage tester", "Headlamp"],
            "safety": ["Turn off main breaker before connections", "Insulated tools", "Rubber gloves", "Safety glasses"],
            "steps": [
                "Review electrical plan and mark outlet/switch/fixture locations on studs",
                "Install electrical boxes at marked locations (height per code: outlets 12-18 inch, switches 48 inch)",
                "Drill 3/4 inch holes through studs for cable runs (center of stud, avoid edges)",
                "Run cable from panel to each box, leaving 8-12 inches extra at each box",
                "Staple cable within 8 inches of boxes and every 4ft along run",
                "Use nail plates if holes are within 1-1/4 inches of stud edge",
                "Install dedicated circuits for kitchen, bathroom, garage (20A required)",
                "Connect all cables to breaker panel (do not energize yet)",
                "Install grounding electrode system per code"
            ],
            "qc_checks": [
                "All boxes are securely fastened and at correct height",
                "Cable is stapled properly (no sagging)",
                "No cable damage or nicks in insulation",
                "Proper cable size for circuit (12AWG for 20A, 14AWG for 15A)",
                "All penetrations have nail plates",
                "Circuits match electrical plan"
            ],
            "inspections": ["Electrical rough-in inspection (required before closing walls)"],
            "related_sheets": ["Electrical"]
        },
        {
            "id": "ELEC-002",
            "name": "Electrical Trim-Out",
            "trade": "Electrical",
            "duration_hours": 24,
            "crew_size": 2,
            "prerequisites": ["Drywall installed", "Electrical rough-in inspection passed"],
            "materials": [
                "Outlets and switches (15A or 20A per circuit)",
                "Cover plates",
                "Light fixtures",
                "Wire nuts",
                "Electrical tape",
                "GFCI outlets (kitchen, bath, exterior)",
                "AFCI breakers (bedrooms)"
            ],
            "tools": ["Screwdrivers", "Wire strippers", "Voltage tester", "Drill", "Ladder"],
            "safety": ["Turn off circuit breakers before working", "Test wires with voltage tester", "Insulated tools"],
            "steps": [
                "Trim excess cable from boxes, leave 6 inches for connections",
                "Strip wire insulation (3/4 inch)",
                "Connect outlets: white to silver screw, black to brass screw, ground to green screw",
                "Connect switches: black (hot) to brass screws, white wire capped off, ground to green",
                "Install GFCI outlets in required locations (test button should work)",
                "Fold wires into box and secure outlet/switch with screws",
                "Install cover plates",
                "Install light fixtures per manufacturer instructions",
                "Label breaker panel clearly (bedroom 1, kitchen outlets, etc.)"
            ],
            "qc_checks": [
                "All connections are tight (tug test)",
                "Polarity is correct (test with outlet tester)",
                "GFCI outlets test properly",
                "All cover plates installed flush",
                "No exposed wires",
                "Panel labels are clear"
            ],
            "inspections": ["Final electrical inspection"],
            "related_sheets": ["Electrical"]
        }
    ],
    "Plumbing": [
        {
            "id": "PLUMB-001",
            "name": "Underground Plumbing",
            "trade": "Plumbing",
            "duration_hours": 24,
            "crew_size": 2,
            "prerequisites": ["Foundation forms set but not poured (or slab trenches dug)"],
            "materials": [
                "4-inch PVC drain pipe",
                "3-inch PVC vent pipe",
                "2-inch drain lines for fixtures",
                "PVC fittings (elbows, tees, wyes)",
                "PVC primer and cement",
                "Gravel for bedding",
                "Cleanout fittings"
            ],
            "tools": ["PVC saw or cutters", "Level", "Shovel", "Tape measure", "Marker"],
            "safety": ["Gloves (PVC cement is harsh)", "Safety glasses", "Ventilate area (cement fumes)"],
            "steps": [
                "Locate main sewer connection point per civil plan",
                "Dig trenches for drain lines (minimum 2% slope, 1/4 inch per foot)",
                "Lay 4-inch main drain line from house to sewer connection",
                "Install wye fittings for branch drains (toilet, shower, sink, etc.)",
                "Install 2-inch branch lines to fixture locations with proper slope",
                "Stub up vent pipes through foundation/slab at fixture locations",
                "Install cleanouts every 100ft and at direction changes",
                "Prime and cement all joints (dry fit first)",
                "Bed pipes in gravel for support",
                "Pressure test or water test system before covering"
            ],
            "qc_checks": [
                "All pipes have proper slope (minimum 1/4 inch per foot)",
                "Joints are glued properly (no leaks)",
                "Vent pipes are stubbed correctly at fixture locations",
                "Cleanouts are accessible",
                "No damage to pipes"
            ],
            "inspections": ["Underground plumbing inspection before covering"],
            "related_sheets": ["Plumbing", "Foundation"]
        },
        {
            "id": "PLUMB-002",
            "name": "Water Supply Rough-In",
            "trade": "Plumbing",
            "duration_hours": 32,
            "crew_size": 2,
            "prerequisites": ["Framing complete", "Underground plumbing complete"],
            "materials": [
                "PEX or copper pipe (3/4 inch main, 1/2 inch branches)",
                "PEX fittings and manifold (if using PEX)",
                "Copper fittings and solder (if copper)",
                "Pipe hangers and straps",
                "Shut-off valves",
                "Water heater (50-gal typical)",
                "Hose bibs for exterior"
            ],
            "tools": ["PEX crimper or expansion tool", "Pipe cutter", "Torch and solder (if copper)", "Drill", "Hole saw"],
            "safety": ["Safety glasses", "Gloves", "Fire extinguisher nearby if soldering"],
            "steps": [
                "Connect main water line from meter to house (3/4 inch or 1 inch per plan)",
                "Install water heater in designated location (on pan with drain)",
                "Run 3/4 inch hot and cold lines from water heater to central manifold",
                "Run 1/2 inch branch lines from manifold to each fixture (sink, toilet, shower, etc.)",
                "Secure pipes to studs with hangers every 6ft",
                "Drill through studs (center) for horizontal runs, nail plates if within 1-1/4 inch of edge",
                "Stub out hot and cold supplies at fixture locations (height per code)",
                "Install shut-off valves at each fixture stub",
                "Install hose bibs at exterior walls",
                "Pressure test system (50 PSI for 24 hours, no leaks)"
            ],
            "qc_checks": [
                "All pipes are secured properly (no sagging)",
                "Hot is on left, cold is on right at fixtures",
                "Shut-off valves installed at all fixtures",
                "No leaks during pressure test",
                "Pipes protected from freezing (insulation or wall cavity depth)"
            ],
            "inspections": ["Plumbing rough-in inspection"],
            "related_sheets": ["Plumbing"]
        },
        {
            "id": "PLUMB-003",
            "name": "Plumbing Fixtures & Trim",
            "trade": "Plumbing",
            "duration_hours": 16,
            "crew_size": 2,
            "prerequisites": ["Drywall finished", "Plumbing rough-in inspection passed"],
            "materials": [
                "Toilets",
                "Sinks and faucets",
                "Shower/tub fixtures",
                "Wax rings for toilets",
                "Teflon tape",
                "Supply lines (braided stainless)",
                "P-traps"
            ],
            "tools": ["Adjustable wrench", "Basin wrench", "Screwdrivers", "Level", "Caulk gun"],
            "safety": ["Gloves", "Safety glasses"],
            "steps": [
                "Install toilets: set wax ring on flange, set toilet, bolt down, connect supply line",
                "Install sinks: mount sink, connect faucet, attach P-trap to drain, connect supply lines",
                "Install shower fixtures: attach trim plate, install shower head and valve handle",
                "Test all fixtures for leaks (run water for 5 minutes)",
                "Caulk around base of toilets and sinks (not back of toilet)",
                "Install shower doors or curtain rods",
                "Ensure all shut-off valves are accessible and working"
            ],
            "qc_checks": [
                "All fixtures are level and secure",
                "No leaks at connections",
                "Drains flow properly (no slow drains)",
                "Hot/cold valves work correctly",
                "Caulking is neat and complete"
            ],
            "inspections": ["Final plumbing inspection"],
            "related_sheets": ["Plumbing"]
        }
    ],
    "HVAC": [
        {
            "id": "HVAC-001",
            "name": "HVAC Rough-In",
            "trade": "HVAC",
            "duration_hours": 32,
            "crew_size": 2,
            "prerequisites": ["Framing complete", "Roof sheathed"],
            "materials": [
                "HVAC unit (sized per load calculation)",
                "Ductwork (flex duct or metal)",
                "Supply registers",
                "Return grilles",
                "Duct tape and mastic",
                "Refrigerant lines",
                "Condensate drain line"
            ],
            "tools": ["Tin snips", "Drill", "Hole saw", "Duct knife", "Level"],
            "safety": ["Gloves (sharp metal edges)", "Safety glasses", "Dust mask"],
            "steps": [
                "Install HVAC unit in attic, garage, or exterior pad (per plan)",
                "Run main supply trunk line from unit to central location",
                "Branch flex ducts to each room per plan (sized for CFM requirement)",
                "Install supply registers in ceiling or floor per plan",
                "Install return grille in central location (typically hallway)",
                "Run refrigerant lines from condenser to air handler (if split system)",
                "Run condensate drain line to exterior or drain",
                "Seal all duct joints with mastic (not just tape)",
                "Insulate ducts in unconditioned spaces"
            ],
            "qc_checks": [
                "All ducts are sealed and insulated",
                "Supply registers are balanced (dampers adjusted)",
                "Return grille has proper clearance (no blockage)",
                "Condensate drain has proper slope",
                "Unit is level and secured"
            ],
            "inspections": ["HVAC rough-in inspection"],
            "related_sheets": ["HVAC"]
        }
    ]
}

def generate_task_json():
    """Generate tasks JSON with all trades."""
    all_tasks = []
    task_id_counter = 1
    
    for trade, tasks in CONSTRUCTION_TASKS.items():
        for task in tasks:
            task['task_id'] = task_id_counter
            all_tasks.append(task)
            task_id_counter += 1
    
    # Load blueprint data to link sheets
    with open(BLUEPRINT_DATA) as f:
        blueprint_data = json.load(f)
    
    # Match tasks to blueprint pages
    for task in all_tasks:
        task['blueprint_pages'] = []
        for related_category in task.get('related_sheets', []):
            # Find pages in this category
            if related_category in blueprint_data['by_category']:
                pages = blueprint_data['by_category'][related_category]
                task['blueprint_pages'].extend([
                    {
                        'page_num': p['page_num'],
                        'sheet_num': p['sheet_num'],
                        'title': p['title']
                    } for p in pages
                ])
    
    output = {
        'project': {
            'id': 'PROJ-001',
            'name': '728 Cortlandt Drive',
            'address': '728 Cortlandt Drive',
            'status': 'In Progress',
            'start_date': '2025-10-27',
            'crew_size': 7,
            'work_hours': '7:30 AM - 4:00 PM',
            'work_days': 'Monday - Friday'
        },
        'tasks': all_tasks,
        'summary': {
            'total_tasks': len(all_tasks),
            'total_hours': sum(t['duration_hours'] for t in all_tasks),
            'trades': list(CONSTRUCTION_TASKS.keys())
        }
    }
    
    OUTPUT_TASKS.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_TASKS, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"✅ Generated {len(all_tasks)} tasks")
    print(f"📁 Saved to: {OUTPUT_TASKS}")
    
    return output

def generate_sop_pages(tasks_data):
    """Generate individual SOP HTML pages for each task."""
    OUTPUT_SOPS.mkdir(parents=True, exist_ok=True)
    
    for task in tasks_data['tasks']:
        sop_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{task['id']} - {task['name']} SOP</title>
  <script src="../assets/shared-nav.js"></script>
  <style>
    body {{background:#0a0e27; color:#e8eef5; font-family:system-ui; padding:16px; line-height:1.6}}
    .container {{max-width:900px; margin:0 auto; padding-bottom:100px}}
    h1 {{color:#667eea; margin-bottom:8px}}
    .meta {{display:flex; gap:16px; flex-wrap:wrap; margin:16px 0; padding:12px; background:#12161b; border-radius:8px}}
    .meta-item {{display:flex; flex-direction:column}}
    .meta-label {{font-size:11px; color:#8a98ab; text-transform:uppercase}}
    .meta-value {{font-size:14px; color:#e8eef5; font-weight:600}}
    .section {{margin:24px 0; padding:16px; background:#12161b; border-left:4px solid #667eea; border-radius:6px}}
    .section h2 {{margin-top:0; color:#9cc1ff; font-size:18px}}
    .section ul {{margin:8px 0; padding-left:20px}}
    .section li {{margin:6px 0}}
    .steps {{counter-reset:step}}
    .steps li {{counter-increment:step; margin:12px 0; padding-left:8px}}
    .steps li::marker {{content:counter(step) ". "; color:#667eea; font-weight:bold}}
    .qc-check {{background:#1a2332; padding:8px 12px; margin:8px 0; border-radius:4px; border-left:3px solid #28a745}}
    .safety-warning {{background:#2d1a1a; padding:12px; margin:16px 0; border-radius:6px; border-left:4px solid:#dc3545}}
    .safety-warning::before {{content:"⚠️ SAFETY: "; font-weight:bold; color:#dc3545}}
    .blueprint-links {{display:flex; gap:8px; flex-wrap:wrap; margin-top:12px}}
    .bp-link {{background:#667eea; color:#fff; padding:6px 12px; border-radius:4px; text-decoration:none; font-size:13px}}
    .bp-link:hover {{background:#764ba2}}
    .back-btn {{display:inline-block; background:#303947; color:#e8eef5; padding:10px 20px; border-radius:6px; text-decoration:none; margin-bottom:20px}}
    .back-btn:hover {{background:#3d4757}}
  </style>
</head>
<body data-jsdom-page="sop" data-jsdom-title="📋 {task['id']} SOP">
  <div class="container">
    <a href="../project.html" class="back-btn">← Back to Tasks</a>
    
    <h1>{task['id']}: {task['name']}</h1>
    
    <div class="meta">
      <div class="meta-item">
        <span class="meta-label">Trade</span>
        <span class="meta-value">{task['trade']}</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Duration</span>
        <span class="meta-value">{task['duration_hours']} hours</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Crew Size</span>
        <span class="meta-value">{task['crew_size']} people</span>
      </div>
    </div>
    
    <div class="section">
      <h2>📋 Prerequisites</h2>
      <ul>
        {''.join(f'<li>{p}</li>' for p in task['prerequisites'])}
      </ul>
    </div>
    
    <div class="section">
      <h2>🧰 Materials Needed</h2>
      <ul>
        {''.join(f'<li>{m}</li>' for m in task['materials'])}
      </ul>
    </div>
    
    <div class="section">
      <h2>🔧 Tools Required</h2>
      <ul>
        {''.join(f'<li>{t}</li>' for t in task['tools'])}
      </ul>
    </div>
    
    <div class="safety-warning">
      {'<br>'.join(task['safety'])}
    </div>
    
    <div class="section">
      <h2>📝 Step-by-Step Instructions</h2>
      <ol class="steps">
        {''.join(f'<li>{s}</li>' for s in task['steps'])}
      </ol>
    </div>
    
    <div class="section">
      <h2>✅ Quality Control Checks</h2>
      {''.join(f'<div class="qc-check">{qc}</div>' for qc in task['qc_checks'])}
    </div>
    
    <div class="section">
      <h2>🔍 Required Inspections</h2>
      <ul>
        {''.join(f'<li>{i}</li>' for i in task['inspections'])}
      </ul>
    </div>
    
    <div class="section">
      <h2>📐 Related Blueprint Pages</h2>
      <div class="blueprint-links">
        {''.join(f'<a href="../index.html?sheet={p["sheet_num"]}" class="bp-link">{p["sheet_num"]}: {p["title"][:30]}</a>' for p in task['blueprint_pages'])}
      </div>
    </div>
  </div>
</body>
</html>"""
        
        sop_file = OUTPUT_SOPS / f"{task['id']}.html"
        with open(sop_file, 'w') as f:
            f.write(sop_html)
    
    print(f"✅ Generated {len(tasks_data['tasks'])} SOP pages")
    print(f"📁 Saved to: {OUTPUT_SOPS}/")

def main():
    print("🏗️  Generating Tasks and SOPs for 728 Cortlandt Drive\n")
    
    tasks_data = generate_task_json()
    generate_sop_pages(tasks_data)
    
    print(f"\n✨ Complete!")
    print(f"   - {tasks_data['summary']['total_tasks']} tasks")
    print(f"   - {tasks_data['summary']['total_hours']} total hours")
    print(f"   - {len(tasks_data['summary']['trades'])} trades")

if __name__ == "__main__":
    main()

