import sqlite3
import os


os.makedirs("data/DB/", exist_ok=True)
DB_PATH = "data/DB/traffic.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

def create_table():
   conn = connect_db()
   cursor = conn.cursor()
   
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
   
   conn.commit()
   conn.close()
   

if __name__ == "__main__":
    create_table()
    print("Database and tables created.")