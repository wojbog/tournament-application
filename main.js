// Start the server
const express = require('express');
// const db = require('./config/db'); // Import the database connection module
require('dotenv').config(); // Load environment variables

// Function to set up the application
function setupApp() {
  const app = express();

  // Middleware to parse JSON requests
  app.use(express.json());

  // Basic route to check if the application is working
  app.get('/', (req, res) => {
    res.send('Node.js and MySQL Application is running!');
  });

//   // Route to fetch data from the database
//   app.get('/data', (req, res) => {
//     db.query('SELECT * FROM your_table_name', (err, results) => {
//       if (err) {
//         console.error('Error fetching data:', err.message);
//         res.status(500).json({ error: 'Database query failed' });
//         return;
//       }
//       res.json(results);
//     });
//   });

//   // Route to add data to the database
//   app.post('/data', (req, res) => {
//     const { field1, field2 } = req.body;
//     const query = 'INSERT INTO your_table_name (field1, field2) VALUES (?, ?)';
//     db.query(query, [field1, field2], (err, results) => {
//       if (err) {
//         console.error('Error inserting data:', err.message);
//         res.status(500).json({ error: 'Database insertion failed' });
//         return;
//       }
//       res.json({ message: 'Data inserted successfully', id: results.insertId });
//     });
//   });

  return app
}

const mysql = require('mysql2');

const connection = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

connection.connect((err) => {
  if (err) {
    console.error('Error connecting to the database:', err.message);
    return;
  }
  console.log('Connected to the MySQL database.');
});
// const setup = require('./config/set_up'); 
const PORT = process.env.PORT || 3000;
const app= setupApp();
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
