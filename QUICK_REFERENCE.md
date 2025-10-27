# 🚀 Quick Reference Card

## 📍 Important URLs

| Resource | URL |
|----------|-----|
| **Live Site** | https://silvercrowdcraft.com |
| **GitHub Repo** | https://github.com/Invinciblelude/silvercrowdcraft |
| **GitHub Pages Settings** | https://github.com/Invinciblelude/silvercrowdcraft/settings/pages |
| **Actions/Deployments** | https://github.com/Invinciblelude/silvercrowdcraft/actions |

---

## 💻 Quick Commands

### **Navigate to Project**
```bash
cd "/Users/invinciblelude/728 Cordant project"
```

### **Check Status**
```bash
git status
git log --oneline -5
```

### **Save Your Work**
```bash
git add -A
git commit -m "Your descriptive message here"
git push origin main
```

### **Create Backup**
```bash
# Quick backup to Desktop
zip -r ~/Desktop/backup-$(date +%Y%m%d).zip "728 Cordant project"
```

### **View Site Locally**
```bash
cd docs
python3 -m http.server 8088
# Then open: http://localhost:8088
```

---

## 📦 Backup Locations

✅ **GitHub** (Primary): https://github.com/Invinciblelude/silvercrowdcraft  
✅ **Local**: `/Users/invinciblelude/728 Cordant project/`  
✅ **Desktop**: `~/Desktop/silvercrowdcraft-COMPLETE-*.zip`  

---

## 🔧 Common Tasks

### **Update the Site**
1. Make your changes locally
2. Run: `git add -A`
3. Run: `git commit -m "Describe changes"`
4. Run: `git push origin main`
5. Wait 2-3 minutes for GitHub to rebuild

### **Add More Training Videos**
1. Edit: `tools/add_training_videos_to_sops.py`
2. Add videos to `TRAINING_VIDEOS` dictionary
3. Run: `python3 tools/add_training_videos_to_sops.py`
4. Commit and push changes

### **Add New Tasks**
1. Edit: `docs/assets/real_construction_plan.json`
2. Add task object with all required fields
3. Run task generator if needed
4. Commit and push changes

### **Update Blueprints**
1. Add images to: `docs/blueprints/classified/`
2. Run: `python3 tools/rebuild_blueprint_index.py`
3. Commit and push changes

---

## 📊 System Status Dashboard

**Current Version**: v1.0.1  
**Last Updated**: October 27, 2025  
**Status**: 🟢 Production  

**Features**:
- ✅ 122 Tasks with SOPs
- ✅ 366+ Training Videos
- ✅ 34 Blueprint Sheets
- ✅ Photo Upload
- ✅ Task Tracking
- ✅ Search Functionality
- ✅ Offline PWA

---

## 🚨 Troubleshooting

### **Site Not Loading?**
1. Hard refresh: `Cmd + Shift + R`
2. Try incognito/private window
3. Check: https://github.com/Invinciblelude/silvercrowdcraft/actions
4. Wait 2-3 minutes after pushing changes

### **Changes Not Showing?**
1. Verify files committed: `git status`
2. Check pushed to GitHub: `git log origin/main..main`
3. Wait for GitHub rebuild (2-3 min)
4. Clear browser cache

### **Videos Not Showing?**
1. Check file has videos: `grep "Training Videos" docs/sops/01-DEMO-001.html`
2. Verify pushed to GitHub
3. Wait for rebuild
4. Hard refresh browser

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview and features |
| `VERSION_HISTORY.md` | Complete version history |
| `CHANGELOG.md` | User-facing changes log |
| `SESSION_SUMMARY.md` | Detailed session notes |
| `HOW_TO_SAVE_AND_BACKUP.md` | Backup procedures |
| `QUICK_REFERENCE.md` | This file - quick lookup |

---

## 🎯 Key Numbers

- **Total Tasks**: 122
- **Total Hours**: 5,536
- **Training Videos**: 366+
- **Blueprint Sheets**: 34
- **SOP Pages**: 122
- **Git Commits**: 12
- **Project Size**: 172 MB

---

## 📞 Emergency Contacts

**Repository**: https://github.com/Invinciblelude/silvercrowdcraft  
**Issues**: Create at https://github.com/Invinciblelude/silvercrowdcraft/issues  
**Email**: SilverCrowdCraft@gmail.com  
**Phone**: 916-634-2083  

---

## 💡 Pro Tips

1. **Always commit before major changes**
2. **Use descriptive commit messages**
3. **Tag important versions** (`git tag v1.0.1`)
4. **Backup before big updates**
5. **Test locally first** (python server)
6. **Hard refresh after deployments**
7. **Check Actions for build errors**
8. **Keep documentation updated**

---

## 🎉 Quick Wins

**Show Training Videos**:
```
https://silvercrowdcraft.com/sops/01-DEMO-001.html
Scroll down to "🎓 Training Videos"
```

**View All Tasks**:
```
https://silvercrowdcraft.com/project.html
Search for any task
```

**Browse Blueprints**:
```
https://silvercrowdcraft.com/blueprints.html
Filter by category
```

---

**🚀 You're all set! Everything is saved, backed up, and deployed!**

