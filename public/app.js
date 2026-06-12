const API_BASE_URL= 'http://localhost:3000/api';
let loadButton;

async function loadCameraData() {
    try {
        console.log("Clicked the button");

        const response = await fetch(API_BASE_URL+"/cameras");
        
        if (!response.ok) {
            throw new Error("Failed to fetch dataset");
        }

        const data = await response.json();
        console.log(data);

        const tableBody = document.getElementById("cameraTableBody");

        tableBody.innerHTML = "";

        data.forEach((camera) => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${camera.camera_id ?? ""}</td>
                <td>${camera.name ?? ""}</td>
                <td>${camera.total_vehicle_count ?? 0}</td>
                <td>${camera.congestion_level ?? ""}</td>
            `;

            tableBody.appendChild(row);
        });


    } catch (err) {
        console.error("Error Occured: Faild to load the data");
        console.error(error);
    }
}

// async function getTableBody() {
//     getLoadID()   
// }

async function init() {

    loadButton = document.getElementById("loadButton");   
    
    loadButton.addEventListener("click", loadCameraData);


}

init();