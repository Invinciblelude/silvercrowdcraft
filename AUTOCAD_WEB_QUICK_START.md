# 🚀 AutoCAD Web - Blueprint to 3D Quick Start Guide

## ✅ What You Have:
- AutoCAD Web (30-day free trial)
- Your 728 Cordant blueprint PDF uploaded

---

## 🎯 **MOST EFFICIENT WORKFLOW**

### **Important:** AutoCAD Web is 2D Only!

For **3D modeling**, you need either:
1. **AutoCAD Desktop** (download from Autodesk)
2. **Use AutoCAD Web for 2D, then export to another program for 3D**

**RECOMMENDATION:** Get AutoCAD Desktop (free 30-day trial) for full 3D capabilities.

---

## 🔄 **Your Two Options:**

### **Option A: AutoCAD Desktop (RECOMMENDED for 3D)**

**Download:**
1. Go to: https://www.autodesk.com/products/autocad/free-trial
2. Download AutoCAD for Mac
3. Install (works on Mac!)
4. You get 30 days free

**Why Desktop?**
- ✅ Full 3D modeling tools
- ✅ Faster performance
- ✅ More powerful commands
- ✅ Can import PDF and trace

### **Option B: AutoCAD Web (2D only)**

**What you can do:**
- ✅ Trace 2D floor plan
- ✅ Create accurate 2D drawings
- ❌ **Cannot create 3D models**

---

## 🏗️ **FASTEST METHOD: AutoCAD Desktop**

### **Step 1: Download & Install (10 minutes)**
1. Visit: https://www.autodesk.com/products/autocad/free-trial
2. Download "AutoCAD 2024 for Mac"
3. Install and sign in with your Autodesk account

### **Step 2: Import Your Blueprint (2 minutes)**
1. Open AutoCAD Desktop
2. Type: **PDFIMPORT** (press Enter)
3. Select your `728 Cortlandt Drive Plans actual.pdf`
4. Choose which sheet (pick Floor Plan - Sheet A1.01)
5. Click OK - blueprint appears!

### **Step 3: Scale the Drawing (5 minutes)**
Your blueprint is 1/4" = 1'-0" scale

1. Type: **SCALE** (press Enter)
2. Select the imported PDF
3. Base point: Pick any corner
4. Type: **48** (because 1/4" × 4 = 1" per foot × 12 = 48)
5. Press Enter

Now your drawing is at real-world scale!

### **Step 4: Trace ONE Wall (10 minutes)**

**Most Important: Work in LAYERS**

1. Type: **LAYER** (press Enter) - Layer Properties window opens
2. Create new layer: **WALLS-EXTERIOR**
   - Color: Red
   - Lineweight: 0.30mm
3. Create new layer: **WALLS-INTERIOR**
   - Color: Yellow  
   - Lineweight: 0.20mm
4. Set **WALLS-EXTERIOR** as current

**Draw First Wall:**
1. Type: **LINE** (or press L + Enter)
2. Click starting point on blueprint
3. Move mouse, type length: **14'4"** (for 14 feet, 4 inches)
4. Press Enter twice to finish

**Pro Tip:** Turn on **ORTHO** (F8) to draw straight lines

### **Step 5: Create 3D Walls (MAGIC!)** 

Once you've traced walls in 2D:

1. Select all wall lines
2. Type: **EXTRUDE** (press Enter)
3. Type: **8'** (for 8-foot wall height)
4. Press Enter

**BOOM! Your 2D lines become 3D walls!**

### **Step 6: Add Thickness to Walls**

Exterior walls are 6" thick (2x6 studs):

1. Select a wall line
2. Type: **OFFSET** (press Enter)
3. Type: **6** (for 6 inches)
4. Click to which side to offset
5. Press Enter

Now you have a 6" thick wall!

---

## ⚡ **SUPER EFFICIENT WORKFLOW**

### **The "Trace & Extrude" Method (Fastest)**

**Time: 4-6 hours for entire house**

1. **Hour 1:** Import PDF, scale, set up layers
2. **Hours 2-3:** Trace ALL walls (exterior first, then interior)
3. **Hour 4:** Offset walls for thickness
4. **Hour 5:** Extrude walls to 8' height
5. **Hour 6:** Add roof, doors, windows

### **Essential AutoCAD Commands:**

| Command | Shortcut | What It Does |
|---------|----------|--------------|
| **LINE** | L | Draw straight lines |
| **OFFSET** | O | Copy line at distance (for wall thickness) |
| **EXTRUDE** | EXT | Make 2D into 3D |
| **MOVE** | M | Move objects |
| **COPY** | CO | Copy objects |
| **ROTATE** | RO | Rotate objects (for angled walls!) |
| **TRIM** | TR | Cut lines at intersections |
| **EXTEND** | EX | Extend lines to meet |
| **FILLET** | F | Round corners |
| **3DORBIT** | 3DO | Rotate 3D view |
| **VSCURRENT** | - | Change visual style (realistic, wireframe) |

---

## 📏 **Working with YOUR Specific Dimensions**

### Room-by-Room Tracing Order (Easiest to Hardest):

1. **OFFICE** (12'-8" × 11'-4") - Rectangular, simple
2. **BEDROOM 2** (14'-4" × 10'-8") - Rectangular
3. **BEDROOM 3** (14'-4" × 10'-8") - Rectangular
4. **KITCHEN** (14'-6" × 17'-4") - Rectangular
5. **GREAT ROOM** (24'-2" × 19'-8") - Large, vaulted ceiling
6. **MASTER SUITE** - Angled walls (HARDEST)

**Start with Office - it's the simplest!**

---

## 🎨 **Viewing Your 3D Model**

After extruding walls:

1. Type: **3DORBIT** (or click the orbit tool)
2. Hold left mouse button and drag to rotate view
3. Type: **VSCURRENT** → Select **"Realistic"** for solid view
4. Type: **HIDE** to hide the blueprint underlay

---

## 💾 **Saving & Exporting**

### Save Your Work:
- **Ctrl + S** (save as .dwg file)

### Export for Others:
1. **PDF:** Type **EXPORTPDF**
2. **3D PDF:** Type **3DPDF** (clients can rotate in Adobe)
3. **OBJ/STL:** For 3D printing or other software

---

## 🆘 **Common Issues & Solutions**

### "I can't see my 3D walls after EXTRUDE"
- Type: **3DORBIT** to rotate view
- You're probably looking straight down (top view)

### "My dimensions are wrong"
- Check your scale! Blueprint should be scaled 48x
- Type: **MEASUREGEOM** → **Distance** to verify

### "The angled walls (Master suite) are hard"
- Use **ROTATE** command
- After drawing wall, type: **RO** → Select wall → Type angle: **45**

### "Lines won't meet at corners"
- Use **TRIM** command (TR)
- Or use **FILLET** with radius 0

---

## 📚 **Learn These 5 Commands First**

Focus on mastering these - they're 80% of what you need:

1. **LINE (L)** - Draw walls
2. **OFFSET (O)** - Create wall thickness
3. **TRIM (TR)** - Clean up corners
4. **EXTRUDE (EXT)** - Make 3D
5. **3DORBIT (3DO)** - View your work

**Practice these on ONE room (the Office) before doing the whole house.**

---

## 🎯 **Your First Session Action Plan (2 hours)**

**Goal:** Model the OFFICE room completely

### Minute 0-30: Setup
- [ ] Download & install AutoCAD Desktop
- [ ] Open AutoCAD
- [ ] Type PDFIMPORT, select your blueprint
- [ ] Scale by 48

### Minute 30-60: Trace Office Walls
- [ ] Create WALLS-EXTERIOR layer
- [ ] Use LINE (L) command
- [ ] Draw 4 walls of Office:
  - Wall 1: 12'8" horizontal
  - Wall 2: 11'4" vertical
  - Wall 3: 12'8" horizontal (back)
  - Wall 4: 11'4" vertical (close the box)

### Minute 60-90: Add Wall Thickness
- [ ] Select one wall line
- [ ] Type: OFFSET (O)
- [ ] Distance: 4.5 (for 2x4 interior walls)
- [ ] Repeat for all 4 walls

### Minute 90-120: Make it 3D!
- [ ] Select all wall lines (both inner and outer)
- [ ] Type: EXTRUDE (EXT)
- [ ] Height: 8' (8 feet)
- [ ] Type: 3DORBIT to view
- [ ] Type: VSCURRENT → Realistic

**Congratulations! You just modeled your first room!** 🎉

---

## 📖 **Free Learning Resources**

### Official Autodesk Tutorials:
1. Go to: https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/Getting-Started-with-AutoCAD.html
2. Watch: "AutoCAD Basics" (30 minutes)
3. Watch: "3D Modeling in AutoCAD" (45 minutes)

### YouTube (Best Channels):
1. **"AutoCAD Tutorial for Beginners"** by The CAD Master
2. **"3D House in AutoCAD"** by CADTutor
3. Search: "AutoCAD floor plan to 3D"

### Practice Files:
- Don't waste time on generic tutorials
- Use YOUR actual blueprint as practice
- You'll learn faster with a real project

---

## 💰 **After 30-Day Trial**

**Options:**
1. **Student License** - FREE for 1 year (if you have .edu email)
2. **Subscription** - $235/month (expensive!)
3. **Switch to free alternative** - Use what you learned in:
   - Blender (free forever)
   - FreeCAD (free forever)
   - DraftSight (free 2D, cheap 3D)

**By then, you'll know enough to transfer skills to any CAD program.**

---

## 🚀 **READY TO START?**

**Right now:**
1. Click "New Drawing" in AutoCAD Web (just to explore)
2. OR download AutoCAD Desktop for full 3D power

**Your first goal:** Model the OFFICE room (12'8" × 11'4") in 2 hours.

Once you can do ONE room, you can do the WHOLE house - it's just repetition!

---

## ✅ **Success Checklist - Week 1**

- [ ] Day 1: Install AutoCAD Desktop, import blueprint
- [ ] Day 2: Model OFFICE room (complete)
- [ ] Day 3: Model BEDROOM 2
- [ ] Day 4: Model BEDROOM 3  
- [ ] Day 5: Model KITCHEN
- [ ] Day 6: Model GREAT ROOM (vaulted ceiling - extrude to 14')
- [ ] Day 7: Start MASTER SUITE (angled walls - challenge!)

**By end of Week 1:** You'll have 70% of the house done!

---

**Need help with a specific step? Let me know and I'll guide you through it!** 🛠️


