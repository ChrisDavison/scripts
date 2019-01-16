; ^ CTRL
; # WIN
; ! ALT
; + SHIFT


; Media functions on ctrl-shift + ins-pgdn block of keys
+^PgDn::Send  {Volume_Down}
+^PgUp::Send {Volume_Up}
+^Del::Send {Media_Prev}
+^End::Send {Media_Next}
+^Home::Send  {Media_Play_Pause}

; UTILITY
^#!SPACE::WinSet, Alwaysontop, , A
^F12::reload
^#!o::   ; Open my 'default' tabs and apps
    run "https://www.pinboard.in/u:davison"
    run "https://www.pinboard.com/u:davison/untagged"
    run "https://www.todoist.com"
    run "https://www.youtube.com"
    run "https://www.feedly.com"
    run "https://mail.google.com"
return

; TEXT SUBSTITUTION
::]dd::   ; Insert 2019-01-01 16:40 (e.g. current date/time)
    FormatTime, Now,, yyyy-MM-dd HH:mm
    SendInput %Now%
return
::]tt::   ; Insert 16:40 (e.g. current time)
    FormatTime, Now,, HH:mm
    SendInput %Now%
return

; Move and resize windows
; (usually for shoving youtube into a bottom corner)
^#Left::
    Resize(480, 320)
    Move("left", "bottom")
return
^#Right::
    Resize(480, 320)
    Move("right", "bottom")
return
^#!Left::
    Resize(320, 240)
    Move("left", "bottom")
return
^#!Right::
    Resize(320, 240)
    Move("right", "bottom")
return
^SPACE::
    Resize(1024,768) 
    Center()
return

Resize(Width, Height)
{
    WinMove, A, , , , Width, Height
}

Move(locx, locy)
{
    mon := GetCurrentMonitor()
    SysGet, MonBox, Monitor, %mon%   ; Get coordinates & width of Monitor 2
    WinGetPos, , , Width, Height, A
    if ( locx = "left" )
        posnx := MonBoxLeft 
    else
        posnx := MonBoxRight-Width
    if ( locy = "top" )
        posny := MonBoxTop 
    else
        posny := MonBoxBottom-Height
    WinMove, A, , %posnx%, %posny%, Width, Height
}

; (%MonBoxLeft%, %MonBoxTop%) to (%MonBoxRight%, %MonBoxBottom%)

Center()
{
    mon := GetCurrentMonitor()
    SysGet, MonBox, Monitor, %mon%   ; Get coordinates & width of Monitor 2
    WinGetPos, , , Width, Height, A
    posnx := MonBoxLeft + (MonBoxRight-MonBoxLeft)/2 - (Width/2)
    posny := MonBoxTop + (MonBoxBottom-MonBoxTop)/2 - (Height/2)
    WinMove, A, , %posnx%, %posny%, Width, Height
}

GetCurrentMonitor()
{
  SysGet, numberOfMonitors, MonitorCount
  WinGetPos, winX, winY, winWidth, winHeight, A
  Loop %numberOfMonitors%
  {
    SysGet, monArea, Monitor, %A_Index%
    if (winX > monAreaLeft && winX < monAreaRight && winY < monAreaBottom && winY > monAreaTop)
      return A_Index
  }
  SysGet, primaryMonitor, MonitorPrimary
  return "No Monitor Found"
}
