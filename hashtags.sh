#!/usr/bin/env bash
rg --only-matching --no-line-number '@[a-zA-Z1-9]+' "$@" | sort | uniq | tr '\n' ' '
