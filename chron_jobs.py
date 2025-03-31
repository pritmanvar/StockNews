import requests
import time

def call_api():
    url = "http://localhost:8000/run_job"  # Replace with your API endpoint
    print("RUNNING JOB")
    response = requests.get(url)
    try:
        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Failed to fetch data: {response.status_code}")
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        
if __name__ == "__main__":
    while True:
        call_api()
        time.sleep(60*10)  # Sleep for 1 second before making the next call