#!/usr/bin/env bash
export DISPLAY=$(grep nameserver /etc/resolv.conf | awk '{print $2}'):0.0
export LIBGL_ALWAYS_INDIRECT=1
export NO_AT_BRIDGE=1

rm -f ~/.wsl_interop

for i in $(pstree -np -s $fish_pid | grep -o -E '[0-9]+'); do
    fname="/run/WSL/$i"_interop
    if [[ -e "$fname" ]]; then
        export WSL_INTEROP=$fname
        echo $fname > ~/.wsl_interop
    fi
done

#     if test -f ~/.emacs.d/bin/doom
#         ~/.emacs.d/bin/doom env >/dev/null 2>&1
#     end

