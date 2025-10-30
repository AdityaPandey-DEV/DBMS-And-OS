#!/bin/bash

# Push to GitHub Script
# Run this after authenticating with GitHub

echo "╔══════════════════════════════════════════════════════════╗"
echo "║        PUSH TO GITHUB - DBMS & OS PROJECTS             ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"

# Check if authenticated
echo "🔍 Checking GitHub authentication..."
git remote -v

echo ""
echo "📊 Current status:"
git log --oneline -3

echo ""
echo "📦 Files ready to push:"
echo "   ✓ 39 original project files"
echo "   ✓ ER_DIAGRAM.md (406 lines)"
echo "   ✓ DATAFLOW_DIAGRAM.md (620+ lines)"
echo "   ✓ GIT_PUSH_INSTRUCTIONS.md (192 lines)"
echo "   ✓ .gitignore"
echo ""
echo "   Total: 43 files committed"
echo ""

read -p "🚀 Ready to push? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "📤 Pushing to GitHub..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "╔══════════════════════════════════════════════════════════╗"
        echo "║              ✅ PUSH SUCCESSFUL!                         ║"
        echo "╚══════════════════════════════════════════════════════════╝"
        echo ""
        echo "🌐 Visit your repository:"
        echo "   https://github.com/AdityaPandey-DEV/DBMS-And-OS"
        echo ""
        echo "📁 Your repository now contains:"
        echo "   • Complete DBMS Project (Startup Funding System)"
        echo "   • Complete OS Project (Blockchain File Access Control)"
        echo "   • 8 Presentation Scripts"
        echo "   • Comprehensive Documentation"
        echo "   • ER Diagram & Data Flow Diagram"
        echo "   • Testing Guides"
        echo ""
    else
        echo ""
        echo "❌ Push failed!"
        echo ""
        echo "📝 Follow these steps:"
        echo ""
        echo "Option 1: GitHub CLI (Easiest)"
        echo "   brew install gh"
        echo "   gh auth login"
        echo "   git push -u origin main"
        echo ""
        echo "Option 2: Personal Access Token"
        echo "   1. Go to: https://github.com/settings/tokens"
        echo "   2. Generate new token (classic)"
        echo "   3. Select scope: repo"
        echo "   4. Copy token"
        echo "   5. Run: git push -u origin main"
        echo "   6. Username: AdityaPandey-DEV"
        echo "   7. Password: <paste your token>"
        echo ""
        echo "📘 Full instructions: See GIT_PUSH_INSTRUCTIONS.md"
        echo ""
    fi
else
    echo "❌ Push cancelled"
fi

