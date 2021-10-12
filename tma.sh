#!/usr/bin/env bash
[[ ! -z "$TMUX" ]] && echo "In Tmux" && exit

chosen=$(tmux ls | cut -d':' -f1 | fzf -0 -1)
if [[ ! -z "$chosen" ]]; then
    tmux attach -t "$chosen"
else
    tmux
fi
