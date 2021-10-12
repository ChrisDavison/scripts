#!/usr/bin/env bash
parent=$(git log --pretty=oneline --color=always | fzf --ansi | cut -d ' ' -f1)
if [[ -z $parent ]]; then
    echo "Must select a parent to rebase from"
else
    git rebase -i $parent
fi
