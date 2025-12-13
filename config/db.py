import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")

if not MONGO_URI:
    raise Exception("MONGODB_URI not set")

try:
    client = MongoClient(MONGO_URI)
    client.admin.command("ping")
    print("MongoDB connection successful")
except ConnectionFailure:
    raise Exception("MongoDB connection failed")

db = client.get_default_database()

page_collection = db.pages
post_collection = db.posts
user_collection = db.users
comment_collection = db.comments
follower_collection = db.followers

page_collection.create_index("page_id", unique=True)
page_collection.create_index("name")
page_collection.create_index("industry")
page_collection.create_index("followers")

post_collection.create_index([("page_id", 1), ("created_at", -1)])
user_collection.create_index("page_id")
comment_collection.create_index("post_id")
follower_collection.create_index("page_id")
