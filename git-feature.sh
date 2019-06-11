#!/usr/bin/env sh
if [ -z $1 ]; then
    echo 'Give a feature name'
    exit
fi

parent=${2:-"master"}
git checkout ${parent}
git pull --rebase
git checkout -b "feature/$1"
