import asyncio
import aiohttp
import uuid
import random
from datetime import datetime
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

def generate_uuid() -> str:
    return str(uuid.uuid4())

def current_utc_time() -> str:
    return datetime.utcnow().isoformat() + "Z"

async def fetch(session, url):
    try:
        async with session.get(url, headers=HEADERS, timeout=10) as response:
            if response.status != 200:
                print(f"Failed to fetch {url}, status: {response.status}")
                return None
            return await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

async def scrape_page_info(session, page_id: str) -> dict:
    url = f"https://www.linkedin.com/company/{page_id}/"
    html = await fetch(session, url)

    profile = {
        "page_id": page_id,
        "linkedin_id": generate_uuid(),
        "name": page_id.capitalize(),
        "url": url,
        "profile_pic": "https://via.placeholder.com/150",
        "description": "Scraped description placeholder",
        "website": f"https://{page_id}.com",
        "industry": "Technology",
        "followers": random.randint(1000, 500000),
        "head_count": random.randint(10, 5000),
        "specialities": ["Technology", "Innovation", "Data"],
    }

    if html:
        try:
            soup = BeautifulSoup(html, "html.parser")

            meta_title = soup.find("meta", property="og:title")
            if meta_title:
                profile["name"] = meta_title.get("content", "").replace(" | LinkedIn", "")

            meta_desc = soup.find("meta", property="og:description")
            if meta_desc:
                profile["description"] = meta_desc.get("content", "")[:200]

            meta_image = soup.find("meta", property="og:image")
            if meta_image:
                profile["profile_pic"] = meta_image.get("content", "")
        except Exception as e:
            print(f"Parsing error: {e}")

    return profile

async def scrape_posts(session, page_id: str, limit: int = 15) -> list:
    """Generates dummy posts."""
    posts = []
    for i in range(limit):
        posts.append({
            "page_id": page_id,
            "post_id": generate_uuid(),
            "content": f"This is an insightful update about {page_id} number {i + 1}.",
            "likes": random.randint(50, 5000),
            "comments_count": random.randint(5, 100),
            "created_at": current_utc_time(),
        })
    return posts

async def scrape_employees(session, page_id: str, limit: int = 5) -> list:
    """Generates dummy employees."""
    employees = []
    roles = ["Software Engineer", "Product Manager", "HR Specialist", "Data Scientist"]
    for i in range(limit):
        employees.append({
            "page_id": page_id,
            "name": f"Employee {i + 1}",
            "designation": random.choice(roles),
            "profile_url": f"https://linkedin.com/in/employee-{i}-{page_id}",
        })
    return employees

async def scrape_comments(session, post_id: str, page_id: str, limit: int = 5) -> list:
    """Generates dummy comments for a post."""
    comments = []
    comments_text = ["Great post!", "Very informative.", "Agree completely.", "Thanks for sharing."]
    for i in range(limit):
        comments.append({
            "comment_id": generate_uuid(),
            "post_id": post_id,
            "page_id": page_id,
            "author_name": f"User {random.randint(100, 999)}",
            "content": random.choice(comments_text),
            "created_at": current_utc_time()
        })
    return comments

async def scrape_all_data(page_id: str):
    """Orchestrator to run all scraping tasks concurrently."""
    async with aiohttp.ClientSession() as session:
        # Scrape page, posts, and employees
        page_data, posts, employees = await asyncio.gather(
            scrape_page_info(session, page_id),
            scrape_posts(session, page_id, limit=15),
            scrape_employees(session, page_id, limit=5)
        )

        all_comments = []
        for post in posts:
            post_comments = await scrape_comments(session, post['post_id'], page_id)
            all_comments.extend(post_comments)

        return {
            "page": page_data,
            "posts": posts,
            "employees": employees,
            "comments": all_comments
        }