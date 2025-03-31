import os
import requests
import certifi

from dotenv import load_dotenv
load_dotenv()

def post_thread_with_text(text):
    container_creation_url = f"https://graph.threads.net/v1.0/{os.getenv('TH_USER_ID')}/threads"
    container_params = {"media_type": "TEXT", "text": text, "access_token": os.getenv("TH_ACCESS_TOKEN")}
    container_response = requests.post(container_creation_url, params=container_params, verify=certifi.where()).json()
    print("Container creation", container_response)

    post_url = f"https://graph.threads.net/v1.0/{os.getenv('TH_USER_ID')}/threads_publish"
    post_params = {"creation_id": container_response["id"], "access_token": os.getenv("TH_ACCESS_TOKEN")}
    post_response = requests.post(post_url, params=post_params, verify=certifi.where()).json()
    print("post creation", post_response)
    
    return post_response['id']

# post_thread_with_text("Hello, Learning thread.")