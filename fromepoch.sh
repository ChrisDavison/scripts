#!/usr/bin/env sh
# Convert from epoch seconds to YYYYmmdd HHMMSS
date -r "$1" +"%Y%m%d %H:%M:%S"
