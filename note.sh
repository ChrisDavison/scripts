cmd=$1
shift

NOTESFILE="$HOME/Dropbox/notes/notes.md"

_add() {
    if [ ! -f "$NOTESFILE" ]; then
        touch $NOTESFILE
    fi
    echo "- $@" >> $NOTESFILE
}
 
_find() {
    # If I'm inside NOTESDIR, only search the subdirectory
    [[ ! -d "${NOTESDIR}" ]] && echo "NOTESDIR not defined" &&  return 2
    loc="${NOTESDIR}"
    if [ -d "$1" ]; then
        loc="$1"
        shift
    fi
    [[ -z "$@" ]] && echo "Must pass a query" && return 1;
    echo "Match is Filename, Directory, or Content"
    fd "$@" "${loc}" -e md | sed -e "s/^/F /"
    fd "$@" "${loc}" -t d | sed -e "s/^/D /"
    rg -F "$@" "${loc}" -l | sed -e "s/^/C /"
}

_view(){
    bat -l md $NOTESFILE
}

_preview(){
    query=${1:-''}
    batcmd='bat $NOTESDIR/{} --color=always -n'
    fd . -e md "$NOTESDIR" | sed -e "s!$NOTESDIR/!!g" | fzf -q "$query" --multi --preview="$batcmd" --preview-window=down:50% | sed -e "s!^!$NOTESDIR/!g"
}

_open(){
    files=$(_preview $@)
    [ -z "$files" ] && return 1
    $EDITOR "$files"
}

_clear(){
    rm "$NOTESFILE"
    touch "$NOTESFILE"
}

_edit(){
    $EDITOR "$NOTESFILE"
}

case $cmd in
    a|add) _add "$@" ;;
    f|find) _find "$@" ;;
    e|edit) _edit ;;
    v|view) _view ;;
    d|delete|empty) _clear ;;
    o|open|edit) _open "$@" ;;
    p|preview) _preview "$@" ;;
    *) 
        echo "note"
        echo "    a - add to NOTES file"
        echo "    v - view full NOTES file"
        echo "    e - edit NOTES file"
        echo "    d - delete(empty) NOTES file"
        echo "    f - find a note by title or content"
        echo "    o - open files in vim"
        echo "    p - preview notes files using fzf"
        ;;
esac

