const express = require('express');
const db = require('./db'); // Import the database connection module
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

  return app, db;
}

module.exports = setupApp;