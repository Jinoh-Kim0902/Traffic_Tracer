from analydata import getDataAnaly
from downLoadImage import save_webcam_image
from requestData import get_data
from imageAnal import analysis_image, import_csv_to_db, reset
import json
import os

def main():
    print("Main.py start")
    
    offsets = [0, 100, 200]
    
    for i in offsets:
        data = get_data(i)
        
        if data:
            with open(f"data/webcam_data{i}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        
            webcam = data["results"]

                
            save_webcam_image(webcam)
                
            print("Saved data to webcam_data.json")
            print(data.keys())
            
        else:
            print("Failed to fetch data from API.")
            
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
    
    getDataAnaly()

    
if __name__ == "__main__":
    main()