# 728 Cortlandt Drive - Construction Management System

## 🎯 Overview
This is a comprehensive construction management system for the 728 Cortlandt Drive project. It provides a structured workflow from project overview → task management → detailed SOPs → blueprint reference.

## 📱 Navigation Flow

```
Dashboard (index.html)
   ↓
   Shows all projects as cards
   Click a project →
   
Project Detail (project.html)
   ↓
   Shows all tasks organized by trade
   Click a task →
   
Task SOP (sops/[TASK-ID].html)
   ↓
   Detailed step-by-step instructions
   Materials, tools, safety, QC checks
   Links to related blueprint pages →
   
Blueprint Viewer (blueprints.html)
   Shows blueprint images by category
```

## 🏗️ Key Features

### 1. **Projects Dashboard** (`index.html`)
- View all construction projects
- See progress, status, and key metrics
- Click to drill into project details

### 2. **Project Tasks** (`project.html`)
- All tasks organized by trade (Foundation, Framing, Electrical, etc.)
- Filter by status or search
- See crew size, duration, and prerequisites
- Click any task to view its SOP

### 3. **Task SOPs** (`sops/`)
- 18 detailed Standard Operating Procedures
- Each includes:
  - **Prerequisites**: What must be done first
  - **Materials**: Exact items needed with specs
  - **Tools**: Required equipment
  - **Safety**: PPE and hazard warnings
  - **Step-by-Step Instructions**: Numbered, detailed steps
  - **QC Checks**: Quality control checkpoints
  - **Inspections**: Required inspection milestones
  - **Blueprint Links**: Direct links to relevant sheets

### 4. **Blueprint Viewer** (`blueprints.html`)
- All 27 pages from PDF extracted and organized
- Filter by category (Architectural, Plumbing, Civil, etc.)
- Click to view full-size image
- Searchable by sheet number or title

### 5. **Schedule** (`schedule/baseline.html`)
- Baseline schedule with all phases
- 3-week rolling lookahead
- Tracks crew allocation and hours

## 📊 Project Data

**Project**: 728 Cortlandt Drive  
**Total Tasks**: 18  
**Total Estimated Hours**: 484 hours  
**Crew Size**: 7 people  
**Work Schedule**: Monday-Friday, 7:30 AM - 4:00 PM  

### Trades Covered:
- Site & Civil (2 tasks, 24 hours)
- Foundation (3 tasks, 64 hours)
- Framing (4 tasks, 156 hours)
- Roofing (3 tasks, 72 hours)
- Electrical (2 tasks, 64 hours)
- Plumbing (3 tasks, 72 hours)
- HVAC (1 task, 32 hours)

## 🎨 Design Features

- **Dark Theme**: Easy on the eyes for outdoor/bright conditions
- **Mobile-First**: Optimized for phones and tablets
- **Offline Support**: PWA with service worker
- **Bottom Navigation**: Consistent across all pages
- **FAB Button (🎤)**: Quick problem logging
- **Online/Offline Indicator**: Shows connectivity status

## 🚀 Local Preview

```bash
python3 -m http.server 8088 --directory docs
```

Then open: http://127.0.0.1:8088

## 📦 File Structure

```
docs/
├── index.html              # Projects dashboard (main entry)
├── project.html            # Project tasks list
├── blueprints.html         # Blueprint viewer
├── sops/                   # Individual task SOPs
│   ├── SITE-001.html
│   ├── FOUND-001.html
│   ├── FRAME-001.html
│   └── ... (18 total)
├── schedule/
│   ├── baseline.html       # Gantt chart
│   └── lookahead.html      # 3-week lookahead
├── assets/
│   ├── blueprint_data.json  # Extracted blueprint metadata
│   ├── project_tasks.json   # All tasks and SOPs
│   └── shared-nav.js        # Common navigation UI
└── blueprints/
    └── classified/          # Organized blueprint images
        ├── ARCH/
        ├── CIVIL/
        ├── MEP/PLUMB/
        └── _unmatched/
```

## 🛠️ Tools Used

- **PyMuPDF**: PDF text extraction
- **Python**: Blueprint analysis and classification
- **Vanilla JavaScript**: No frameworks, fast and simple
- **CSS Grid/Flexbox**: Responsive layouts
- **Service Workers**: Offline support

## 📝 Next Steps

1. **Update Task Status**: As you complete tasks, mark them in localStorage
2. **Add Photos**: Attach progress photos to tasks
3. **Log Problems**: Use FAB button to quickly log issues
4. **Review SOPs**: Before starting any task, review its SOP
5. **Check Blueprints**: Reference relevant sheets during work

---

**Built for**: Foreman & Crew  
**Project**: 728 Cortlandt Drive  
**Last Updated**: October 26, 2025

