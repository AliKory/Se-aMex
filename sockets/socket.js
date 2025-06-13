function socket(io) {
  io.on("connection", (socket) => {
      socket.on('clienteEnviarLetra', (data) => {
          const letra = data.letra;
          const rutaImagen = `../assets/${letra}.jpeg`; 
          // Emite el evento con la URL de la imagen de vuelta al cliente que hizo la solicitud
          socket.emit('servidorEnviarImagen', { imagenUrl: rutaImagen });
      });

  
  });
}
module.exports = socket;