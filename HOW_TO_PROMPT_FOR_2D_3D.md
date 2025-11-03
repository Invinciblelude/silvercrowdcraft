# How to Prompt for Accurate 2D & 3D Models
## Using OCR to Extract EXACT Blueprint Data → Generate Models

---

## 🎯 THE COMPLETE SYSTEM

```
BLUEPRINT PDF/IMAGE
    ↓
OCR EXTRACTION (pytesseract)
    ↓
STRUCTURED DATA (JSON)
    ↓
2D CAD (DXF) ← AutoCAD can open
    ↓
3D MODEL (OBJ/GLTF) ← 3D viewers can open
```

---

## 📋 HOW TO PROMPT ME

### Option 1: Extract from Specific Blueprint File

**YOU SAY:**
> "Extract the Office room from the PDF blueprint and create 2D CAD and 3D model"

**I DO:**
1. Run OCR on `728 Cortlandt Drive Plans actual.pdf`
2. Find "OFFICE" in the extracted text
3. Extract dimensions near "OFFICE" (12'-8" x 11'-4")
4. Extract any notes/specifications near it
5. Generate 2D DXF with exact stud positions
6. Extrude to 3D model

### Option 2: Extract from Specific Sheet

**YOU SAY:**
> "Read Sheet 15 (Roof Framing Plan) and extract all beam sizes, then create 3D roof structure"

**I DO:**
1. Locate Sheet 15 image file
2. Run OCR on that specific sheet
3. Extract beam schedule (B1, B2, B3...)
4. Extract beam sizes and positions
5. Generate 3D roof model with exact beam locations

### Option 3: Extract Room with All Details

**YOU SAY:**
> "Extract Great Room from floor plan - get dimensions, windows, doors, ceiling height, and create complete 2D/3D"

**I DO:**
1. OCR floor plan image
2. Find "GREAT ROOM" text
3. Extract: 24'-2" x 19'-8" dimensions
4. Extract: Window/door markers near it
5. Extract: "VAULTED" ceiling note
6. Check elevations for exact ceiling height
7. Generate 2D CAD with all openings
8. Generate 3D with vaulted ceiling

---

## 🔧 WHAT OCR EXTRACTS

### From Floor Plans:
- **Room Names:** BEDROOM 2, OFFICE, KITCHEN, etc.
- **Dimensions:** 14'-4" x 10'-8" (exact measurements)
- **Wall Types:** "2x6" or "2x4" annotations
- **Openings:** Window/door markers and sizes

### From Structural Plans:
- **Beam Schedule:** B1, B2, B3 with sizes
- **Rafter Schedule:** R1, R2 with specifications
- **Header Sizes:** For openings
- **Nailing Patterns:** Shear wall details

### From Elevations:
- **Heights:** Wall heights, roof heights
- **Ceiling Types:** VAULTED, standard
- **Window Sizes:** Actual opening dimensions

### From Details:
- **Connection Details:** How pieces join
- **Material Specs:** Exact sizes and types
- **Special Instructions:** Notes and requirements

---

## 🎨 PROMPT TEMPLATES

### For 2D CAD:

```
"Extract [ROOM/SECTION] from [BLUEPRINT FILE]
- Get exact dimensions
- Get stud positions @ 16" O.C.
- Get all openings (windows/doors)
- Generate DXF file AutoCAD can open
- Use ONLY data from blueprint, no assumptions"
```

### For 3D Model:

```
"Extract [ROOM/SECTION] from blueprints,
then create 3D model showing:
- Walls extruded to 8'-0" height (or vaulted height if noted)
- Studs as vertical columns
- Openings cut out
- Roof structure if applicable
- Export as OBJ or GLTF for 3D viewing"
```

### For Complete Section:

```
"Extract [OFFICE/GREAT ROOM/etc.] with:
1. Floor plan dimensions (from OCR)
2. Wall specifications (from notes)
3. Window/door openings (from schedule)
4. Header sizes (from beam schedule)
5. Ceiling height (from elevations)
Then create both 2D CAD and 3D model"
```

---

## ✅ VERIFICATION PROMPT

**YOU SAY:**
> "Show me what OCR extracted for Great Room - verify the dimensions match"

**I DO:**
1. Display extracted text near "GREAT ROOM"
2. Show parsed dimensions
3. Compare to known values
4. Highlight any discrepancies
5. Show confidence scores from OCR

---

## 🚀 WORKFLOW EXAMPLE

### Step-by-Step Prompt Sequence:

**1. Initial Extraction:**
> "Run OCR on the floor plan image and extract all room dimensions"

**2. Verify:**
> "Show me the Office room extraction - is 12'-8" x 11'-4" correct?"

**3. Generate 2D:**
> "Create 2D CAD for Office using the extracted dimensions"

**4. Generate 3D:**
> "Extrude the Office 2D CAD to 3D showing walls at 8'-0" height"

**5. Add Details:**
> "Add window openings to the Office 3D model based on window schedule"

---

## 📊 DATA STRUCTURE

What I extract and store:

```json
{
  "rooms": {
    "OFFICE": {
      "name": "OFFICE",
      "dimensions": [
        {"feet": 12, "inches": 8, "total_inches": 152},
        {"feet": 11, "inches": 4, "total_inches": 136}
      ],
      "position": [1234, 567],  // Where found in image
      "notes": ["Southwest corner", "Mixed interior/exterior"]
    }
  },
  "beam_schedule": {
    "B1": {
      "id": "B1",
      "size_text": "3-3/4\" x 11\" GLU. LAM.",
      "position": [890, 234]
    }
  }
}
```

---

## 🎯 KEY POINTS FOR PROMPTING

### ✅ DO:
- Specify which blueprint file/sheet to use
- Ask for specific rooms/sections
- Request verification of extracted data
- Ask for both 2D and 3D
- Request specific details (windows, headers, etc.)

### ❌ AVOID:
- Vague requests ("make a model")
- Not specifying which room/section
- Skipping verification step
- Assuming I remember previous extractions

---

## 📝 EXAMPLE COMPLETE PROMPT

**YOU SAY:**
> "Extract the Master Bedroom from the floor plan PDF. Get the exact dimensions (should be around 15'-6" x 14'-8"), extract any window/door openings near it, check the elevations for ceiling height, then create both a 2D CAD file and a 3D model. Use only the extracted data - no guessing."

**I DO:**
1. ✅ Run OCR on PDF
2. ✅ Find "MASTER BEDROOM" text
3. ✅ Extract dimensions nearby
4. ✅ Find window/door markers
5. ✅ Check elevation sheets for height
6. ✅ Generate 2D DXF with exact measurements
7. ✅ Extrude to 3D with correct height
8. ✅ Show you the extracted data for verification

---

## 🔄 ITERATIVE PROCESS

**Prompt 1:** "Extract Office room from blueprint"
**You verify:** "Yes, 12'-8" x 11'-4" is correct"

**Prompt 2:** "Now create 2D CAD for Office"
**You verify:** "Studs are in the right places?"

**Prompt 3:** "Extrude to 3D and show me"
**You verify:** "Height looks right"

**Prompt 4:** "Add the window opening from the schedule"
**Result:** Complete accurate model

---

## 💡 ADVANCED PROMPTS

### For Complex Structures:
> "Extract the Great Room vaulted ceiling structure: get the dimensions from floor plan, the ceiling height from elevations (12'-14' peak), and the roof framing from Sheet 15. Create a 3D model showing the vaulted space."

### For Multi-Part Extraction:
> "Extract all bedrooms (Bedroom 2, Bedroom 3, Master) from the floor plan, get their exact dimensions, then create a combined 3D model showing all three rooms."

### For Structural Elements:
> "Extract all beams from Sheet 15 (Roof Framing Plan) - get beam IDs (B1-B15) and their exact sizes, then create a 3D model showing how they connect."

---

**END OF PROMPT GUIDE**

