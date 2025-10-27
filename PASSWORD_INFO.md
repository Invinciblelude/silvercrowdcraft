# 🔒 Site Password Protection

## Current Password

**Password:** `SilverCrowd2024`

## How It Works

- Password is required to access any page on the site
- After entering the password correctly, you stay logged in for **24 hours**
- Password is stored in browser's localStorage (local device only)
- Authentication expires after 24 hours of inactivity

## Protected Pages

✅ All main pages are password protected:
- Dashboard (index.html)
- Project Tasks (project.html)
- Blueprints (blueprints.html)
- Changelog (changelog.html)
- Baseline Schedule
- Lookahead Schedule

## How to Change the Password

1. Open the file: `docs/auth.js`
2. Find this line (around line 8):
   ```javascript
   const SITE_PASSWORD = 'SilverCrowd2024';
   ```
3. Change `'SilverCrowd2024'` to your new password
4. Save and commit to GitHub

## How to Logout

Users can manually log out by:
1. Opening browser console (F12)
2. Typing: `siteLogout()`
3. Or just clear browser localStorage/cookies

## Security Notes

⚠️ **Important:** This is client-side password protection (browser-based). It's good for keeping casual visitors out, but:
- The password is visible in the source code
- Someone with technical knowledge can bypass it
- For high-security needs, use server-side authentication

✅ **Best for:** Private construction sites, internal team access, keeping unauthorized workers out

## For Workers

Share this password with your construction crew:
**Password:** `SilverCrowd2024`

They'll need to enter it once, then they're good for 24 hours on that device.

