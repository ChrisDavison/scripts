YoutubeSearch(){
    myQuery =
    InputBox, myQuery, YoutubeSearch, , , 250, 100
    if (myQuery){
        Run https://www.youtube.com/results?search_query=%myQuery%
    }
}

DuckDuckGoSearch(){
    query =
    InputBox, query, DuckDuckGoSearch, , ,250, 100
    if(query){
        Run https://www.duckduckgo.com/?q=%query%
    }
}
