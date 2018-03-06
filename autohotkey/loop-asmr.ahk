LoopASMRWindows(action){
    ; If action = 0; hide
    ; If action = 1; show
    WinGet windows, List, .*(ASMR|ACMP|Tingle|Mouth Sounds|Whisper).*
    Loop %windows% {
        id := windows%A_Index%
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
