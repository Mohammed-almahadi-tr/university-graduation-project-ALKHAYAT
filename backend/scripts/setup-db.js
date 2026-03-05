const mysql = require('mysql2/promise');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

async function setupDatabase() {
    try {
        // Connect without database first
        const connection = await mysql.createConnection({
            host: process.env.DB_HOST,
            user: process.env.DB_USER,
            password: process.env.DB_PASSWORD,
            multipleStatements: true
        });

        console.log('Connected to MySQL server');

        // Read and execute schema
        const schemaPath = path.join(__dirname, '../config/schema.sql');
        const schema = fs.readFileSync(schemaPath, 'utf8');

        await connection.query(schema);
        console.log('Database and tables created successfully!');

        await connection.end();
        console.log('Setup complete!');
    } catch (error) {
        console.error('Error setting up database:', error.message);
        process.exit(1);
    }
}

setupDatabase();
