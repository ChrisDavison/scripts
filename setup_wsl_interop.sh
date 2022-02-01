#!/usr/bin/env bash
if [[ "$IS_WSL" -eq 1 ]]; then
    echo "Setting up WSL interop"
    export BROWSER=$(which firefox)
    export DISPLAY=$(route.exe print | grep 0.0.0.0 | head -1 | awk '{print $4}'):0.0
    export LIBGL_ALWAYS_INDIRECT=1
    export NO_AT_BRIDGE=1


    # THINK i only need to find the /run/WSL file when using emacs?
    # ...as i did this as a hack when trying to get copy-paste working (by reading in from the file)
    # i create every time I do a copy-paste
 
    # for i in $(pstree -np -s $$ | grep -o -E '[0-9]+'); do
    #     fname=/run/WSL/"$i"_interop
    #     if [[ -e "$fname" ]]; then
    #         export WSL_INTEROP=$fname
    #         [[ -f "~/.wsl_interop" ]] && rm "~/.wsl_interop"
    #         echo $fname > ~/.wsl_interop
    #         exit
    #     fi
    # done
fi
