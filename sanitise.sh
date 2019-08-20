#!/usr/bin/env sh
# Tidy up a filename
if [ $# -eq 0 ]; then
    echo "sanitise <filename> - convert to lowercase; keep alphanumeric, dots and dashes"
    exit
fi
direc=$(dirname $1)
base=$(basename $1)
echo $base | tr '[:upper:]' '[:lower:]' | sed 's/[^a-zA-Z0-9.-]/-/g' | tr -s - - | sed 's/\-$//g'
