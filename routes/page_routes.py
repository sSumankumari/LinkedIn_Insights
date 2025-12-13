from fastapi import APIRouter, HTTPException
from config.db import (
    page_collection, post_collection,
    user_collection, comment_collection, follower_collection
)
from controllers.scraper import scrape_linkedin_data

router = APIRouter()

@router.get("/page/{page_id}")
def get_page(page_id: str):
    page = page_collection.find_one({"page_id": page_id}, {"_id": 0})
    if not page:
        scraped = scrape_linkedin_data(page_id)
        page_collection.insert_one(scraped["page"])
        if scraped["posts"]:
            post_collection.insert_many(scraped["posts"])
        if scraped["employees"]:
            user_collection.insert_many(scraped["employees"])
        if scraped["comments"]:
            comment_collection.insert_many(scraped["comments"])
        page = scraped["page"]
    return page

@router.get("/pages/search")
def search_pages(name=None, industry=None, min_followers=None, max_followers=None, page=1, limit=10):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if industry:
        query["industry"] = industry
    if min_followers or max_followers:
        query["followers"] = {}
        if min_followers:
            query["followers"]["$gte"] = min_followers
        if max_followers:
            query["followers"]["$lte"] = max_followers

    skip = (page - 1) * limit
    total = page_collection.count_documents(query)
    data = list(page_collection.find(query, {"_id": 0}).skip(skip).limit(limit))

    return {"data": data, "total": total}

@router.get("/page/{page_id}/posts")
def get_posts(page_id: str, page=1, limit=10):
    skip = (page - 1) * limit
    return list(
        post_collection.find({"page_id": page_id}, {"_id": 0})
        .sort("created_at", -1)
        .skip(skip).limit(limit)
    )

@router.get("/page/{page_id}/employees")
def get_employees(page_id: str):
    return list(user_collection.find({"page_id": page_id}, {"_id": 0}))

@router.get("/post/{post_id}/comments")
def get_comments(post_id: str):
    return list(comment_collection.find({"post_id": post_id}, {"_id": 0}))

@router.get("/page/{page_id}/followers")
def get_followers(page_id: str):
    return list(follower_collection.find({"page_id": page_id}, {"_id": 0}))
