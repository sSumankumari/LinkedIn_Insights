import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")

if not MONGO_URI:
    raise Exception("MONGODB_URI not set in env variables")

try:
    client = MongoClient(MONGO_URI)
    client.admin.command("ping")
    print("MongoDB Connection Successful")
except ConnectionFailure:
    raise Exception("Could not connect to MongoDB")

db = client.get_default_database()

page_collection = db.pages
post_collection = db.posts
user_collection = db.users
comment_collection = db.comments

page_collection.create_index("page_id", unique=True)
post_collection.create_index([("page_id", 1), ("created_at", -1)])
user_collection.create_index("page_id")
comment_collection.create_index("post_id")