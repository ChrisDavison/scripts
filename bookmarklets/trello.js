#! /usr/bin/env node

// Hide labels
function hide_labels(labels){    
    function hide_label(l){        
        $(".card-label").each( (a, b) => {
            var card = b.parentElement.parentElement.parentElement;
            var has_label = b.innerText.indexOf(l) >= 0;
            var is_card = card.classList.contains("list-card");
            if(is_card && has_label) {              
                console.log(card);
                card.classList.add("hide");
            }}); 
    }
    labels.split(",").forEach(hide_label);
}
hide_labels(prompt("Hide: ", "podcast"));

// Show labels
function show_labels(labels){
    function show_label(l){
        $(".card-label").each( (a, b) => {
             var card = b.parentElement.parentElement.parentElement;
            var has_label = b.innerText.indexOf(l) >= 0;
            var is_card = card.classList.contains("list-card");
            if(is_card && has_label) {
                 console.log(card);
                card.classList.remove("hide");
        }});
    }    labels.split(",").forEach(show_label);
}
show_labels(prompt("Show: ", "podcast"));

// Toggle hiding or showing of card covers
$(".list-card-cover").each( (a, b) => { b.classList.toggle("hide"); });
