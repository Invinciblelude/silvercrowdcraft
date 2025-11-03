# 🏗️ Blender Tutorial: 728 Cordant House from Blueprint

## ✅ Prerequisites
- Blender 4.5.4 LTS installed (you have this!)
- Your blueprint: `blueprints/classified/ARCH/07-Proposed-FloorPlan.jpg`

---

## 📋 **STEP 1: Initial Setup**

### A. Close Splash Screen
- Click **"Continue"** on the Quick Setup dialog

### B. Delete Default Objects
1. Click the **Cube** in the center (turns orange)
2. Press **X** on keyboard
3. Select **"Delete"**

4. Click the **Light** (above where cube was)
5. Press **X** → Delete

6. Keep the **Camera** (we'll need it later)

---

## 📐 **STEP 2: Enable Import Add-on**

### Enable "Import Images as Planes"
1. Go to **Edit → Preferences** (top menu)
2. Click **Add-ons** tab (left side)
3. In search box, type: **"Import Images"**
4. Check the box next to **"Import Images as Planes"**
5. Close Preferences window

---

## 📥 **STEP 3: Import Your Blueprint**

### A. Import the Floor Plan Image
1. **File → Import → Images as Planes**
2. Navigate to: `/Users/invinciblelude/728 Cordant project/blueprints/classified/ARCH/`
3. Select: **07-Proposed-FloorPlan.jpg**
4. Click **"Import Images as Planes"** (bottom right)

### B. Position the Blueprint
- The image will appear in the 3D view
- Press **Numpad 7** (or View → Viewpoint → Top) to see top-down view
- Your blueprint should now be flat on the ground plane

---

## 📏 **STEP 4: Scale the Blueprint to Real Size**

Your blueprint scale is **1/4" = 1'-0"** (means every 1/4 inch on paper = 1 foot in real life)

### A. Switch to Edit Mode
1. Make sure the blueprint plane is selected (orange outline)
2. Press **Tab** to enter Edit Mode

### B. Scale the Image
We need to scale it so dimensions match reality.

1. Press **S** (for Scale)
2. Type: **48** (because 1/4" scale × 4 = 1" per foot × 12 inches = 48)
3. Press **Enter**

### C. Return to Object Mode
- Press **Tab** to exit Edit Mode

---

## 🧱 **STEP 5: Start Drawing Walls**

Now we'll trace walls on top of the blueprint.

### A. Add a Cube (We'll Turn it Into a Wall)
1. Press **Shift + A** (Add menu)
2. Select **Mesh → Cube**
3. A cube appears at center

### B. Scale it to Wall Dimensions
Exterior walls are **2x6 studs = 6 inches thick = 0.5 feet**
Wall height = **8 feet**

1. Press **S** then **X** (scale X-axis only) → type **0.5** → Enter (makes it 6" thick)
2. Press **S** then **Y** (scale Y-axis) → type **10** → Enter (makes it 10' long for now)
3. Press **S** then **Z** (scale Z-axis) → type **8** → Enter (makes it 8' tall)

### C. Move the Wall to Blueprint Starting Point
1. Press **G** (for Grab/Move)
2. Use mouse to position wall over a wall line on your blueprint
3. Click to place

---

## 🎨 **STEP 6: Make Blueprint Semi-Transparent**

So you can see walls on top of blueprint:

1. Click the blueprint plane
2. In right panel, find **Material Properties** (pink sphere icon)
3. Under **Base Color**, reduce **Alpha** slider to **0.5**

Now you can see both the blueprint and your 3D walls!

---

## 🔄 **STEP 7: Duplicate Walls**

To create more walls:

1. Select a wall (click it)
2. Press **Shift + D** (Duplicate)
3. Press **G** to move
4. Press **R** then **Z** then **90** to rotate 90° (for perpendicular walls)

---

## 🎯 **USEFUL SHORTCUTS**

| Key | Action |
|-----|--------|
| **G** | Move (Grab) |
| **R** | Rotate |
| **S** | Scale |
| **X** | Delete |
| **Tab** | Toggle Edit/Object Mode |
| **Shift + A** | Add Object |
| **Shift + D** | Duplicate |
| **Numpad 7** | Top View |
| **Numpad 1** | Front View |
| **Numpad 3** | Side View |
| **Middle Mouse** | Rotate View |
| **Scroll Wheel** | Zoom |

---

## 🏠 **STEP 8: Trace Your Entire House**

Now repeat the wall creation process for each wall on your blueprint:

### Reference Dimensions from Blueprint:
- **BEDROOM 2**: 14'-4" × 10'-8"
- **BEDROOM 3**: 14'-4" × 10'-8"
- **GREAT ROOM**: 24'-2" × 19'-8" (VAULTED CEILING)
- **KITCHEN**: 14'-6" × 17'-4"
- **MASTER BEDROOM**: 15'-6" × 14'-8"
- **MASTER BATH**: 14'-2" × 13'-4"
- **OFFICE**: 12'-8" × 11'-4"

### Wall Specifications:
- **Exterior walls**: 6" thick (2x6 studs)
- **Interior walls**: 4.5" thick (2x4 studs)
- **Standard height**: 8'-0"
- **Great Room**: VAULTED (scale Z to 14' or more)

---

## 🎬 **STEP 9: View Your 3D Model**

Once walls are traced:

1. Press **Numpad 0** to see Camera View
2. Press **Z** → Select **"Material Preview"** (to see textures)
3. Use middle mouse button to orbit around your house

---

## 💾 **STEP 10: Save Your Work**

1. **File → Save As**
2. Save to: `/Users/invinciblelude/728 Cordant project/`
3. Name it: **728-Cordant-3D-Model.blend**

---

## 🆘 **TROUBLESHOOTING**

### "I can't see the blueprint after importing"
- Press **Numpad 7** for top view
- Scroll out with mouse wheel

### "My walls are the wrong size"
- Select the wall
- Press **S** (scale), then **X**, **Y**, or **Z** for specific axis
- Type the number, press Enter

### "I accidentally deleted something"
- Press **Ctrl + Z** to undo

### "Blender feels confusing"
- This is normal! Blender has a learning curve
- Focus on just these tools: G (move), S (scale), R (rotate)
- The blueprint helps guide you

---

## 🎯 **NEXT STEPS AFTER WALLS**

Once all walls are traced:

1. **Add Roof** (using your Roof Framing Plan - Sheet S-3)
2. **Add Windows/Doors** (from your Window Schedule)
3. **Add Materials** (stucco, wood, etc.)
4. **Render** final images

---

## 🏆 **YOU'RE READY!**

Start with **Step 1** and work through each section. Take your time - this is a complex house with angled walls.

**Don't try to do it all at once!** Just focus on getting one room's walls right first (like the OFFICE - it's rectangular and simple).

Good luck! 🚀


