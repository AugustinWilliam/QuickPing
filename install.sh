#!/usr/bin/env bash
set -e

echo "⚡ QuickPing Installer"
echo "====================="

# Install pipx if missing
if ! command -v pipx &>/dev/null; then
    echo "📦 Installing pipx..."
    sudo apt update
    sudo apt install -y pipx
    pipx ensurepath
    echo "🔄 Please restart terminal after install"
fi

# Remove old pipx installs
pipx uninstall quickping || true

# Install QuickPing globally
echo "🚀 Installing QuickPing globally..."
pipx install --force .

echo ""
echo "✅ QuickPing installed globally!"
echo "👉 Run with: quickping"
