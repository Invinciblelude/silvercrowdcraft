# 728 Cordant Drive — Construction Management System

A complete, field-ready project management dashboard for residential construction, built from actual PDF blueprints.

## Features

✅ **5-Minute Morning Huddle Dashboard** — Single-screen view of critical tasks, inspections, and material arrivals  
✅ **Blueprint Viewer** — Organized by trade (ARCH, STRUCT, MEP/ELEC, CIVIL, DETAILS)  
✅ **Task Dashboard** — 103 tasks with crew, hours, QC checklists, and Definition of Done  
✅ **SOPs & Printables** — One-page field guides for every phase (Site Prep → Closeout)  
✅ **Baseline Schedule** — Gantt chart for 7-person crew, 40 hrs/week  
✅ **3-Week Lookahead** — Rolling schedule updated weekly  
✅ **Per-Task SOPs** — Installation requirements, materials, steps, inspections, safety  
✅ **Offline-First PWA** — Works without internet, syncs when reconnected  
✅ **Problem Logger** — Voice notes attached to tasks, queued for sync  
✅ **Safety-First Design** — PPE requirements and hazard warnings on every screen  

## Local Preview

```bash
cd /Users/invinciblelude/728\ Cordant\ project
python3 -m http.server 8088 --directory docs
```

Open http://127.0.0.1:8088/

## Deploy to GitHub Pages

### 1. Initialize Git (if not already done)

```bash
cd /Users/invinciblelude/728\ Cordant\ project
git init
git add -A docs
git commit -m "Initial commit: construction management system"
```

### 2. Create GitHub Repository

Go to https://github.com/new and create a **public** repository named `728-cordant` (or any name).

### 3. Connect and Push

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git remote add origin git@github.com:YOUR_USERNAME/728-cordant.git
git branch -M main
git push -u origin main
```

### 4. Enable GitHub Pages

1. Go to your repo on GitHub → **Settings** → **Pages**
2. Under **Source**, select branch: `main`, folder: `/docs`
3. Click **Save**

Your site will be live at:  
`https://YOUR_USERNAME.github.io/728-cordant/`

## File Structure

```
/Users/invinciblelude/728 Cordant project/
├── blueprints/
│   ├── incoming/          # Original PDFs
│   ├── classified/        # Auto-sorted JPEGs by trade
│   └── _unmatched/        # Pages needing manual classification
├── tools/
│   └── index_blueprints.py  # Classifier script
├── site/                  # Development version
└── docs/                  # Production (GitHub Pages)
    ├── index.html         # Blueprint browser
    ├── tasks.html         # Task dashboard
    ├── schedule/
    │   ├── baseline.html  # Gantt chart
    │   └── lookahead.html # 3-week rolling schedule
    ├── printables/        # One-page SOPs
    ├── task_sops/         # Detailed per-task instructions
    ├── blueprints/        # Classified images
    └── assets/
        ├── index.json     # Blueprint metadata
        └── pdf_extract.json  # Extracted text from PDFs
```

## Workflow

### Add New PDF Plans

1. Place PDFs in `blueprints/incoming/`
2. Run:
   ```bash
   python3 -m pip install PyMuPDF pdfminer.six --quiet
   python3 /Users/invinciblelude/728\ Cordant\ project/tools/convert_classify.py
   ```
3. Sync to docs:
   ```bash
   rsync -av --delete blueprints/classified/ docs/blueprints/classified/
   rsync -av --delete blueprints/_unmatched/ docs/blueprints/_unmatched/
   ```
4. Rebuild index:
   ```bash
   python3 /Users/invinciblelude/728\ Cordant\ project/tools/rebuild_index.py
   ```
5. Push to GitHub:
   ```bash
   git add -A docs
   git commit -m "Update blueprints"
   git push
   ```

### Update Tasks or Schedule

- Edit `docs/tasks.json` or `docs/schedule/*.html`
- Commit and push:
  ```bash
  git add -A docs
  git commit -m "Update tasks/schedule"
  git push
  ```

## Tech Stack

- **Frontend**: Vanilla HTML/CSS/JS (no build step)
- **PDF Processing**: PyMuPDF (fitz), pdfminer.six
- **Hosting**: GitHub Pages (free, SSL, custom domain support)
- **Classification**: Regex-based text extraction + keyword matching

## Credits

Built for a 7-person crew to frame and finish a single-family residence in ~14 weeks (Oct 27, 2025 → Feb 2026).

---

**Live Preview**: http://127.0.0.1:8088/ (local)  
**GitHub Pages**: https://YOUR_USERNAME.github.io/728-cordant/ (after deploy)

