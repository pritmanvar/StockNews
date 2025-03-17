import time
from datetime import datetime
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from agents import basic_analysis, get_text_post_content
from functions.utils import calculate_tokens
from functions.threads_api import post_thread_with_text
from functions.mongo_operations import insert_news, get_latest_object
from news_details_scrapper import get_news_details

is_job_running = False

def extract_news_details(item):
    anchor_tag = item.find_element("xpath", "h2/a")
    description_tag = item.find_element("xpath", "div")
    span_tags = item.find_elements("xpath", "span")
    return {
        "title": anchor_tag.text,
        "url": anchor_tag.get_attribute("href"),
        "description": description_tag.text[1:-1],
        "time": span_tags[0].get_attribute("title"),
        "source": span_tags[1].text,
        "will_it_directly_impact_any_stock": "",
        "directly_mentioned_companies_in_news": [],
        "how_will_it_impact": "",
        "reason": "",
    }

def is_new_news(news_obj, latest_obj=None):    
    if not latest_obj:
        print("NEW NEWS")
        return True
    
    print(news_obj['time']) 
    print(latest_obj['time'])
    
    news_obj_date = None
    latest_obj_date = None
    try:
        news_obj_date = datetime.strptime(news_obj["time"], "%I:%M %p, %d %b %Y")
    except Exception:
        news_obj_date = datetime.strptime(news_obj["time"], "%Y-%m-%dT%H:%M:%SZ")
    
    try:
        latest_obj_date = datetime.strptime(latest_obj["time"], "%I:%M %p, %d %b %Y")
    except Exception:
        latest_obj_date = datetime.strptime(latest_obj["time"], "%Y-%m-%dT%H:%M:%SZ")

    if not latest_obj or news_obj_date > latest_obj_date:
        print("NEW NEWS")
        return True
    else:
        return False

def process_news(news):
    try:
        news_obj = basic_analysis(news)
        
        detailed_news, do_we_have_details = get_news_details(news_obj['url'], news_obj['source'], news_obj['title'], news_obj['description'])
        
        print("#################### DETAILED NEWS ####################")
        print(detailed_news)
        print(do_we_have_details)
        print(len(news_obj['directly_mentioned_companies_in_news']))
        print(news_obj['will_it_directly_impact_any_stock'])
        print(news_obj['how_will_it_impact'])
        print("#################### DETAILED NEWS ####################")
        
        if do_we_have_details and len(news_obj['directly_mentioned_companies_in_news']) and news_obj['will_it_directly_impact_any_stock'].lower() == "true" and news_obj['how_will_it_impact'] != "Natural":
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
        traceback.print_exc()
        print(e)
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

    has_new_news = False
    latest_obj = get_latest_object()
    for item in news:
        news_obj = extract_news_details(item)
        # print(news_obj)
        
        try:
            if is_new_news(news_obj, latest_obj):
                process_news({**news_obj})
                news_list = []

                news_list.append({**news_obj})
                print(news_list[-1])
                has_new_news = True
        except Exception as e:
            traceback.print_exc()
            print(e)
            
    is_job_running = False
    driver.quit()
    
    return "Job completed successfully with some new news." if has_new_news else "Job completed successfully with all old jobs."
