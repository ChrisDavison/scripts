let books = document.querySelectorAll('.book-entry');

const filter = () => {
    let q_title = inp_book.valuetoLowerCase();
    let q_genre = inp_genre.valuetoLowerCase();
    let q_status = inp_status.valuetoLowerCase();

    for(let book of books) {
        book.style.display = "None";
        let matches_title =book.children[0].textContent.toLowerCase().includes(q_title);
        let matches_genre =book.children[1].textContent.toLowerCase().includes(q_genre);
        let matches_status =book.children[2].textContent.toLowerCase().includes(q_status);

        if (matches_title && matches_genre && matches_status) {
            book.style.display = "";
        }
    }
}

let inp_book = document.getElementById('input_book');
let inp_genre = document.getElementById('input_genre');
let inp_status = document.getElementById('input_status');
inp_book.addEventListener('input', filter);
inp_genre.addEventListener('input', filter);
inp_status.addEventListener('input', filter);
