from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017/")
db = client["FB_scrapping"]
collection = db["posts"]


def insert_posts(posts):
    return collection.insert_many(posts)

def find_posts(page_name = None):
    if page_name is None : 
        return list(collection.find())
    return list(collection.find({'username' : page_name}))
