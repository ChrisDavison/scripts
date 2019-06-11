#!/usr/bin/env sh
if [ -z $1 ]; then
    echo 'Give a fix name'
    exit
fi

if [ -z "$2" ]; then
    git checkout master
    git pull --rebase
    git checkout -b "fix/$1"
else
    git checkout "$2"
    git pull --rebase
    git checkout -b "fix/$1"
fi
