# 🏗️ Construction Management System - JSDOM (Job-Site Digital Operating Manual)

> **A comprehensive, mobile-first construction project management system built from architectural blueprints**

[![Live Demo](https://img.shields.io/badge/Live-Demo-blue)](https://invinciblelude.github.io/silvercrowdcraft)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Overview

This is a **complete digital construction management system** for a 3,200 SF residential addition project. Built from actual architectural blueprints, it provides:

- **122 detailed construction tasks** organized by phase
- **5,536 total estimated hours** with realistic crew sizes
- **122 Standard Operating Procedures (SOPs)** with step-by-step instructions
- **34 architectural blueprint sheets** classified and indexed
- **Real-time progress tracking** with photo uploads and notes
- **Offline-first Progressive Web App (PWA)** for job site use
- **Mobile-responsive design** optimized for tablets and phones

---

## ✨ Key Features

### 📊 **Projects Dashboard**
- Project overview with key metrics
- Total tasks, hours, and completion tracking
- Quick access to all project modules

### 📋 **Task Management**
- Tasks organized by construction phase (Site Prep → Final Walkthrough)
- Status tracking: Pending, In Progress, Complete
- Search functionality across task names, IDs, phases, and blueprint references
- Quick complete buttons for field updates
- Estimated hours and crew size for each task

### 📐 **Blueprint Viewer**
- 34 high-resolution blueprint sheets
- Categorized: ARCH, STRUCT, MEP/ELEC, GENERAL
- Filter by category and search by sheet number or title
- Direct links from tasks to relevant blueprint pages

### 📝 **Standard Operating Procedures (SOPs)**
- Detailed instructions for every task
- Materials list with specifications
- Required tools and equipment
- Safety requirements and PPE
- Step-by-step execution instructions
- Quality control checklists
- Direct blueprint references

### 📸 **Progress Tracking**
- Photo upload for task documentation
- Notes and comments per task
- Changelog tracking all updates
- Timestamp and task reference for all changes
- Stored locally using browser localStorage

### 📅 **Project Schedule**
- Gantt chart visualization (baseline plan)
- Task dependencies and critical path
- Start/end dates for all 122 tasks
- Duration estimates based on crew size

---

## 🚀 Live Demo

**Visit the live site:** [https://invinciblelude.github.io/silvercrowdcraft](https://invinciblelude.github.io/silvercrowdcraft)

---

## 🛠️ Technology Stack

### **Frontend**
- Pure HTML5, CSS3, JavaScript (ES6+)
- No framework dependencies - lightweight and fast
- Progressive Web App (PWA) with Service Worker
- LocalStorage for offline data persistence
- CSS Grid and Flexbox for responsive layouts

### **Blueprint Processing**
- Python 3.x with PyMuPDF (fitz)
- PDF text extraction and image conversion
- Automated classification and indexing
- 300 DPI JPEG output for quality

### **Data Management**
- JSON-based data structure
- Automated task generation from blueprints
- Blueprint-to-task relationship mapping
- Realistic construction sequencing

---

## 📁 Project Structure

```
silvercrowdcraft/
├── docs/                          # Main web application
│   ├── index.html                 # Projects dashboard
│   ├── project.html               # Task list and management
│   ├── blueprints.html            # Blueprint viewer
│   ├── changelog.html             # Activity log
│   ├── schedule/
│   │   └── baseline.html          # Gantt chart schedule
│   ├── sops/                      # 122 SOP pages
│   │   ├── SOP-001.html          # Site Mobilization
│   │   ├── SOP-002.html          # Tree Protection
│   │   └── ...                    # (120 more SOPs)
│   ├── assets/
│   │   ├── blueprint_data.json    # Blueprint index
│   │   ├── real_construction_plan.json  # Task data
│   │   └── shared-nav.js          # Navigation component
│   └── blueprints/
│       └── classified/            # 34 blueprint images
│           ├── 01-General-CoverSheet.jpg
│           ├── 02-AsBuilt-SitePlan.jpg
│           └── ...
├── tools/                         # Python processing scripts
│   ├── generate_tasks_and_sops.py # Main task generator
│   ├── index_blueprints.py        # Blueprint indexer
│   └── rebuild_blueprint_index.py # Index rebuilder
├── blueprints/                    # Source blueprint PDFs
│   ├── classified/                # Organized blueprint images
│   └── original/                  # Original PDF files
└── README.md                      # This file
```

---

## 🔧 Setup & Installation

### **Running Locally**

1. **Clone the repository**
```bash
git clone https://github.com/Invinciblelude/silvercrowdcraft.git
cd silvercrowdcraft
```

2. **Serve the docs folder**
```bash
# Using Python
python3 -m http.server 8088 --directory docs

# Or using Node.js
npx serve docs

# Or using PHP
php -S localhost:8088 -t docs
```

3. **Open in browser**
```
http://localhost:8088
```

### **Blueprint Processing (Optional)**

If you need to regenerate tasks or reindex blueprints:

```bash
# Install Python dependencies
pip install PyMuPDF pillow

# Regenerate tasks and SOPs
python3 tools/generate_tasks_and_sops.py

# Rebuild blueprint index
python3 tools/rebuild_blueprint_index.py
```

---

## 📊 Project Data

### **Task Breakdown by Phase**

| Phase | Tasks | Hours | Key Activities |
|-------|-------|-------|----------------|
| **Site Preparation** | 8 | 312 | Mobilization, utilities, temp facilities |
| **Foundation** | 15 | 624 | Footings, concrete, waterproofing |
| **Framing** | 22 | 1,168 | Floor, wall, roof framing |
| **Rough-Ins** | 18 | 936 | MEP systems installation |
| **Exterior Envelope** | 12 | 728 | Roofing, siding, windows, doors |
| **Insulation & Drywall** | 8 | 520 | Insulation, drywall, taping |
| **Interior Finishes** | 24 | 832 | Flooring, cabinets, trim, paint |
| **MEP Trim-Out** | 9 | 312 | Fixtures, devices, final connections |
| **Final Details** | 6 | 104 | Cleanup, punch list, walkthrough |
| **TOTAL** | **122** | **5,536** | **~6 months** (4 crew) |

### **Blueprint Organization**

| Category | Sheets | Description |
|----------|--------|-------------|
| **GENERAL** | 3 | Cover, notes, site plans |
| **ARCH** | 12 | Floor plans, elevations, details |
| **STRUCT** | 14 | Foundation, framing, engineering |
| **MEP/ELEC** | 5 | Mechanical, electrical, plumbing |
| **TOTAL** | **34** | Complete construction documents |

---

## 💾 Data Storage

### **Client-Side Storage**
- Task states (status: pending/in-progress/complete)
- Photo uploads (base64 encoded)
- Task notes and comments
- Changelog entries
- All stored in browser `localStorage`
- Persists across sessions
- No server required

### **Data Format**
```javascript
// Task state example
{
  "SOP-045": {
    "status": "in-progress",
    "photos": ["data:image/jpeg;base64,..."],
    "notes": "North wall framing complete, waiting on inspection"
  }
}

// Changelog entry example
{
  "timestamp": "2025-10-27T10:30:00",
  "taskId": "SOP-045",
  "taskName": "First Floor Wall Framing",
  "type": "status",
  "change": "Updated to in-progress"
}
```

---

## 🎯 Use Cases

### **For Project Managers**
- Track overall project progress
- Monitor task completion rates
- Review photo documentation
- Generate progress reports from changelog

### **For Foremen**
- Access SOPs in the field (offline capable)
- Mark tasks complete on mobile device
- Upload progress photos immediately
- Add notes for crew coordination

### **For Crew Members**
- View detailed work instructions
- Check material and tool requirements
- Review safety protocols
- Reference blueprints on-site

### **For Inspectors**
- Review QC checklists
- Verify code compliance items
- Check blueprint references
- View progress photos

---

## 🔐 Security & Privacy

- **No server-side storage** - all data stored locally
- **No user tracking** - no analytics or cookies
- **No external dependencies** - all resources self-hosted
- **Offline capable** - works without internet connection
- **Open source** - transparent and auditable code

---

## 🚀 Deployment

### **GitHub Pages (Current)**

Already deployed at: https://invinciblelude.github.io/silvercrowdcraft

To redeploy after changes:
```bash
git add .
git commit -m "Update project"
git push origin main
```

### **Alternative Hosting Options**

- **Netlify**: Connect GitHub repo for auto-deploy
- **Vercel**: Import from GitHub with zero config
- **AWS S3**: Static website hosting
- **Azure Static Web Apps**: Free tier available

---

## 📱 Mobile Support

- **Responsive design** - adapts to all screen sizes
- **Touch-optimized** - large buttons and tap targets
- **PWA support** - add to home screen
- **Offline mode** - Service Worker caching
- **Photo upload** - camera integration
- **Vertical sidebar** on desktop, bottom tabs on mobile

---

## 🤝 Contributing

Contributions are welcome! This system can be adapted for:
- Different project types (commercial, industrial)
- Other construction trades
- Renovation vs. new construction
- Different project sizes

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- Built for real-world construction management
- Designed for offline field use
- Optimized for mobile devices
- Created with builder feedback

---

## 📞 Contact

**Project Repository**: [https://github.com/Invinciblelude/silvercrowdcraft](https://github.com/Invinciblelude/silvercrowdcraft)

**Issues & Feedback**: [GitHub Issues](https://github.com/Invinciblelude/silvercrowdcraft/issues)

---

## 🗺️ Roadmap

### **Planned Features**
- [ ] User authentication for multi-user teams
- [ ] Cloud sync for cross-device access
- [ ] PDF report generation
- [ ] Real-time collaboration
- [ ] Integration with project management tools
- [ ] Time tracking per task
- [ ] Material cost tracking
- [ ] Weather integration for scheduling
- [ ] Push notifications for task updates

### **Current Version**
- ✅ 122 tasks with detailed SOPs
- ✅ 34 blueprint sheets indexed
- ✅ Photo upload and notes
- ✅ Changelog tracking
- ✅ Search functionality
- ✅ Mobile-responsive design
- ✅ Offline PWA capability

---

**Built with ❤️ for construction professionals**
