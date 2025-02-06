import time
import json
from datetime import datetime

from selenium import webdriver

from agents import basic_analysis
from functions.utils import calculate_tokens
from functions.mongo_operations import insert_news, get_latest_object
from news_details_scrapper import get_news_details


print("STARTED")
driver = webdriver.Chrome()  # or webdriver.Firefox()
print("Driver", driver)
driver.get("https://pulse.zerodha.com/")
driver.maximize_window()

news = driver.find_elements("xpath", "/html/body/div[1]/div[1]/ul/li")
news_list = []
total_tokens = 0
llm_results = []

latest_obj = get_latest_object()

for item in news[::-1]:
    anchor_tag = item.find_element("xpath", "h2/a")
    description_tag = item.find_element("xpath", "div")
    span_tags = item.find_elements("xpath", "span")
    news_obj = {
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
    

    if not latest_obj or datetime.strptime(news_obj["time"], "%I:%M %p, %d %b %Y") > datetime.strptime(latest_obj["time"], "%I:%M %p, %d %b %Y"):
        print("NEW NEWS")
        print(news_obj)
        num_tokens = calculate_tokens(news_obj)
        print(num_tokens)
        
        if total_tokens > 3000:
            results = basic_analysis(news_list) or []
            llm_results += results
            
            total_tokens = 0
            news_list = []
            
            time.sleep(30)

        news_list.append({**news_obj})
        total_tokens += num_tokens
    else:
        print("################################ OLD NEWS ########################################")
        
if len(news_list):
    results = basic_analysis(news_list) or []
    llm_results += results
    
    total_tokens = 0
    news_list = []

for news_obj in llm_results:
    print(news_obj)
    print(type(news_obj))
    detailed_news, do_we_have_details = get_news_details(anchor_tag.get_attribute("href"), span_tags[1].text, anchor_tag.text)
    
    if do_we_have_details and len(news_obj['directly_mentioned_companies_in_news']) and news_obj['will_it_directly_impact_any_stock'] == "true" and news_obj['how_will_it_impact'] != "Natural":
        # Generate tweet and share it on X.
        pass

    insert_news({**news_obj})
    
if len(llm_results):
    with open("news_data.json", "w") as json_file:
        json.dump(llm_results, json_file, indent=4)
    

    
driver.quit()

# 1. https://pulse.zerodha.com/
# 2. https://www.moneycontrol.com/news/business/companies/
# 3. https://www.business-standard.com/
# 4. https://www.cnbctv18.com/stocks/


# STEPS:
# 1. Fetch news and store it someware in proper formate.
# 2. Find out more details about news from google.
# 3. Find out related companies from news.
# 4. From stored news get related news of that perticular companies.
# 5. Find past movements of market related to past news fetched from database.
# 6. Predict future market movements based on past movements using LLM.
# 7. Write blog on it.
# 8. Share blog on social media.
