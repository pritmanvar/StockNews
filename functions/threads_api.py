import os
import requests
import certifi

from dotenv import load_dotenv
load_dotenv()

def post_thread_with_text(text):
    print(os.getenv('TH_USER_ID'))
    print(os.getenv('TH_ACCESS_TOKEN'))
    print(certifi.where())
    container_creation_url = f"https://graph.threads.net/v1.0/{os.getenv('TH_USER_ID')}/threads"
    container_params = {"media_type": "TEXT", "text": text.replace("\\n", "\n"), "access_token": os.getenv("TH_ACCESS_TOKEN")}
    container_response = requests.post(container_creation_url, params=container_params, verify=certifi.where()).json()
    print("Container creation", container_response)

    post_url = f"https://graph.threads.net/v1.0/{os.getenv('TH_USER_ID')}/threads_publish"
    post_params = {"creation_id": container_response["id"], "access_token": os.getenv("TH_ACCESS_TOKEN")}
    post_response = requests.post(post_url, params=post_params, verify=certifi.where()).json()
    print("post creation", post_response)
    
    return post_response['id']

# post_thread_with_text("Hello, Threads! Testing without ngrok.")
def post_thread_with_text_api(text):
    url = f"https://stocknews-1.onrender.com/post_thread?text={'\\n'.join(text.splitlines())}"
    headers = {
        "accept": "application/json"
    }

    response = requests.post(url, headers=headers, data="")

    print(response.status_code)
    print(response)  # Assuming the response is in JSON format
    
    return response
