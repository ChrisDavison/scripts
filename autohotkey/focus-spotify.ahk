SaveWindowAndGoSpotify(){
      global beforeSpotify
      WinGetTitle, title, A
      if !RegExMatch(title, "Spotify"){
            WinGet, beforeSpotify, , A
      }
      WinActivate, Spotify
}