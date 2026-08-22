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

# 5. Copy the file contents and print the confirmation
if [[ -n "$newest" ]]; then
    # Copy file contents to clipboard
    xclip -selection clipboard < "$newest"
    
    # Extract just the filename from the full path for a cleaner print
    filename=$(basename "$newest")
    echo "Success! Copied contents of file: $filename"
else
    echo "No files found in '$TARGET_DIR'." >&2
fi
