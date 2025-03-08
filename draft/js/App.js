import { Model, Film, FilmManager } from './Model.js';
import { View, Spinner, Selections } from './View.js';
import { Controller } from './Controller.js';

const app = new Controller(new Model(), new View())