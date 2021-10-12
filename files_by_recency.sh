#!/usr/bin/env bash
fd -t f -x stat --format "%X %N" '{}' \; | sort -rn | sed -e "s/.*'\(.*\)'/\1/g"
