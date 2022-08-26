#!/usr/bin/env bash
OLD_IFS=$IFS
IFS='
'
pkill polybar
# MONITOR=eDP-1 polybar -r internal &

for m in `polybar --list-monitors`; do
    monitor_id=$(echo $m | cut -d':' -f1)
    echo $m | grep -q "primary" > /dev/null
    is_secondary=$?
    if [[ $is_secondary -eq 0 ]]; then
        MONITOR=$monitor_id polybar -r internal &
    else
        MONITOR=$monitor_id polybar -r external &
    fi
done

IFS=$OLD_IFS
