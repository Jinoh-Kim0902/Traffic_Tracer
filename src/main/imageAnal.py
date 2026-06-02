import csv
import os
from datetime import datetime
from ultralytics import YOLO
import sqlite3

def classify_traffic(n_traffic):
    if n_traffic < 0:
        return None
    elif n_traffic <= 5:
        return "green"
    elif n_traffic <= 15:
        return "yellow"
    else:
        return "red"
    
    
def import_csv_to_db():
    csv_path = "data/result/analysisResult.csv"
    db_path = "data/DB/traffic.db"
    
    if not os.path.exists(csv_path):
        print("CSV file does not exist.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM traffic_observation")
    
    with open(csv_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            cursor.execute("""
                INSERT INTO traffic_observation(
                    camera_id,
                    image_id,
                    car_count,
                    bus_count,
                    truck_count,
                    motorcycle_count,
                    vehicle_count,
                    congestion_level,
                    model_name,
                    conf,
                    imgsz,
                    analyzed_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,(
                row["camera_id"],
                row["image_id"],
                int(row["car_count"]),
                int(row["bus_count"]),
                int(row["truck_count"]),
                int(row["motorcycle_count"]),
                int(row["vehicle_count"]),
                row["congestion_level"],
                row["model_name"],
                float(row["conf"]),
                int(row["imgsz"]),
                row["analyzed_at"]
            ))
            
            
    conn.commit()
    conn.close()
    
def reset():
    result_path = "data/result/analysisResult.csv"
    os.makedirs(os.path.dirname(result_path), exist_ok=True)


    field_names = [
        "camera_id",
        "image_id",
        "car_count",
        "bus_count",
        "truck_count",
        "motorcycle_count",
        "vehicle_count",
        "congestion_level",
        "model_name",
        "conf",
        "imgsz",
        "analyzed_at"
    ]

    with open(result_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()

def save_to_csv(result_data):
    
    result_path = "data/result/analysisResult.csv"
    os.makedirs("data/result", exist_ok=True)
    file_exists = os.path.exists(result_path)
    
    fieldNames = [
        "camera_id",
        "image_id",
        "car_count",
        "bus_count",
        "truck_count",
        "motorcycle_count",
        "vehicle_count",
        "congestion_level",
        "model_name",
        "conf",
        "imgsz",
        "analyzed_at"
    ]
    
    with open(result_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldNames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(result_data)


def analysis_image(image_path, image_id, camera_id):
    model_name = "yolo26n.pt"
    model = YOLO(model_name)
    conf_value = 0.4
    image_size = 1280
    
    
    results = model(
    image_path,
    classes=[2, 3, 5, 7],
    conf=conf_value,
    imgsz=image_size,
    save=False
    )

    result = results[0]
    class_names = result.names

    counts = {
        "car": 0,
        "bus": 0,
        "truck": 0,
        "motorcycle": 0
    }
    for box in result.boxes:
        class_id = int(box.cls[0])
        class_name = class_names[class_id]

        if class_name in counts:
            counts[class_name] += 1

    vehicle_count = (
        counts["car"]
        + counts["bus"]
        + counts["truck"]
        + counts["motorcycle"]
    )


    congestion_level = classify_traffic(vehicle_count)
    
    result_data = {
        "camera_id": camera_id,
        "image_id": image_id,
        "car_count": counts["car"],
        "bus_count": counts["bus"],
        "truck_count": counts["truck"],
        "motorcycle_count": counts["motorcycle"],
        "vehicle_count": vehicle_count,
        "congestion_level": congestion_level,
        "model_name": model_name,
        "conf": conf_value,
        "imgsz": image_size,
        "analyzed_at": datetime.now().isoformat(timespec="seconds")
    }

    save_to_csv(result_data)

    print("Saved YOLO result to CSV")
    print(result_data)
 
    
    
    
    
    
def main():    
    reset()
    for i in range(0, 221):
        if i < 10:
            camera_id = f"TCM00{i}"
        elif i < 100:
            camera_id = f"TCM0{i}"
        else:
            camera_id = f"TCM{i}"
            


        for j in range(0, 4):
            image_id = f"{camera_id}_{j}"        
            image_path = f"images/{camera_id}/{image_id}.jpg"

            if not os.path.exists(image_path):
                continue
            analysis_image(image_path, image_id, camera_id)
            
    import_csv_to_db()
    
if __name__ == "__main__":
    main()
            
            

            
            
