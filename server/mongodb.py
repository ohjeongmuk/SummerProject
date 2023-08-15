import asyncio
import pymongo

# ID & PW
username = "ohjeo"
password = "wjdanr90"

# it is a My MongoDB Server to be connected with vscode
url = "mongodb+srv://ohjeo:wjdanr90@summerproject.xf5ljbg.mongodb.net/"
client = pymongo.MongoClient(url)

# Database and Collection
db = client["novel_db"]
collection = db["novel"]

async def insert_data(filename, title, author):
    new_novel = {
        "author": author,
        "filename": filename,
        "title": title,
    }
    if client is not None:
        # show log
        print("Connected to MongoDB server successfully!")
        collection.insert_one(new_novel)
        print("Successfully inserted!")
    else:
        print("Failed to connect to MongoDB server.")