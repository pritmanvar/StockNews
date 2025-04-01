import requests
import time

from main import run_job

def call_api():
    url = "http://localhost:8686/run_job"  # Replace with your API endpoint
    print("RUNNING JOB")
    print("STARTED JOB AT:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    response = requests.get(url)
    print("COMPLETED JOB AT:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
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
        time.sleep(1800)
