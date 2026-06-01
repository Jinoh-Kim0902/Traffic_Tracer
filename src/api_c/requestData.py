import json
import requests

def get_data(offset):
    url = f"https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/web-cam-url-links/records?limit=100&offset={offset}"

    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("Error occured during request the data")
            print("\n Error code:", response.status_code)
            
    except requests.exceptions.RequestException as e:
    
        # Handle any network-related errors or exceptions
        print('Error:', e)
        return None
            


def main():
    offsets = [0, 100, 200]
    
    for i in offsets:
        data = get_data(i)
        
        if data:
            with open(f"data/webcam_data{i}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
            print("Saved data to webcam_data.json")
            print(data.keys())
            
        else:
            print("Failed to fetch data from API.")

if __name__ == '__main__':
    main()
    