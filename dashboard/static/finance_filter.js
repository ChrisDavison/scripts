let finances = document.querySelectorAll('.finance-entry');

const filter = () => {
    let q_y = inp_y.value.toLowerCase();
    let q_m = inp_m.value.toLowerCase();
    let q_c = inp_c.value.toLowerCase();
    let q_d = inp_d.value.toLowerCase();

    for(let finance of finances) {
        finance.style.display = "None";
        let matches_year =finance.children[0].textContent.toLowerCase().includes(q_y);
        let matches_month =finance.children[1].textContent.toLowerCase().includes(q_m);
        let matches_category =finance.children[3].textContent.toLowerCase().includes(q_c);
        let matches_description =finance.children[4].textContent.toLowerCase().includes(q_d);

        if (matches_year && matches_month && matches_category && matches_description) {
            finance.style.display = "";
        }
    }
}

let inp_y = document.getElementById('input_year');
let inp_m = document.getElementById('input_month');
let inp_c = document.getElementById('input_category');
let inp_d = document.getElementById('input_description');
inp_y.addEventListener('input', filter);
inp_m.addEventListener('input', filter);
inp_c.addEventListener('input', filter);
inp_d.addEventListener('input', filter);
