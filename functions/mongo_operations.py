import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)

try:
    print("Pinging your mongo deployment...")
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Error in mongo connecton")
    print(e)
    exit()
    
db = client["stockNews"]
collection = db["news"]
    

def insert_news(news_obj):
    collection.insert_one(news_obj)
    print("News inserted into MongoDB")
    
def get_latest_object():
    try:
        return collection.find_one(sort=[( '_id', -1 )])
    except Exception:
        return None