export class View {
    constructor() {
        this.spinner = new Spinner();
        this.selections = new Selections();
    }   
}

export class Spinner {
    constructor() {
        this.spinner = document.createElement("div");
        this.spinner.className = "spinner";
    }

    cook_the_pies(films) {
        // Create the pie chart with all the films
    }

    show() {
        document.body.appendChild(this.spinner);
    }
}

export class Selections {
    constructor() {
        const element = document.createElement("div");
        this.selections.className = "selections";

        return element;
    }

    refresh(selections) {
        // If no selections, show hint
        // If selections, hide hint
    }
}