import csv
import pandas as pd
import sqlite3
import os


# 카메라 4개 합산 기준:
# 0~20대     → green
# 21~60대    → yellow
# 61대 이상 → red

# def countVehicle():
    
    
#     return

def getDataAnaly():
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


    for camera_id, total_vehicle_count in rows:
        if total_vehicle_count <= 20:
            congestion_level = "green"
        elif total_vehicle_count <= 60:
            congestion_level = "yellow"
        else:
            congestion_level = "red"
            
            
        cursor.execute(
        """
            UPDATE camera
            SET total_vehicle_count = ?,
            congestion_level = ?
            WHERE camera_id = ?
            
        
        """,(
            total_vehicle_count,
            congestion_level,
            camera_id
            )
        )
        # print("Updated:", camera_id, total_vehicle_count, congestion_level, "rowcount:", cursor.rowcount)


        
    conn.commit()
    conn.close()
        
            
    

def main():
    getDataAnaly()
    
main()