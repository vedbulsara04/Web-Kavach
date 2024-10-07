const express = require('express');
const http = require('http');
const mysql = require('mysql');
const axios = require('axios');  // Import axios for making HTTP requests
const bodyParser = require('body-parser');

const app = express();
const server = http.createServer(app);

app.use(bodyParser.json());
app.use(express.json()); // Parse JSON request bodies
app.use(express.urlencoded({ extended: true })); // Parse URL-encoded bodies
app.use(express.static('public'));

const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '',
  database: 'breached_passwords',
});

db.connect((err) => {
  if (err) {
      throw err;
  }
  console.log('MySQL Connected...');
});

app.post('/scan-password', (req, res) => {
  const password = req.body.password;
  const query = 'SELECT * FROM breached_passwords WHERE password = ?';

  db.query(query, [password], (err, results) => {
      if (err) {
          return res.status(500).json({ error: err.message });
      }
      if (results.length > 0) {
          res.json({ breached: true });
      } else {
          res.json({ breached: false });
      }
  });
});

// Route to handle prediction requests from the frontend
app.post('/predict', async (req, res) => {
  try {
    const { subject, body } = req.body;

    if (!subject || !body) {
      return res.status(400).send('Subject and body are required');
    }

    // Send request to Flask API
    const response = await axios.post('http://127.0.0.1:5000/predict', {
      subject,
      body,
    });

    res.json(response.data); // Send back the Flask API response
  } catch (error) {
    console.error(error);
    res.status(500).send('Error connecting to the ML model');
  }
});


server.listen(3000, () => {
  console.log('Server is running on port 3000');
});
