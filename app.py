from fastapi import FastAPI

from main import run_job
from functions.threads_api import post_thread_with_text
from agents import basic_analysis, get_text_post_content

app = FastAPI()

@app.post("/get_basic_analysis")
def handle_basic_analysis(news: dict):
    return basic_analysis(news)

@app.post("/get_text_post_content")
def handle_text_post_content(details: str, reference: str):
    return get_text_post_content(details, reference)