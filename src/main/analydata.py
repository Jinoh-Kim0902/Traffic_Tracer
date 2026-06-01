import csv
import pandas as pd
import sqlite3
import os


# 카메라 4개 합산 기준:
# 0~20대     → green
# 21~60대    → yellow
# 61대 이상 → red

def countVehicle():
    
    
    return

def getData():
    csv_path = "data/result/analysisResult.csv"
    db_path = "data/DB/traffic.db"
    
    if not os.path.exists(csv_path):
        print("CSV file does not exist.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute(
        """
       SELECT camera_id, SUM(vehicle_count) AS total_vehicle_count
       FROM traffic_observation
       GROUP BY camera_id
        """
    )
    
    rows = cursor.fetchall()    
    
    combo_id_count = {}
    combo_id_level = {}
    
    # 카메라 4개 합산 기준:
    # 0~20대     → green
    # 21~60대    → yellow
    # 61대 이상 → red

    for camera_id, total_vehicle_count in rows:
        combo_id_count[camera_id] = total_vehicle_count
        if total_vehicle_count <= 20:
            combo_id_level[camera_id] = "green"
        elif total_vehicle_count <= 60:
            combo_id_level[camera_id] = "yello"
        else:
            combo_id_level[camera_id] = "red"
            
            
    cursor.execute(
    """
        INSERT INTO camera(
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
        
            
    

def main():
    getData()
    
main()