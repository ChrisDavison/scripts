#!/usr/bin/env bash
chosen=$(files_by_recency | fzf -m)
if [[ ! -z $chosen ]]; then
    vim $chosen
fi
