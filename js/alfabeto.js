<script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>

const socket = io();

socket.on('mqtt_message', function(msg) {
        document.getElementById('letraInput').value = msg;
        mostrarImagenYAudio(msg);
});

function mostrarImagenYAudio(texto) {
    var imagenDiv = document.getElementById('imagenDiv');
var imagen = document.getElementById('letraImage');
var audio = new Audio(); // Crea un objeto de audio

if (texto !== '') {
    // Ruta de la imagen basada en el texto ingresado
    var imagenSrc = '../assets/' + texto.toLowerCase() + '.jpeg'; // Cambia 'jpg' por la extensión de tu imagen
    // Ruta del audio basada en el texto ingresado
    var audioSrc = `../assets/audio/${texto.toLowerCase()}.mp3`; // Asegúrate de que tus archivos de audio sean .mp3 o cambia la extensión según sea necesario

  
    // Cargar y mostrar imagen
    imagen.src = imagenSrc;
    imagen.style.display = 'block';

    // Cargar y reproducir audio
    audio.src = audioSrc;
    audio.play();
} else {
    imagen.style.display = 'none';
}
}
