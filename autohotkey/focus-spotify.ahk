ToggleSpotifyVisibility(){
      global beforeSpotify
      global spotifyVisible
      WinGetTitle, title, A
      if(!spotifyVisible) {
            WinActivate ahk_id %beforeSpotify%
      } else {
            if !RegExMatch(title, "Spotify"){
                  WinGet, beforeSpotify, , A
            }
            WinActivate, Spotify
      }
      spotifyVisible := !spotifyVisible
}
