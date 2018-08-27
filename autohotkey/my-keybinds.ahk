SetTitleMatchMode, RegEx
DetectHiddenWindows, On

#Include copy-text-as-markdown.ahk
#Include focus-spotify.ahk
#Include mute_current_application.ahk
#Include loop-asmr.ahk
#Include web-search.ahk

; Media functions on ctrl-shift + ins-pgdn block of keys
+^PgDn::Send  {Volume_Down}
+^PgUp::Send {Volume_Up}
+^Del::Send {Media_Prev}
+^End::Send {Media_Next}
+^Home::Send  {Media_Play_Pause}

; Functionkey binds
F1::MuteCurrentApp()
^#F9::LoopASMRWindows()
#F9::ToggleSpotifyVisibility()

; Ctrl-alt
^!y::YoutubeSearch()
^!s::Run https://www.youtube.com/feed/subscriptions
^!w::Run https://www.youtube.com/playlist?list=WL
^!t::Run https://todoist.com/app?lang=en#agenda%2Fp%3AInbox%2C%20Overdue%2C%20Today
^!a::RUN https://www.youtube.com/playlist?list=PLHCsA_6Hf0ebZEZrdTkL5IwizYOYmLnNc
^!n::RUN https://www.netflix.com/browse/my-list
^!d::DuckDuckGoSearch()

; Lock active window always on top
^!#SPACE:: Winset, Alwaysontop, , A
