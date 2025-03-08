export class Model {
    constructor() {
        this.filmManager = new FilmManager();
    }
}

export class Film {
    constructor(title, year) {
        this.title = title;
        this.year = year;
        this.img_url = "";
    }

    setImgURL(img_url) {
        this.img_url = img_url;
    }
}

export class FilmManager {
    constructor() {
        this.filmslist = [];
        this.selections = [];
        this.category = "";
    }

    // --- Film List ---
    addFilm(film) {
        this.filmslist.push(film);
    }

    removeFilm(film) {
        this.filmslist.splice(this.filmslist.indexOf(film), 1);
    }

    loadFilms() {
        // Load films from list
    }

    // --- Selections ---
    addSelection(film) {
        this.selections.push(film);
    }

    removeSelection(film) {
        this.selections.splice(this.selections.indexOf(film), 1);
    }

    clearSelections() {
        this.selections = [];
    }

    // --- Images ---
    fetchImages() {
        // Fetch images from API for each film
    }
}