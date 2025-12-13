import os
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

load_dotenv()

EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

def now():
    return datetime.now(timezone.utc).isoformat()

def init_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def login(driver):
    driver.get("https://www.linkedin.com/login")
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(EMAIL)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

def scroll(driver, n=5):
    body = driver.find_element(By.TAG_NAME, "body")
    for _ in range(n):
        body.send_keys(Keys.PAGE_DOWN)
        WebDriverWait(driver, 3).until(lambda d: True)


def scrape_linkedin_data(page_id: str):
    driver = init_driver()
    data = {"page": {}, "posts": [], "comments": [], "employees": []}

    try:
        login(driver)
        base_url = f"https://www.linkedin.com/company/{page_id}/"
        driver.get(base_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        soup = BeautifulSoup(driver.page_source, "html.parser")

        data["page"] = {
            "page_id": page_id,
            "linkedin_id": base_url,
            "name": soup.find("h1").get_text(strip=True),
            "url": base_url,
            "profile_pic": None,
            "description": "",
            "website": None,
            "industry": "Technology",
            "followers": 0,
            "head_count": 0,
            "specialities": [],
            "scraped_at": now()
        }

        driver.get(f"{base_url}posts/")
        scroll(driver, 6)
        post_soup = BeautifulSoup(driver.page_source, "html.parser")
        posts = post_soup.find_all("div", {"data-urn": True})

        for p in posts[:20]:
            pid = str(uuid.uuid4())
            data["posts"].append({
                "post_id": pid,
                "page_id": page_id,
                "content": p.get_text(" ", strip=True)[:500],
                "likes": 0,
                "comments_count": 0,
                "created_at": now()
            })
            data["comments"].append({
                "comment_id": str(uuid.uuid4()),
                "post_id": pid,
                "author": "Sample User",
                "text": "Sample comment",
                "created_at": now()
            })

        driver.get(f"{base_url}people/")
        scroll(driver, 3)
        emp_soup = BeautifulSoup(driver.page_source, "html.parser")
        people = emp_soup.find_all("div", class_="org-people-profile-card__profile-title")

        for p in people[:10]:
            data["employees"].append({
                "page_id": page_id,
                "name": p.get_text(strip=True),
                "designation": "Employee",
                "profile_url": None
            })

    finally:
        driver.quit()

    return data
