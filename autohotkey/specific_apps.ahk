SetTitleMatchMode, RegEx
DetectHiddenWindows, On

; Functionkey binds
F7::LoopASMRWindows("hide")
F8::LoopASMRWindows("show")
F9::SaveWindowAndGoSpotify()
F10::WinActivate ahk_id %beforeSpotify%
^!c::CopyTextAsMarkdownLink() ;Ctrl Alt C
^!i::Run https://inbox.google.com
^!t::Run https://trello.com
^!s::Run https://www.youtube.com/feed/subscriptions
^!w::Run https://www.youtube.com/playlist?list=WL
^!p::Run https://pubgmap.io/

SaveWindowAndGoSpotify(){
      global beforeSpotify
      WinGetTitle, title, A
      if !RegExMatch(title, "Spotify"){
            WinGet, beforeSpotify, , A
      }
      WinActivate, Spotify
}

LoopASMRWindows(action){
      ; If action = 0; hide
      ; If action = 1; show
      rx := ".*ASMR|ACMP|Tingle|Mouth Sounds.*|Whisper"
      WinGet windows, List, %rx%
      Loop %windows% {
            id := windows%A_Index%
            WinGetTitle wt, ahk_id %id%
            if (action = "show"){
                  WinShow ahk_id %id%
            }
            else if (action = "hide") {
                  WinHide ahk_id %id%
            }
            else {
                  MsgBox "Don't understand the action..."
            }
      }
}

CopyTextAsMarkdownLink(){
      ; ---------------------------------
      ; MD hyperlink
      ; ---------------------------------

      ; Copies selected text as the URL portion of a Markdown-formatted hyperlink
      ; Asks for the text to display for the link
      ; Places the link as follows in the clipboard [text](url)  
      ;Clipboard :=
      SendInput ^c
      sleep 100

      global MDurl
      global MDtext
      MDurl = %Clipboard%
      MDtext = %Clipboard%

      IfNotInString, MDurl, ://
            MDurl = http://%MDurl%

      Gui, +AlwaysOnTop +Owner
      Gui, Add, Text,, Text to display
      Gui, Add, Edit, vMDtext w320 r1, %MDtext%
      Gui, Add, Text,, URL
      Gui, Add, Edit, vMDurl w320 r1, %MDurl%
      Gui, Add, Button, Default, OK
      Gui, Show, w350, MDLink

      Return

      ButtonOK:
            Gui, Submit
            Gui, Destroy
            Clipboard = [%MDtext%](%MDurl%)
            Return

      GuiClose:
            Gui, Destroy
            Return

      return 
}