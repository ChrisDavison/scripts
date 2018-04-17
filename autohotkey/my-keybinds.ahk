SetTitleMatchMode, RegEx
DetectHiddenWindows, On

#Include copy-text-as-markdown.ahk
#Include focus-spotify.ahk
#Include mute_current_application.ahk
#Include loop-asmr.ahk

; Media functions on ctrl-shift + ins-pgdn block of keys
+^PgDn::Send  {Volume_Down}
+^PgUp::Send {Volume_Up}
+^Del::Send {Media_Prev}
+^End::Send {Media_Next}
+^Home::Send  {Media_Play_Pause}

; Mute using 'break' (top right of keyboard)
break::Send {Volume_Mute}

; Functionkey binds
F1::MuteCurrentApp()
F7::LoopASMRWindows("hide")
F8::LoopASMRWindows("show")
F9::SaveWindowAndGoSpotify()
F10::WinActivate ahk_id %beforeSpotify%

; Ctrl-alt
^!c::CopyTextAsMarkdownLink()
^!i::Run https://inbox.google.com
^!s::Run https://www.youtube.com/feed/subscriptions
^!w::Run https://www.youtube.com/playlist?list=WL
^!a::RUN https://www.youtube.com/playlist?list=PLHCsA_6Hf0ebZEZrdTkL5IwizYOYmLnNc

; Ctrl-alt-win
^!#p::Run https://pubgmap.io/
^!#b::Run http://bbc.co.uk/news

; Lock active window always on top
^!#SPACE:: Winset, Alwaysontop, , A
