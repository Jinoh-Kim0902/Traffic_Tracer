import sqlite3
import os
import json


os.makedirs("data/DB/", exist_ok=True)
DB_PATH = "data/DB/traffic.db"


def create_camera():
    conn = connect_db()
    cursor = conn.cursor()
    
    offsets = [0, 100, 200]
    for offset in offsets:    
        with open(f"data/webcam_data{offset}.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        results = data["results"]
        
        for result in results:
                
            lon = result["geo_point_2d"]["lon"]
            lat = result["geo_point_2d"]["lat"]
            url = result["url"]
            name = result["name"]
            mapid = result["mapid"]
        
            cursor.execute(
                """
                INSERT INTO camera (
                    camera_id,
                    mapid,
                    name,
                    url,
                    lon,
                    lat
                )
                VALUES (?, ?, ?, ?, ?, ?)
                
                """,(
                    mapid, mapid, name, url, lon, lat
                )
            )
    conn.commit()
    conn.close()
    
def connect_db():
    return sqlite3.connect(DB_PATH)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
   
    cursor.execute("""
        DROP TABLE IF EXISTS camera
    """)

    cursor.execute("""
        DROP TABLE IF EXISTS traffic_observation
    """)
   
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS camera (
            camera_id TEXT PRIMARY KEY,
            mapid TEXT,
            name TEXT,
            total_vehicle_count INTEGER,
            congestion_level TEXT,
            url TEXT,
            lon REAL,
            lat REAL
        )
                  
                  """
       
   )
   
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS traffic_observation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            camera_id TEXT,
            image_id TEXT,
            car_count INTEGER,
            bus_count INTEGER,
            truck_count INTEGER,
            motorcycle_count INTEGER,
            vehicle_count INTEGER,
            congestion_level TEXT,
            model_name TEXT,
            conf REAL,
            imgsz INTEGER,
            analyzed_at TEXT
        )
        
        """
   )
    
    create_camera()
    
   
    conn.commit()
    conn.close()
   

if __name__ == "__main__":
    create_table()
    print("Database and tables created.")