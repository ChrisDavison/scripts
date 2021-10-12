#!/bin/bash
# Convert each note to epub, and send to NAS/archive/knowledge-epub
function dir_to_epub(){
    dir="$1"; shift
    cd "$dir"
    for f in $(fd -e org); do
        pandoc "$f" -o "$f".epub --shift-heading-level-by=1 -V title="${f%%.org}"
    done
    pandoc --metadata title="$dir" $(fd -e epub) -o ../"$dir".epub --standalone --self-contained --shift-heading-level-by=1 --epub-chapter-level=2
    fd -e org.epub -x rm {}
    cd ..
}

cd ~/src/github.com/ChrisDavison/recipes
for dir in starters-and-sides soups mains desserts breads sauces; do
    dir_to_epub "$dir"
    mv "$dir".epub /media/nas/archive/my-recipes/
done

fd -e epub -x rm {}
