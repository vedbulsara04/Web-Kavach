const express = require('express');
const http = require('http');
// const socketIo = require('socket.io');
// const { exec } = require('child_process');

const app = express();
const server = http.createServer(app);
// const io = socketIo(server);

app.use(express.static('public'));

server.listen(3000, () => {
    console.log('Server is running on port 3000');
});
