#! /usr/bin/env bash
# This facilitates merging two repos together
# 
# Usage:
# - source this file
# - go into repoA
# - run pre-repomerge <prefix-for-repoA>
# - go into repoB
# - run git pull <path-to-repoA>
#
# you should now have repoA and repoB merged
# however you may need to fix filenames etc, as I spotted
# this put the prefix in the middle of the filenames, rather
# than at the start (to truely give a directory prefix)
# UPDATE: This is due to MacOSX's SED.  GNU Sed will allow
# \t, however for mac you must do `Ctrl-V <TAB>` to enter
# the tab character in SED replace
function pre-repomerge(){
    PREFIX=$1
    echo $PREFIX
    unamestr=`uname`
    if [[ "$unamestr" == 'Linux' ]]; then
        git filter-branch --index-filter '
            git ls-files -s |
            sed "s,\t,&'"$PREFIX"'/," |
            GIT_INDEX_FILE=$GIT_INDEX_FILE.new git update-index --index-info &&
            mv $GIT_INDEX_FILE.new $GIT_INDEX_FILE
        ' HEAD
    elif [[ "$unamestr" == 'Darwin' ]]; then
        git filter-branch --index-filter \
            'git ls-files -s | sed "s,	,&'"$PREFIX"'/," |
                GIT_INDEX_FILE=$GIT_INDEX_FILE.new git update-index --index-info &&
            mv $GIT_INDEX_FILE.new $GIT_INDEX_FILE' HEAD
    fi
}


