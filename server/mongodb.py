import asyncio
import pymongo

client = pymongo.MongoClient("localhost", 27017)

db = client["novel_db"]
collection = db["novel"]

async def insert_data(filename, title, author):
    print("Received title:", title)  # 로그 추가
    print("Received author:", author)  # 로그 추가

    new_novel = {
        "author": author,
        "filename": filename,
        "title": title,
    }
    if client is not None:
        print("Connected to MongoDB server successfully!")
    else:
        print("Failed to connect to MongoDB server.")

    collection.insert_one(new_novel)
    print("Successfully inserted!")
    