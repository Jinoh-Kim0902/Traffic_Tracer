const API_BASE_URL= 'http://localhost:3000/api';
let loadButton;

async function loadCameraData() {
    try {
        console.log("Clicked the button");


        // fetch the data to the server and wait it when server response
        const response = await fetch(API_BASE_URL+"/cameras");
        
        if (!response.ok) {
            throw new Error("Failed to fetch dataset");
        }

        // server send the data as a query
        const data = await response.json();
        console.log(data);

        // document는 html을 의미함함
        const tableBody = document.getElementById("cameraTableBody");
        // id가 cameraTableBody 인 애의 inner 내용을 전부 삭제함함
        tableBody.innerHTML = "";

        data.forEach((camera) => {
            // and then write the new data into the body
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