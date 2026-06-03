const { exec } = require("child_process");

let isRunning = false;

function runRequestData() {
    if (isRunning) {
        console.log("Previous analysis is still running. Skipping this cycle.");
        return;
    }
    
    isRunning = true;
    
    console.log("Starting python");
    console.log(new Date().toLocaleTimeString());
    exec("python src/main/main.py", (error, stdout, stderr) => {
        isRunning = false;

        if (error) {
            console.error("Failed to run python script");
            console.error(error.message);
            return;
        }

        if (stderr) {
            console.error("Python stderr:");
            console.error(stderr);
        }

        console.log("python output:");
        console.log(stdout);

        console.log("Finished Request Data");
        console.log(new Date().toLocaleTimeString());
    });
}

runRequestData();

setInterval(runRequestData, 20 * 60 * 1000);