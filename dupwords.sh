#!/usr/bin/env bash

[[ $# -eq 0 ]] && echo "usage: dupwords <file>..." && return
grep -Eo '(\b.+) \1\b' $1 && true
