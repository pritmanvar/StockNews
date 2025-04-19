import os
import requests
from dotenv import load_dotenv

load_dotenv()

headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}
def call_basic_analysis_api(news, url):

    response = requests.post(url, headers=headers, json=news)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status code {response.status_code}"}
    
def get_text_post_content_api(details, reference):
    url = os.getenv("POST_GENERATION_URL")
    payload = {
        "details": details,
        "reference": reference
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return [{"error": f"Request failed with status code {response.status_code}"}, False]