# 728 Cordant Blueprint Site

This folder is ready for GitHub Pages.

## Deploy
1. Create a new GitHub repo and commit/push this project.
2. In GitHub: Settings → Pages → Build and deployment:
   - Source: Deploy from a branch
   - Branch: main, Folder: /docs
3. Wait for the Pages build, then open the URL shown.

## Local preview
```bash
python3 -m http.server 8088 --directory "$(pwd)/docs"
```

## Notes
- Images are served from `docs/blueprints`.
- Tasks Dashboard saves status locally in your browser (localStorage).
- To add OCR later: install Tesseract and run `tools/extract_text.py`, then copy updated `site/assets/ocr.json` to `docs/assets/ocr.json` and commit.
