#!/usr/bin/env bash
pandoc --to markdown-shortcut_reference_links+pipe_tables-simple_tables-fenced_code_attributes-smart --wrap=auto --columns=72 --atx-headers $1 -o $1


