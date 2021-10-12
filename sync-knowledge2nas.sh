#!/usr/bin/env bash
src="$HOME/src/github.com/ChrisDavison/knowledge/"

pushd $src > /dev/null
# Send directory to NAS/notes
rsync -rq --exclude '.git' /media/nas/notes/mobile.md .
rsync -rq --delete --exclude '.git' . /media/nas/notes
mkdir /media/nas/notes/.stfolder
popd > /dev/null

