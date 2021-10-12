#!/usr/bin/env bash
selected=$(git ls-files -m -o --exclude-standard | fzf -m --ansi --preview="git diff --color=always -w {}")
if [[ -z "$selected" ]]; then
    exit
fi
git add $selected
git commit
