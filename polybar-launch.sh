#!/usr/bin/env sh
pkill polybar
# for m in `polybar --list-monitors | cut -d':' -f1`; do
#     MONITOR=$m polybar -r internal &
# done
MONITOR=eDP-1 polybar -r internal &
MONITOR=DP-1 polybar -r external &
