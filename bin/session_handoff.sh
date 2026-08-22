#!/bin/bash
# Ensure clipboard communication works
export DISPLAY=:0

# 1. Define your target directory path
TARGET_DIR="/home/k/Code/Helpful/PyCJr/sessions"

# 2. Check if the directory actually exists
if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Directory '$TARGET_DIR' does not exist." >&2
    exit 1
fi

# 3. Print the head (top 5 newest items) of the target directory
echo "=== Top 5 Newest Items in Directory ==="
ls -lt "$TARGET_DIR" | head -n 6
echo "======================================="
echo ""

# 4. Find the single newest file
unset -v newest
for file in "$TARGET_DIR"/*; do
    [[ -f "$file" ]] || continue
    [[ -z "$newest" || "$file" -nt "$newest" ]] && newest="$file"
done

# 5. Copy the git command + file contents and print confirmation
if [[ -n "$newest" ]]; then
    filename=$(basename "$newest")
    
    # Define the git command string you want at the top
    GIT_CMD="# git add $filename && git commit -m 'update' && git push"

    # Group the git command and file contents into a single clipboard stream
    { 
        echo "$GIT_CMD"
        echo "" # Adds a blank line for spacing
        cat "$newest"
    } | xclip -selection clipboard
    
    echo "Success! Copied git command and contents of file: $filename"
else
    echo "No files found in '$TARGET_DIR'." >&2
fi
