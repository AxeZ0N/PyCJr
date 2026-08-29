#!/bin/bash
export DISPLAY=:0

BASE_DIR="/home/k/Code/Helpful/PyCJr"
TARGET_DIR="$BASE_DIR/sessions"

# 1. Grab the file path with the highest inode number
newest=$(find "$TARGET_DIR" -maxdepth 1 -type f -printf "%i %p\n" | sort -n | tail -n 1 | cut -d' ' -f2-)
filename=$(basename "$newest")

# 2. Run the git command inside your code repository to capture live output
# (Assumes /home/k/Code/Helpful/PyCJr is your git repository root)
GIT_OUTPUT=$(cd $BASE_DIR && git reflog --oneline -n 7)
FILES=$(cd $BASE_DIR && git ls-files)

# 3. Stream the live terminal output and file contents directly to the clipboard
{ 
    echo "$FILES"
    echo ""
    echo "$GIT_OUTPUT"
    echo ""
    cat "$newest"
} | xclip -selection clipboard

echo "Copied: $filename"
