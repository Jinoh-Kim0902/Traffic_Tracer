
const http = require("http");
const sqlite3 = require("sqlite3").verbose();
const path = require("path");
const fs = require("fs");
const PORT = 3000;

const dbPath = path.join(__dirname, "..", "..", "data", "DB", "traffic.db");


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
const server = http.createServer((req, res) =>{
    console.log(req.method, req.url);

    // check the server status
    if (req.method == "GET" && req.url === "/api/health") {
        res.writeHead(200, {"Content-Type": "application/json"});
        res.end(JSON.stringify({
            status:"ok",
            message:"Server is running"
        }));
        return;
    }

    // load index.html
    if (req.method == "GET" && req.url === "/") {
        const filePath = path.join(__dirname, "..", "..", "public", "index.html");

        fs.readFile(filePath, (error, content) => {
            if (error) {
                res.writeHead(500, { "Content-Type": "text/plain"});
                res.end("Failed to load index.html");
                return;
            }
        
            res.writeHead(200, {"Content-Type": "text/html"});
            res.end(content);
        });
        
        
        return;
    }

    // load app.js
    if (req.method == "GET" && req.url === "/") {
        const filePath = path.join(__dirname, "..", "..", "public", "app.js");

        fs.readFile(filePath, (error, content) => {
            if (error) {
                res.writeHead(500, { "Content-Type": "text/plain"});
                res.end("Failed to load app.js");
                return;
            }
        
            res.writeHead(200, {"Content-Type": "text/app"});
            res.end(content);
        });
        
        
        return;
    }

    // load style.css
    if (req.method == "GET" && req.url === "/") {
        const filePath = path.join(__dirname, "..", "..", "public", "style.css");

        fs.readFile(filePath, (error, content) => {
            if (error) {
                res.writeHead(500, { "Content-Type": "text/plain"});
                res.end("Failed to load style.css");
                return;
            }
        
            res.writeHead(200, {"Content-Type": "text/css"});
            res.end(content);
        });
        
        
        return;
    }

    // get the data from the db
    if (req.method === "GET" && req.url === "/api/cameras") {
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

        db.all(query, [], (error, rows)=> {
            if(error) {
                console.error("FAILED to read caemra talbe:");
                console.error(error.message);

                res.writeHead(500, { "Content-Type": "application/json"});
                res.end(JSON.stringify({
                    error: "Failed to read camera table"
                }));
                return;
            }
            res.writeHead(200, { "Content-Type": "application/json"});
            res.end(JSON.stringify(rows));
        });
        return;
    }

    res.writeHead(404, { "Content-Type": "text/plain"});
    res.end("Not Found");

});

server.listen(PORT, ()=> {
    console.log(`Server running on http://localhost:${PORT}`);
})

