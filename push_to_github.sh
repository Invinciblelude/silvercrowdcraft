#!/bin/bash
# Push to GitHub - Run this script to update your repository

echo "🚀 Pushing to GitHub..."
echo ""

cd "/Users/invinciblelude/728 Cordant project"

# Show what will be pushed
echo "📋 Commits to push:"
git log origin/main..main --oneline 2>/dev/null || git log --oneline -3

echo ""
echo "Attempting to push..."

# Try to push
git push origin main 2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "🌐 View at: https://github.com/Invinciblelude/silvercrowdcraft"
else
    echo ""
    echo "❌ Push failed. Authentication needed."
    echo ""
    echo "📱 EASIEST METHOD: Use GitHub Desktop"
    echo "   1. Download: https://desktop.github.com/"
    echo "   2. Add this repository"
    echo "   3. Click 'Push origin'"
    echo ""
    echo "💻 OR: Create Personal Access Token"
    echo "   1. Go to: https://github.com/settings/tokens"
    echo "   2. Generate new token (classic)"
    echo "   3. Select 'repo' scope"
    echo "   4. Run:"
    echo "      git push https://YOUR_TOKEN@github.com/Invinciblelude/silvercrowdcraft.git main"
fi


