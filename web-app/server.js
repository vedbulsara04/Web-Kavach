const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const { exec } = require('child_process');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.use(express.static('public'));

io.on('connection', (socket) => {
    console.log('New client connected');

    socket.on('command', (cmd) => {
        // Use bash shell explicitly
        exec(cmd, { shell: 'bash' }, (error, stdout, stderr) => {
            if (error) {
                socket.emit('output', `Error: ${error.message}`);
                return;
            }
            if (stderr) {
                socket.emit('output', `Stderr: ${stderr}`);
                return;
            }
            socket.emit('output', stdout);
        });
    });

    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});

server.listen(3000, () => {
    console.log('Server is running on port 3000');
});