#!/bin/bash
# Convert each note to epub, and send to NAS/archive/knowledge-epub
for file in $(fd -e org); do
    dirname=$(dirname "$file")
    base=$(basename "$file")
    tidy=$(echo "$base" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-zA-Z0-9.-]/-/g' | tr -s - - | sed 's/\-$//g')
    outdir="/media/nas/archive/knowledge-epub/$dirname"
    if [[ ! -d $outdir ]]; then
        mkdir "$outdir"
    fi
    pandoc "$file" -o "$outdir/$tidy".epub --standalone --self-contained -V title="$file"
done
