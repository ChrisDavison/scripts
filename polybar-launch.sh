#!/usr/bin/env bash
pkill polybar
i=0
MONITOR=eDP-1 polybar -r internal &

for m in `polybar --list-monitors | cut -d':' -f1`; do
    if [[ $m -eq "eDP-1" ]]; then
        continue
    else
        MONITOR=$m polybar -r external &
    fi
done
