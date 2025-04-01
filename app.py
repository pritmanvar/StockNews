from fastapi import FastAPI

# from main import run_job
from functions.threads_api import post_thread_with_text

app = FastAPI()

# @app.get("/")
# def hello_world():
#     return {"data": "Welcome!!!"}

# @app.get("/run_job")
# def handle_job_running():
#     return run_job()

@app.post("/post_thread")
def handle_job_running(text: str):
    return post_thread_with_text(text)