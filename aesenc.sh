#!/usr/bin/env sh
# Symmetric encode a file with AES256
if [ $# = 0 ]
then
    echo "usage: `basename $0` <file>"
    exit 1
fi
out="$1".asc
in="$1"
gpg --symmetric -a --cipher-algo aes256 --output "$out" "$in"
echo "$out created"

