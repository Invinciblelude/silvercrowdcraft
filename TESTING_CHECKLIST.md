# 🧪 Site Testing Checklist

Test your site after the update (2-3 minutes after push)

## 🔒 Password Protection Test

### Test 1: Login Screen
- [ ] Go to https://silvercrowdcraft.com
- [ ] You should see a password screen with 🔒 icon
- [ ] Enter password: `SilverCrowd2024`
- [ ] Click "🔓 Unlock Site"
- [ ] You should see the dashboard

### Test 2: Wrong Password
- [ ] Open site in incognito/private window
- [ ] Enter wrong password like "test123"
- [ ] You should see: "❌ Incorrect password. Please try again."
- [ ] The login box should shake

### Test 3: Stay Logged In
- [ ] After successful login, refresh the page
- [ ] You should NOT see the password screen again
- [ ] You stay logged in for 24 hours

### Test 4: Other Pages
- [ ] Navigate to Project Tasks
- [ ] Navigate to Blueprints
- [ ] Navigate to Changelog
- [ ] All should be accessible without re-entering password

## 📷 Photo Upload Test

### Test 5: Upload a Photo
- [ ] Go to Project Tasks page
- [ ] Find task "01-DEMO-001 - Demo Existing Fences"
- [ ] Click the "📷 Photo" button
- [ ] Select an image from your device
- [ ] Add a note (optional) like "Test photo"
- [ ] Click OK
- [ ] You should see: "✅ Photo uploaded successfully!"

### Test 6: View Photo
- [ ] After upload, the photo button should show "📷 Photo (1)"
- [ ] A 100x100px thumbnail should appear below the task
- [ ] Hover over thumbnail - it should grow slightly
- [ ] Click the thumbnail to view full-size

### Test 7: Multiple Photos
- [ ] Upload 2-3 more photos to the same task
- [ ] Button should show "📷 Photo (3)" etc.
- [ ] All thumbnails should appear in a row
- [ ] Click each to verify full-size view works

### Test 8: Photo Persistence
- [ ] Refresh the page
- [ ] Photos should still be there
- [ ] Photo count should remain correct

## 📝 Notes Test

### Test 9: Add Multiple Notes
- [ ] Click "📝 Note" on any task
- [ ] Add note: "First test note"
- [ ] Click "📝 Note" again
- [ ] Add note: "Second test note"
- [ ] You should see "📝 Notes (2)" section
- [ ] Each note should have a timestamp

### Test 10: Notes Persistence
- [ ] Refresh the page
- [ ] Both notes should still be there
- [ ] Timestamps should be preserved

## 🎥 YouTube Search Bar Test

### Test 11: YouTube Search
- [ ] Open any SOP (e.g., 01-DEMO-001)
- [ ] Scroll to "🎥 Search YouTube Tutorials" section
- [ ] Click "🔍 Search" button
- [ ] YouTube results should appear in iframe below
- [ ] Try modifying search and clicking "🔍 Search" again

### Test 12: No Hardcoded Videos
- [ ] Scroll through the SOP
- [ ] Verify NO section called "🎓 Training Videos - Learn the Skills"
- [ ] Verify NO hardcoded video cards with titles like "Proper Use of PPE"

## ✅ Quality Control Test

### Test 13: QC Section Present
- [ ] In any SOP, verify "✅ Quality Control Checks" section exists
- [ ] Checklist items should be visible
- [ ] Section should be cleanly formatted

## 🧪 Browser Tests

### Test 14: Different Browsers
Test on at least 2 browsers:
- [ ] Chrome/Edge
- [ ] Safari
- [ ] Firefox
- [ ] Mobile browser (iPhone/Android)

### Test 15: Mobile Responsive
- [ ] Open on phone
- [ ] Password screen should look good
- [ ] Photo upload should work
- [ ] Tasks should be readable
- [ ] Navigation should work

## 🚨 What to Report

If anything doesn't work:
1. Take a screenshot
2. Note which browser you're using
3. Check browser console (F12) for errors
4. Let me know and I'll fix it!

## ✅ Success Criteria

All tests should pass:
- ✅ Password protection works
- ✅ Photos upload and display
- ✅ Multiple notes work
- ✅ YouTube search bar works
- ✅ No hardcoded videos
- ✅ QC sections intact
- ✅ Everything persists after refresh

---

**Last Updated:** October 27, 2025  
**Site Version:** v2.0 with Password Protection  
**Password:** SilverCrowd2024

