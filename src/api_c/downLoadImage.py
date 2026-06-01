import json
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def save_webcam_image(webcams):    
    for webcam in webcams:
        page_url = webcam["url"]
        mapid = webcam["mapid"]
        
        save_dir = f"images/{mapid}"

        page_response = requests.get(page_url)
        page_response.raise_for_status()
        
        soup = BeautifulSoup(page_response.text, "html.parser")
        img_tags = soup.find_all("img")

        image_urls = []
        
        for img_tag in img_tags:
            img_src = img_tag.get("src")
            
            if img_src is None:
                continue
        
            if "cameraimages" in img_src and img_src.lower().endswith(".jpg"):
                image_url = urljoin(page_url, img_src)
                image_urls.append(image_url)

        if len(image_urls) == 0:
            print("No image tag found:", page_url)
            return
        
        os.makedirs(save_dir, exist_ok=True)

        for i, image_url in enumerate(image_urls):
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            filename = f"{webcam['mapid']}_{i}.jpg"
            filepath = os.path.join(save_dir, filename)
            
            with open(filepath, "wb") as file:
                file.write(image_response.content)

        print("Saved:", filepath)
        
    


def main():
    offsets = [0, 100, 200]
    for offset in offsets:    
        with open(f"data/webcam_data{offset}.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        webcam = data["results"]

            
        save_webcam_image(webcam)
    
    

    
    
if __name__ == '__main__':
    main()
    
    