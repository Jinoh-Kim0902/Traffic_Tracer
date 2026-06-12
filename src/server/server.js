const sqlite3 = require("sqlite3").verbose();
const path = require("path");
const PORT = 3000;
const express = require("express");

const server = express();

const dbPath = path.join(__dirname, "..", "..", "data", "DB", "traffic.db");

server.use(express.static(path.join(__dirname, "..", "..", "public")));

// connect to the database
const db = new sqlite3.Database(dbPath, (error) =>{
    if (error) {
        console.error("Failed to connect to SQLITE DB:");
        console.error(error.message);
        return;
    }

    console.log("Connected to SQLite DB");
});


// create the server and api endpoint
// request from the user and response to the user
// check the server status
// 
server.get("/api/health", (req,res) => {
    res.json({
        status:"ok",
        message:"Server is running"
    });
});

// load index.html
server.get("/", (req, res) => {
    const filePath = path.join(__dirname, "..", "..", "public", "index.html");
    res.send(filePath);
});


// load app.js
server.get("/", (req, res) => {
    const filePath = path.join(__dirname, "..", "..", "public", "app.js");
    res.send(filePath);

});


// load style.css
server.get("/", (req, res) => {
    const filePath = path.join(__dirname, "..", "..", "public", "style.css");
    res.send(filePath);
});

server.get("/api/cameras", (req, res) => {
    const query = `
        SELECT
            camera_id,
            mapid,
            name,
            total_vehicle_count,
            congestion_level,
            url,
            lon,
            lat
        FROM camera
    `;

    db.all(query, [], (error, rows) => {
        if (error) {
            console.error("Failed to read camera table:");
            console.error(error.message);

            res.status(500).json({
                error: "Failed to read camera table"
            });
            return;
        }

        res.json(rows);
    });
});


// 404 handler
server.use((req, res) => {
    res.status(404).send("Not Found");
});

server.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});

