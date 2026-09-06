#!/bin/bash

# ============================================
# SMS BOMBER v3.0 - Auto Installer (Simple)
# ============================================

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ☠️  SMS BOMBER v3.0 - HACKER EDITION  ☠️               ║"
echo "║  🔥 Auto Installer                                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "[1/4] Updating packages..."
pkg update -y && pkg upgrade -y
echo "✅ Done!"

echo "[2/4] Installing Python..."
pkg install python -y
echo "✅ Done!"

echo "[3/4] Installing Python libraries..."
pip install --upgrade pip
pip install requests colorama fake-useragent urllib3
echo "✅ Done!"

echo "[4/4] Installing sound tools..."
pkg install termux-speaker termux-media-player sox -y
termux-setup-storage
echo "✅ Done!"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ INSTALLATION COMPLETED!                              ║"
echo "║                                                          ║"
echo "║  📁 Place main.py in ~/sms_bomber/                     ║"
echo "║  🎵 Place start.mp3 in ~/sms_bomber/                   ║"
echo "║                                                          ║"
echo "║  🚀 To run:                                             ║"
echo "║     cd ~/sms_bomber                                     ║"
echo "║     python main.py                                      ║"
echo "║                                                          ║"
echo "║  ☠️  HAPPY HACKING!  ☠️                                 ║"
echo "╚════════════════════════════════════════════════════════════╝"