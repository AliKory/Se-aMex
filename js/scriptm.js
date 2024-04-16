const socket = io();

document.getElementById('letraInput').addEventListener('input', (e) => {
    const letra = e.target.value;
    if (letra.length === 1 && letra.match(/[a-zñ]/i)) { // Verifica si es una letra.
        socket.emit('clienteEnviarLetra', { letra: letra.toLowerCase() });
        // Reproduce el audio de la letra
        const audio = new Audio(`/assets/audio/${letra.toLowerCase()}.mp3`);
        audio.play();
    }
});

socket.on('servidorEnviarImagen', (data) => {
    document.getElementById('imagenContenedor').innerHTML = `<img src="${data.imagenUrl}" alt="Imagen" style="max-width: 100%;">`;
    // Reproduce el audio de la letra aquí también si lo consideras necesario
});