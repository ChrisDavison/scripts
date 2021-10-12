#!/usr/bin/env python3
from pathlib import Path
import datetime


skeleton_doc = """*{name}.txt*  {description} 

Author:  chris cavison <https://chrisdavison.github.io>
License: Same terms as Vim itself (see |license|)

INTRODUCTION                                    *{name}*

MAPS                                            *{name}-maps*

                                                *{name}-SOME_MAPPING*
{{visual}}<leader>ml                   
    Mapping description


COMMANDS                                          *{name}-commands*
"""

skeleton_plugin = """
" {name}.vim - {description}
" Maintainer: Chris Davison <https://chrisdavison.github.io>
" Version: {date}

if exists("g:loaded_{name}") || &cp || v:version < 700
    finish
endif
let g:loaded_{name} = 1

" PLUGIN HERE
"""

skeleton_autoload = """
" {name}.vim - {description}
" Maintainer: Chris Davison <https://chrisdavison.github.io>
" Version: {date}

" AUTOLOAD FUNCTIONS HERE
function {name}#SOMETHING(ARGS)

endfunction
"""

def write_autoloads(name, description):
    direc = Path(name) / "autoload"
    direc.mkdir(exist_ok=True)
    filename = direc / f"{name}.vim"
    shortname = name.replace("vim-", "")
    filename.write_text(skeleton_autoload.format(
        name=shortname, 
        description=description, 
        date=str(datetime.date.today())))


def write_docs(name, description):
    direc = Path(name) / "doc"
    direc.mkdir(exist_ok=True)
    filename = direc / f"{name}.txt"
    shortname = name.replace("vim-", "")
    filename.write_text(skeleton_doc.format(
        name=name,
        description=description))


def write_plugin(name, description):
    direc = Path(name) / "plugin"
    direc.mkdir(exist_ok=True)
    filename = direc / f"{name}.vim"
    shortname = name.replace("vim-", "")
    filename.write_text(skeleton_plugin.format(
        name=name, 
        description=description, 
        date=str(datetime.date.today())))

name = input("Plugin name: ").replace(" ", "-")
description = input("Oneline description: ")

write_autoloads(name, description)
write_plugin(name, description)
write_docs(name, description)
