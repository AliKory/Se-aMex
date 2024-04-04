const express = require("express");
const http = require("http");
const {Server} = require("socket.io");
const path = require("path");
const cors = require("cors");
//const {conectarMongoDB}=require("./bd/conexion");
const socket = require("./sockets/socket");
//conectarMongoDB();
const app = express();
const httpServer = http.createServer(app);
const io = new Server(httpServer);
socket(io);


app.use(cors());
app.use("/",express.static(path.join(__dirname,'/')));

app.use('/assets', express.static("./assets"));
const port = 3000;
httpServer.listen(port, ()=>{
    console.log("Servidor en http://localhost:"+port);
});