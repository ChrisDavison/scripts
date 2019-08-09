#!/usr/bin/env sh

# Symmetric encode a file with AES256
out="$1".asc
in="$1"
gpg --symmetric -a --cipher-algo aes256 --output "$out" "$in"
echo "$out created"

