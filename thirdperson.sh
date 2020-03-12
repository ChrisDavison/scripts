#!/bin/bash

# change to read from file
firsts="i|we|me|us|my|mine|ours"
seconds="you|your|yours"

if [ $# -eq 0 ]
then
    echo "usage: `basename $0` <file>..."
    exit
fi

rg --vimgrep -i -n --color=never "\\b($firsts)\\b" $*

rg --vimgrep -i -n --color=never "\\b($seconds)\\b" $*

exit $?
