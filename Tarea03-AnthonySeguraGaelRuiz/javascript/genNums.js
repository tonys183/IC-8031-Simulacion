const fs = require('fs');
const path = require('path');

function genNums(n, nombreArchivo, min, max) {
    const ruta = path.join(__dirname, nombreArchivo);
    const stream = fs.createWriteStream(ruta);

    for (let i=0; i<n; i++) stream.write(Math.floor(Math.random()*(max-min+1))+min + '\n');
    stream.end();
}
const n = 1000000;
genNums(n, 'javascript.txt', 1, 100);