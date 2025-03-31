import requests
import time
from datetime import datetime

def call_api():
    url = "https://stocknews-p0gz.onrender.com/run_job"  # Replace with your API endpoint
    print("RUNNING JOB")
    response = requests.get(url)
    try:
        if response.status_code == 200:
            print(response.json(), end=" ")
            print(" at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            print(f"Failed to fetch data: {response.status_code}")
            print(response.text + " at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        
if __name__ == "__main__":
    while True:
        call_api()
        time.sleep(1800)