LoopASMRWindows(){
    global asmrVisible
    WinGet windows, List, .*(ASMR|ACMP|Tingle|Mouth Sounds|Whisper|Role Play).*
    Loop %windows% {
        id := windows%A_Index%
        if (asmrVisible){
            WinHide ahk_id %id%
        }
        else {
            WinShow ahk_id %id%
            WinActivate ahk_id %id%
        }
    }
    asmrVisible := !asmrVisible
}
