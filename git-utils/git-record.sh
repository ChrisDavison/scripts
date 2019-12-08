#!/usr/bin/env sh
echo "Adding all, committing, and pushing"

git add . > /dev/null
git commit -m "$@" > /dev/null
git push > /dev/null

echo "FINISHED"
