#!/bin/bash
set -e

echo "🚀 Starting project rename: vgd -> vgd"

# --- 1. Rename Directories ---
# We use 'find' to locate directories safely, handling depth so we don't move a parent before a child
echo "📂 Renaming directories..."

# Rename 'vgd' directories to 'vgd'
find . -depth -type d -name "*vgd*" | while read dir; do
    new_dir="$(dirname "$dir")/$(basename "$dir" | sed 's/vgd/vgd/g')"
    if [ "$dir" != "$new_dir" ]; then
        mv "$dir" "$new_dir"
    fi
done

# Rename 'VGD' directories to 'VGD' (mostly for iOS/macOS paths)
find . -depth -type d -name "*VGD*" | while read dir; do
    new_dir="$(dirname "$dir")/$(basename "$dir" | sed 's/VGD/VGD/g')"
    if [ "$dir" != "$new_dir" ]; then
        mv "$dir" "$new_dir"
    fi
done

# --- 2. Rename Files ---
echo "PAGE Renaming files..."

# Lowercase 'vgd' filenames
find . -depth -type f -name "*vgd*" | while read file; do
    new_file="$(dirname "$file")/$(basename "$file" | sed 's/vgd/vgd/g')"
    mv "$file" "$new_file"
done

# TitleCase 'Vgd' filenames
find . -depth -type f -name "*Vgd*" | while read file; do
    new_file="$(dirname "$file")/$(basename "$file" | sed 's/Vgd/Vgd/g')"
    mv "$file" "$new_file"
done

# Caps 'VGD' filenames
find . -depth -type f -name "*VGD*" | while read file; do
    new_file="$(dirname "$file")/$(basename "$file" | sed 's/VGD/VGD/g')"
    mv "$file" "$new_file"
done

# --- 3. Replace Content in Files ---
echo "📝 Replacing text content..."

# List of extensions to process
EXTENSIONS="py|toml|rs|md|swift|sh|yml|yaml|json|js|ts|svelte|html|css|spec"

# Use grep to find files and sed to replace.
# We use LC_ALL=C to avoid illegal byte sequence errors on some binary files if grep catches them.
grep -rlE --exclude-dir={.git,.venv,node_modules,build,dist} . | grep -E "\.($EXTENSIONS)$" | while read file; do
    # Replace 'vgd' -> 'vgd'
    sed -i 's/vgd/vgd/g' "$file"
    # Replace 'Vgd' -> 'Vgd'
    sed -i 's/Vgd/Vgd/g' "$file"
    # Replace 'VGD' -> 'VGD'
    sed -i 's/VGD/VGD/g' "$file"
done

echo "✅ Renaming complete!"
