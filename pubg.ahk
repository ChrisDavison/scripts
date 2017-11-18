#IfWinActive ahk_exe TslGame.exe
Suspend
Pause,,1
 
SoundBeep
return


; If you do  run and jump add "shift", "&" before Space::
shift & Space::
SendInput, {F2}
SendInput, {h}
return

Space::
SendInput, {F2}
SendInput, {h}
return