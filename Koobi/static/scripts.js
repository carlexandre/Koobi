function Search() {
    let input = document.getElementById('search-input').value.toLowerCase();
    let eachnote = document.querySelectorAll('.each-note');

    if (!eachnote) return;

    eachnote.forEach(en => {
        let idtitle = en.id;
        let title = document.querySelector(`.card-title[data-title="${idtitle}"]`).textContent.toLowerCase();

        if (title.includes(input)) {
            en.classList.remove('oculto');
        } else {
            en.classList.add('oculto');
        }
    });
}