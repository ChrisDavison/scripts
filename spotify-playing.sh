#!/usr/bin/env bash

title=`playerctl --player spotify metadata --format "{{ title }}, by {{ artist }} ({{ album }})"`
if [ -z "$title" ] || [ "$(playerctl status)" = 'Stopped' ] ; then
    echo "No music playing"
else
    status=`playerctl --player spotify status`
    case $status in
        Playing) echo "$title" ;;
        Paused) echo "(PAUSE) $title" ;;
        *) echo "$status: $title" ;;
    esac
fi
