# Blueprint-to-Diagram Prompt System
## Convert YOUR EXACT blueprints → Accurate Construction Diagrams

---

## 🎯 THE SYSTEM

You describe ANY section/detail → I extract EXACT data from blueprints → Generate precise illustration

---

## 📋 DATA EXTRACTION PROTOCOL

### Step 1: Identify WHAT You Want to Illustrate
**YOU SAY:** "Office window" OR "Great Room vaulted ceiling" OR "Master Bedroom corner"

### Step 2: I Extract EXACT Specifications from Blueprints

#### For WALLS:
**From BLUEPRINT_DATA_EXTRACTION.md:**
- Wall Type: Exterior 2x6 or Interior 2x4
- Stud Spacing: 16" O.C.
- Height: 8'-0" or Vaulted 12'-14'
- **EXACT ROOM DIMENSIONS from your plans**

#### For WINDOWS/DOORS:
**From Elevations & Schedules:**
- Window Type: "2x6 Portal Frame Fixed" (per your notes)
- Size: Need from window schedule
- Headers: Based on opening size + beam schedule

#### For OPENINGS:
**From Beam Schedule (Sheet S-3):**
- B1: 3-3/4" x 11" GLU. LAM. (DF/DF)
- B2: 3-1/8" x 12" LAM.
- B5: (4) 2x12
- B9: (5) 2x10
- **Use these EXACT sizes, not guesswork**

#### For ROOF:
**From Rafter Schedule:**
- R1: 2x8 @ 24" O.C., 16'-11" / 16'-8"
- R2: (2)TJI/560 @ 48" O.C.
- Pitch: 4:12 (main)
- Overhang: 2'-0" typical

---

## 🔨 SPECIFIC PROMPT TEMPLATE

### FOR ANY SECTION YOU DESCRIBE:

```
CREATE PRECISE CONSTRUCTION DIAGRAM FOR: [Your Description]

SOURCE DATA FROM 728 CORDANT BLUEPRINTS:

LOCATION DATA:
- Room/Section: [from BLUEPRINT_DATA_EXTRACTION.md]
- Dimensions: [exact from extraction]
- Wall Type: [exterior 2x6 or interior 2x4]
- Height: [8'-0" or vaulted]
- Special Notes: [from elevations]

WALL CONSTRUCTION (From Your Specs):
- Bottom Plate: 2x6 (1.5" x 5.5" actual) 
- Studs: 2x6 @ 16" O.C. for exterior
- Top Plates: Double 2x6
- Anchor Bolts: 5/8" @ 6'-0" max
- Sheathing: 15/32" OSB
- Insulation: R-19
- Drywall: 1/2"

OPENINGS (From Beam Schedule):
- Header Size: [Use B1-B15 schedule - EXACT size, not estimate]
- Use this EXACT beam for windows/doors in this opening

CALCULATE FROM EXACT DATA:
- Stud Count: (Wall Length ÷ 16") + 1
- Header Selection: Based on opening width + beam schedule
- Rough Opening: Unit size + standard shrinkage

ILLUSTRATION REQUIREMENTS:
1. Use EXACT dimensions from blueprints
2. Use EXACT beam sizes from schedule
3. Show EXACT stud locations (calculated)
4. Label with REAL specifications
5. No generic/typical values - only your data
```

---

## 📊 EXAMPLE TRANSFORMATIONS

### YOU SAY: "Show me the Office room walls"

**I EXTRACT:**
```
FROM BLUEPRINT_DATA_EXTRACTION.md:
- Dimensions: 12'-8" x 11'-4" (approximately 144 SF)
- Location: Southwest corner
- Wall Type: Mixed interior/exterior

CALCULATIONS:
- North Wall: 12'-8" = 152 inches
- South Wall: 152 inches
- East Wall: 11'-4" = 136 inches  
- West Wall: 136 inches

STUD COUNTS:
- North: (152 ÷ 16) + 1 = 10.5 → 11 studs
- South: 11 studs
- East: (136 ÷ 16) + 1 = 9.5 → 10 studs
- West: 10 studs

OPENINGS (if any marked on plan):
- Refer to window/door schedule for exact sizes
```

### YOU SAY: "Great Room vaulted ceiling connection"

**I EXTRACT:**
```
FROM BLUEPRINT_DATA_EXTRACTION.md:
- Dimensions: 24'-2" x 19'-8" (approximately 476 SF)
- Ceiling Height: VAULTED (per notes - likely 12'-14' at peak)

FROM ROOF DATA:
- Rafters: R1 = 2x8 @ 24" O.C.
- Pitch: 4:12
- Ridge Height: ~24'-0" from finished floor

CALCULATE:
- Standard wall: 8'-0" to plate
- Vault starts: At plate
- Vault Peak: Additional 4'-6' to 6'-6' above plate
- Total height: 12'-14' as noted

RAFTER LAYOUT:
- 24'-2" = 290 inches
- Rafters: (290 ÷ 24) + 1 = 13.1 → 14 rafters per side
```

---

## 🎨 PROMPT GENERATION WORKFLOW

### FOR EACH SECTION YOU REQUEST:

**1. YOU DESCRIBE:**
> "Show me how to frame the Master Bedroom"

**2. I LOOK UP:**
- Exact dimensions from BLUEPRINT_DATA_EXTRACTION.md
- Wall specifications 
- Window/door locations
- Special features

**3. I CALCULATE:**
- Stud counts
- Stud positions
- Header requirements
- Rough openings

**4. I GENERATE:**
- Precise diagram using EXACT data
- All measurements from your blueprints
- No generic assumptions

**5. I LABEL:**
- "12'-8" x 11'-4" - FROM YOUR BLUEPRINTS"
- "Beam B5: (4) 2x12 - FROM SCHEDULE"
- "10 studs @ 16" O.C. - CALCULATED"

---

## ✅ VERIFICATION CHECKLIST

Before creating diagram, I verify:

- [ ] Dimensions match BLUEPRINT_DATA_EXTRACTION.md
- [ ] Beam sizes from actual schedule (B1-B15)
- [ ] Rafter specs from R1, R2, R3
- [ ] Stud spacing is your spec (16" O.C.)
- [ ] Wall height is your spec (8'-0" or vaulted)
- [ ] Header selection based on opening + schedule
- [ ] No "typical" or "standard" assumptions
- [ ] All labels reference YOUR blueprints

---

## 🚀 READY TO USE

**Describe ANY section** → I extract YOUR data → I build EXACT diagram

**Examples:**
- "Office corner detail with window"
- "Great Room vaulted wall to roof connection"
- "Master Bedroom complete wall layout"
- "Kitchen to Great Room opening"
- "Any beam from schedule B1-B15 in use"

**I will use ONLY YOUR BLUEPRINT DATA - no guessing!**

---

**END OF PROMPT SYSTEM**

