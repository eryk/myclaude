#!/bin/bash
# Sync agents, skills, and commands from current project to ~/.claude
# Ensures both sides are completely consistent (uses --delete)

set -e

SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="$HOME/.claude"

DIRS=("agents" "skills" "commands")

echo "Syncing from: $SOURCE_DIR"
echo "Syncing to:   $TARGET_DIR"
echo ""

# Check if target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: $TARGET_DIR does not exist"
    exit 1
fi

# Dry run first to show what will change
echo "=== Changes to be made ==="
for dir in "${DIRS[@]}"; do
    if [ -d "$SOURCE_DIR/$dir" ]; then
        echo ""
        echo "[$dir]"
        rsync -avhn --delete "$SOURCE_DIR/$dir/" "$TARGET_DIR/$dir/" 2>/dev/null | grep -E "^(sending|deleting|>|<|\*)" | sed 's/^sending file list .*//' | grep -v "^$" || echo "(no changes)"
    fi
done

echo ""
read -p "Proceed with sync? [y/N] " confirm

if [[ "$confirm" =~ ^[Yy]$ ]]; then
    echo ""
    echo "=== Syncing ==="
    for dir in "${DIRS[@]}"; do
        if [ -d "$SOURCE_DIR/$dir" ]; then
            echo "Syncing $dir..."
            rsync -av --delete "$SOURCE_DIR/$dir/" "$TARGET_DIR/$dir/"
        else
            echo "Skipping $dir (not found in source)"
        fi
    done
    echo ""
    echo "Done!"
else
    echo "Cancelled."
fi
