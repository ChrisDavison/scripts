#!/usr/bin/env sh
if [ -z $1 ]; then
    echo "Must give commit message"
    exit
fi

echo "Adding all, committing, and pushing"

git add .
git commit -m "$@"
git push
