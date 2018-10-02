#!/usr/bin/env sh
dir=/Users/davison/devel/
for f in "$dir"*; do
    cd "$f" || (echo "Couldn't change to $f" && exit)
    git fetch --all > /dev/null
    cd .. || (echo "Couldn't CD out of $f" && exit)
done
