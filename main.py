import time
import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from agents import basic_analysis, get_text_post_content
from functions.utils import calculate_tokens
from functions.threads_api import post_thread_with_text
from functions.mongo_operations import insert_news, get_latest_object
from news_details_scrapper import get_news_details

# Configure logging
logging.basicConfig(filename='main.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

is_job_running = False

def extract_news_details(item):
    anchor_tag = item.find_element("xpath", "h2/a")
    description_tag = item.find_element("xpath", "div")
    span_tags = item.find_elements("xpath", "span")
    return {
        "title": anchor_tag.text,
        "url": anchor_tag.get_attribute("href"),
        "description": description_tag.text,
        "time": span_tags[0].get_attribute("title"),
        "source": span_tags[1].text,
        "will_it_directly_impact_any_stock": "",
        "directly_mentioned_companies_in_news": [],
        "how_will_it_impact": "",
        "reason": "",
    }

def is_new_news(news_obj):
    latest_obj = get_latest_object()
    return not latest_obj or datetime.strptime(news_obj["time"], "%I:%M %p, %d %b %Y") > datetime.strptime(latest_obj["time"], "%I:%M %p, %d %b %Y")

def process_news_list(news_list):
    try:
        results = basic_analysis(news_list) or []
        
        for news_obj in results:
            print(news_obj)
            detailed_news, do_we_have_details = get_news_details(news_obj['url'], news_obj['source'], news_obj['title'])
            
            if do_we_have_details and len(news_obj['directly_mentioned_companies_in_news']) and news_obj['will_it_directly_impact_any_stock'] == "true" and news_obj['how_will_it_impact'] != "Natural":
                post_content, is_success = get_text_post_content(detailed_news, news_obj['url'])
                
                print("#################### RESPONSE ####################")
                print(post_content)
                
                if is_success:
                    post_id = post_thread_with_text(post_content)
                    
                    news_obj['post_id'] = post_id
                    news_obj['post_content'] = post_content
                    print("POST CREATED SUCCESSFULLY")
                time.sleep(60)
                
            insert_news({**news_obj})
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
    time.sleep(30)

def run_job():
    global is_job_running
    
    if is_job_running:
        return "Job is already running..."
    
    is_job_running = True
    print("STARTED")
    options = Options()
    options.add_argument("--headless")  
    driver = webdriver.Chrome(options=options) 
    print("Driver initialized")
    driver.get("https://pulse.zerodha.com/")
    driver.maximize_window()
    news = driver.find_elements("xpath", "/html/body/div[1]/div[1]/ul/li")
    news_list = []
    total_tokens = 0

    has_new_news = False
    for indx, item in enumerate(news[::-1]):
        news_obj = extract_news_details(item)
        
        try:
            if is_new_news(news_obj):
                num_tokens = calculate_tokens(news_obj)
                
                if total_tokens > 3000 or indx == len(news) - 1:
                    process_news_list(news_list)
                    total_tokens = 0
                    news_list = []

                news_list.append({**news_obj})
                total_tokens += num_tokens
                has_new_news = True
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
            
    is_job_running = False
    driver.quit()
    
    return "Job completed successfully with some new news." if has_new_news else "Job completed successfully with all old jobs."
