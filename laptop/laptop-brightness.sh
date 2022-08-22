#!/usr/bin/env bash
set -e

# Question: Under what circumstances could there be two backlight listings?
# If I had this, I would set it up to adjust each in turn maybe. But I don't.

# Usage
if [ "$#" -eq 0 ]; then
    cat <<-EOF
Usage: $0 [command]
Increase or decrease screen brightness at hardware level by steps of 5% of
max, as determined by the values under /sys/class/backlight/**. Limit values
to the range of 0 to max_brightness.

up | Increase brightness by 5%
down | Decrease brightness by 5%
current | Report current brightness


This script needs root access - sudo is an option, but you may also consider
allowing your user to run the script without a password prompt e.g.:

# Append to /etc/sudoers
Cmnd_Alias BRIGHT_CMDS=/bin/path/bright up, /bin/path/bright down
username ALL=(root) NOPASSWD: BRIGHT_CMDS
EOF
exit 1
fi

SHORT_USAGE="laptop-brightness up|down|show"

# Gather information
backlight_dir='/sys/class/backlight'
# device_dir=$(ls "${backlight_dir}" | head -n 1)
device_dir=intel_backlight
if [ -z "$device_dir" ]; then
    echo 'No backlight hardware is listed in /sys/class/backlight! Quitting.'
    exit 1
fi
device_dir="${backlight_dir}/${device_dir}"
brightness_file="${device_dir}/brightness"
curr_brightness=$(cat "${brightness_file}")
max_brightness=$(cat "${device_dir}/max_brightness")
step=$(( $max_brightness / 20 ))

function write_brightness() {
    echo $1 > "${brightness_file}"
}

function increase_brightness() {
    new_brightness=$(( $curr_brightness + $step ))
    if [ "$new_brightness" -gt "$max_brightness" ]; then
        new_brightness="$max_brightness"
    fi
    write_brightness $new_brightness
}

function decrease_brightness() {
    new_brightness=$(( $curr_brightness - $step ))
    if [ "$new_brightness" -lt 0 ]; then
        new_brightness=0
    fi
    write_brightness $new_brightness
}

function show_current_brightness() {
    echo "SHOWING"
    now=$( echo "(${curr_brightness} / ${max_brightness}) * 100" | bc -l | cut -d'.' -f 1)
    echo  $now%
}

command=$1

case $command in
    up|increase|--up|u) increase_brightness ;;
    down|decrease|--down|d) decrease_brightness ;;
    show|s|--show) show_current_brightness ;;
    *) echo $SHORT_USAGE ;;
esac
