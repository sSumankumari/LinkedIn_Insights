from fastapi import APIRouter, HTTPException
from config.db import page_collection, post_collection, user_collection, comment_collection
from controllers.scraper import scrape_all_data
from models.page import page_schema
from models.posts import post_schema
from models.user import user_schema
from models.comments import comment_schema

router = APIRouter()

@router.get("/page/{page_id}")
async def get_page(page_id: str):
    page = page_collection.find_one({"page_id": page_id}, {"_id": 0})

    if not page:
        try:
            scraped_data = await scrape_all_data(page_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

        page_data = scraped_data["page"]
        posts = scraped_data["posts"]
        employees = scraped_data["employees"]
        comments = scraped_data["comments"]

        if page_data:
            page_collection.insert_one(page_schema(page_data))

        if posts:
            post_collection.insert_many([post_schema(p) for p in posts])

        if employees:
            user_collection.insert_many([user_schema(u) for u in employees])

        if comments:
            comment_collection.insert_many([comment_schema(c) for c in comments])

        page = page_data

    return page

@router.get("/pages/search")
async def search_pages(
        name: str | None = None,
        industry: str | None = None,
        min_followers: int | None = None,
        max_followers: int | None = None,
        page: int = 1,
        limit: int = 10
):
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
    pages = list(page_collection.find(query, {"_id": 0}).skip(skip).limit(limit))

    return {
        "data": pages,
        "pagination": {
            "current_page": page,
            "limit": limit,
            "total_matches": total
        }
    }

@router.get("/page/{page_id}/posts")
async def get_posts(page_id: str, limit: int = 10):
    return list(
        post_collection.find({"page_id": page_id}, {"_id": 0})
        .sort("created_at", -1)
        .limit(limit)
    )

@router.get("/page/{page_id}/employees")
async def get_employees(page_id: str):
    return list(user_collection.find({"page_id": page_id}, {"_id": 0}))

@router.get("/post/{post_id}/comments")
async def get_post_comments(post_id: str):
    return list(
        comment_collection.find({"post_id": post_id}, {"_id": 0})
    )