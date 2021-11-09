// require('dotenv').config();

const utils = require('./utils');

console.log('starting metal-december...');

const day = utils.getDay();
const year = utils.getYear();

utils.getAlbumOfTheDay(day, year);