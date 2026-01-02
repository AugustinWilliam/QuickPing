#!/usr/bin/env bash
set -e

echo "⚡ QuickPing Full Uninstaller"
echo "============================"

# 1️⃣ Remove pipx installation
if command -v pipx &>/dev/null; then
    if pipx list | grep -q "quickping"; then
        echo "📦 Removing QuickPing from pipx..."
        pipx uninstall quickping
    else
        echo "ℹ️ QuickPing not found in pipx."
    fi
else
    echo "ℹ️ pipx not installed, skipping pipx removal."
fi

# 2️⃣ Remove system-wide CLI
if [ -f /usr/local/bin/quickping ]; then
    echo "🗑 Removing system-wide QuickPing CLI..."
    sudo rm -f /usr/local/bin/quickping
else
    echo "ℹ️ No system-wide QuickPing CLI found."
fi

# 3️⃣ Remove local virtual environment
if [ -d "venv" ]; then
    echo "🗑 Removing local virtual environment..."
    rm -rf venv
fi

# 4️⃣ Optional: Remove project folder
read -p "Do you want to remove the QuickPing project folder completely? [y/N]: " confirm
if [[ "$confirm" =~ ^[Yy]$ ]]; then
    folder_name=$(basename "$PWD")
    cd ..
    rm -rf "$folder_name"
    echo "✅ QuickPing project folder removed."
else
    echo "ℹ️ Skipping removal of project folder."
fi

# 5️⃣ Final check
echo ""
echo "✅ QuickPing has been fully uninstalled!"
