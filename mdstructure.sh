#!/usr/bin/env sh 
cmd="$1"; shift
case "$cmd" in
    links) query="[^!]\[.*?\]\(.*?\)" ;;
    images) query="!\[.*?\]\(.*?\)" ;;
    keywords) query="(?:[\s\`^])#[a-zA-Z]+" ;;
    headers) query="^#+ .*" ;;
    todos) query="^\s*\-*\s*\[ \]\s*.*" ;;
    *)
        echo "Unrecognised command: $cmd"
        echo "links, images, keywords, todos, or headers"
        return 1
        ;;
esac
if [ $# -gt 0 ]; then
    files="$@"
else
    files=`echo **/*.md`
fi
rg "$query" $files -g -o --no-heading --sort=path
