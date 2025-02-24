from fastapi import FastAPI

from main import run_job

app = FastAPI()

@app.get("/")
def hello_world():
    return {"data": "Welcome!!!"}

@app.get("/run_job")
def handle_job_running():
    return run_job()