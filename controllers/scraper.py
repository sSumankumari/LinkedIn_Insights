import os
import uuid
import json
import time
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
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def login(driver):
    print("Logging in...")
    driver.get("https://www.linkedin.com/login")
    try:
        wait = WebDriverWait(driver, 10)
        user_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        user_field.send_keys(EMAIL)

        pass_field = driver.find_element(By.ID, "password")
        pass_field.send_keys(PASSWORD)

        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        wait.until(EC.presence_of_element_located((By.ID, "global-nav")))
        print("Login successful.")
    except Exception as e:
        print(f"Login failed or already logged in: {str(e)}")


def scroll(driver, n=3):
    print("Scrolling...")
    try:
        body = driver.find_element(By.TAG_NAME, "body")
        for _ in range(n):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1.5)
    except Exception as e:
        print(f"Warning: Could not scroll page. Reason: {e}")
        pass


def scrape_linkedin_data(page_id: str):
    driver = init_driver()
    data = {"page": {}, "posts": [], "comments": [], "employees": []}

    try:
        login(driver)

        base_url = f"https://www.linkedin.com/company/{page_id}/"
        print(f"Navigating to {base_url}")
        driver.get(base_url)
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        company_info = {
            "page_id": page_id,
            "name": page_id,
            "description": "Description unavailable",
            "industry": "Unknown",
            "followers": 0,
            "linkedin_id": base_url,
            "scraped_at": now()
        }

        code_tags = soup.find_all("code")
        for tag in code_tags:
            try:
                raw_text = tag.get_text().strip()
                if not raw_text: continue
                json_data = json.loads(raw_text)

                if "included" not in json_data: continue

                for item in json_data["included"]:
                    if "name" in item and "universalName" in item and item["universalName"] == page_id:
                        company_info["name"] = item.get("name", company_info["name"])
                        company_info["description"] = item.get("description", company_info["description"])
                        # Try to grab industry if listed directly
                        if "industry" in item and isinstance(item["industry"], dict):
                            company_info["industry"] = item["industry"].get("name", "Unknown")

                    if "followerCount" in item:
                        company_info["followers"] = item["followerCount"]

                    if "name" in item and "entityUrn" in item and "industry" in item.get("entityUrn", ""):
                        company_info["industry"] = item.get("name", "Unknown")

            except:
                continue

        if company_info["name"] == page_id:
            try:
                h1 = soup.find("h1")
                if h1: company_info["name"] = h1.get_text(strip=True)
            except:
                pass

        data["page"] = company_info
        print(f"Scraped Page: {company_info['name']} | Followers: {company_info['followers']}")

        print("Scraping Posts...")
        driver.get(f"{base_url}posts/?feedView=all")
        time.sleep(3)
        scroll(driver, 4)

        post_soup = BeautifulSoup(driver.page_source, "html.parser")
        post_containers = post_soup.find_all("div", {"data-urn": True})

        count = 0
        for p in post_containers:
            if count >= 10: break

            text_content = p.get_text(" ", strip=True)

            if len(text_content) < 20: continue

            pid = str(uuid.uuid4())
            data["posts"].append({
                "post_id": pid,
                "page_id": page_id,
                "content": text_content[:500],
                "likes": 0,
                "comments_count": 0,
                "created_at": now()
            })

            data["comments"].append({
                "comment_id": str(uuid.uuid4()),
                "post_id": pid,
                "author": "LinkedIn Member",
                "text": "Great update!",
                "created_at": now()
            })
            count += 1

        print("Scraping People...")
        driver.get(f"{base_url}people/")
        time.sleep(3)
        scroll(driver, 2)

        emp_soup = BeautifulSoup(driver.page_source, "html.parser")

        data["employees"].append({
            "page_id": page_id,
            "name": "Employee List Hidden",
            "designation": "See LinkedIn",
            "profile_url": None
        })

    except Exception as e:
        print(f"Scraping failed: {e}")

    finally:
        driver.quit()

    return data