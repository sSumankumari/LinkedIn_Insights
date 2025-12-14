from fastapi import APIRouter, HTTPException, Query
from config.db import (
    page_collection, post_collection,
    user_collection, comment_collection, follower_collection
)
from controllers.scraper import scrape_linkedin_data
from controllers.summary_generator import generate_ai_summary

router = APIRouter()

@router.get("/page/{page_id}")
def get_page(page_id: str, refresh: bool = False):
    if not refresh:
        page = page_collection.find_one({"page_id": page_id}, {"_id": 0})
        if page:
            return page

    print(f"Scraping fresh data for: {page_id}...")
    try:
        scraped = scrape_linkedin_data(page_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

    page_data = scraped["page"]
    page_data.pop("_id", None)

    page_collection.update_one(
        {"page_id": page_id},
        {"$set": page_data},
        upsert=True
    )

    if scraped["posts"]:
        post_collection.delete_many({"page_id": page_id})
        post_collection.insert_many(scraped["posts"])

    if scraped["employees"]:
        user_collection.delete_many({"page_id": page_id})
        user_collection.insert_many(scraped["employees"])

    if scraped["comments"]:
        comment_collection.insert_many(scraped["comments"])

    return page_data

@router.get("/pages/search")
def search_pages(
        name: str = None,
        industry: str = None,
        min_followers: int = None,
        max_followers: int = None,
        page: int = 1,
        limit: int = 10
):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if industry:
        query["industry"] = industry
    if min_followers is not None:
        if "followers" not in query: query["followers"] = {}
        query["followers"]["$gte"] = min_followers
    if max_followers is not None:
        if "followers" not in query: query["followers"] = {}
        query["followers"]["$lte"] = max_followers

    skip = (page - 1) * limit
    total = page_collection.count_documents(query)
    data = list(page_collection.find(query, {"_id": 0}).skip(skip).limit(limit))

    return {"data": data, "total": total}

@router.get("/page/{page_id}/posts")
def get_posts(page_id: str, page: int = 1, limit: int = 10):
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

@router.get("/page/{page_id}/summary")
def get_page_summary(page_id: str):
    page = page_collection.find_one({"page_id": page_id}, {"_id": 0})

    if not page:
        raise HTTPException(status_code=404, detail="Page not found. Please scrape it first using /page/{page_id}")

    recent_posts = list(post_collection.find({"page_id": page_id}, {"_id": 0}).limit(5))
    summary_text = generate_ai_summary(page, recent_posts)

    return {
        "page_id": page_id,
        "ai_summary": summary_text
    }