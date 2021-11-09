require('dotenv').config();
const fs = require('fs');

const getYear = () => {
    console.log('getting year...');

    const d = new Date();
    return d.getFullYear();
}

const getDay = () => {
    console.log('getting day...');

    const d = new Date();
    return d.getDate();
}

const getAlbumOfTheDay = (day, year) => {
    console.log('getting album of the day...');

    const jsonFolder = process.env.JSON_FOLDER;
    const jsonPath = jsonFolder + '/' + year + '.json';

    const rawAlbums = fs.readFileSync(jsonPath);
    const albums = JSON.parse(rawAlbums);

    albums.forEach((album) => {
        if (album.day === day) {
            console.log(album.content);
        }
    })
}

exports.getYear = getYear;
exports.getDay = getDay;
exports.getAlbumOfTheDay = getAlbumOfTheDay;