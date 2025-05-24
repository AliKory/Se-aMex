const admin = require('firebase-admin');
const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const path = require("path");
const cors = require("cors");
const socket = require("./sockets/socket");
const mqtt = require('mqtt');
const fs = require('fs');
const { PythonShell } = require('python-shell');

const app = express();
const httpServer = http.createServer(app);
const io = new Server(httpServer);
socket(io);

// Configuración de CORS
app.use(cors());

// Configuración de rutas estáticas
app.use(express.static('public'));
app.use("/static", express.static(path.join(__dirname, 'static')));
app.use("/", express.static(path.join(__dirname, '/')));
app.use('/assets', express.static("./assets"));

// Iniciar el servidor Flask
let pyProc = new PythonShell('app.py');
pyProc.on('message', function (message) {
    console.log('Flask:', message);
});

// Ruta para la vista de gestos
app.get('/gestos', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates/deteccion.html'));
});

app.get('/gestos/saludos', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates/deteccionsaludos.html'));
});

app.get('/gestos/emociones', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates/deteccionemociones.html'));
});

app.get('/gestos/presentacion', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates/deteccionpresentacion.html'));
});

app.get('/gestos/negacion', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates/deteccionnegacion.html'));
});

app.get('/gestos/ubicacion', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates/deteccionubicacion.html'));
});

app.get('/gestos/problemas', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates/deteccionproblemas.html'));
});

app.get('/gestos/estadosanimo', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates/deteccionestadosa.html'));
});

app.get('/gestos/salud', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates/deteccionsalud.html'));
});

app.get('/gestos/conducta', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates/deteccionconducta.html'));
});

app.get('/gestos/familia', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates/deteccionfamilia.html'));
});

app.get('/gestos/verbos', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates/deteccionverbos.html'));
});

app.get('/gestos/comunicacion', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates/deteccioncomunicacion.html'));
});

app.get('/gestos/tiempo', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates/detecciontiempo.html'));
});

app.get('/gestos/descripcion', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates/detecciondescripcion.html'));
});

app.get('/gestos/preguntas', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates/deteccionpreguntas.html'));
});

app.use(express.static('public'));

app.use("/", express.static(path.join(__dirname, '/')));

app.use('/assets', express.static("./assets"));

// Configuración de opciones para la conexión segura MQTT
const options = {
    host: '9490def8d1484163895a70bd2a54355f.s1.eu.hivemq.cloud',
    port: 8883,
    protocol: 'mqtts',
    username: 'miapi2',
    password: 'cisco123T',
    // Configuración de TLS/SSL
    // Asegúrate de tener los certificados correctos si tu servidor MQTT lo requiere
    // ca: [fs.readFileSync('path/to/cacert.pem')]
    rejectUnauthorized: false // Solo si confías en el servidor y no puedes verificarlo
};

// Inicializa el cliente MQTT con las opciones configuradas
const client = mqtt.connect(options);

// Configura los callbacks
client.on('connect', function () {
    console.log('Connected');

    // Suscríbete al tópico 'rasp/resultado'
    client.subscribe('rasp/resultado', function(err, granted) {
        if (err) {
            console.log('Subscription failed:', err);
        } else {
            console.log('Subscribed to topic:', granted.map(g => g.topic).join(", "));
        }
    });
});

client.on('error', function (error) {
    console.log('Error:', error);
});

client.on('message', function (topic, message) {
    // Se llama cada vez que se recibe un mensaje en los tópicos suscritos
    console.log('Received message:', topic, message.toString());
    io.emit('mqtt_message', message.toString());
});

// Asegurarse de manejar correctamente el cierre del cliente al terminar el proceso
process.on('SIGINT', function() {
    client.end(true, function() {
        console.log('Client disconnected on process termination');
        process.exit(0);
    });
});

// Objeto para contar las apariciones de cada letra
const letterCounts = {};

client.on('message', function (topic, message) {
    const letter = message.toString().trim(); // Asumiendo que cada mensaje es una letra
    if (letter) {
        letterCounts[letter] = (letterCounts[letter] || 0) + 1;
    }
    io.emit('data', { letter, count: letterCounts });
});


const port = 3000;
httpServer.listen(port, ()=>{
    console.log("Servidor en http://localhost:"+port);
});

// Cuando se cierre el servidor Node.js, también cerrar Flask
process.on('SIGINT', function() {
    pyProc.end(function (err,code,signal) {
        if (err) throw err;
        console.log('The exit code was: ' + code);
        console.log('The exit signal was: ' + signal);
        console.log('Flask process terminated');
        client.end(true, function() {
            console.log('MQTT client disconnected on process termination');
            process.exit(0);
        });
    });
});