# LinkedIn Insights Microservice

A simple tool to fetch LinkedIn page details (like followers, posts, and comments) and save them to a database.

## ⚡ Quick Start

**1. Install**
Open your terminal and run:
```bash
git clone [https://github.com/sSumankumari/LinkedIn_Insights.git](https://github.com/sSumankumari/LinkedIn_Insights.git)
cd LinkedIn_Insights
pip install -r requirements.txt
````

**2. Setup Database**
Create a file named `.env` in the folder and paste this line inside:

```env
MONGODB_URI=mongodb://localhost:27017/linkedin_db
```

**3. Run**

```bash
python main.py
```

Go to **`http://localhost:8000/docs`** in your browser to test it.

-----

## 🔍 How to Use

Once the server is running, you can use these links:

  * **Get Company Info:**
    `GET /page/{company_name}` (e.g., `/page/google`)
    *Scrapes the page and saves info to your database.*

  * **Search Pages:**
    `GET /pages/search?name=goo`
    *Finds pages you have already saved.*

  * **See Posts:**
    `GET /page/{company_name}/posts`

  * **See Comments:**
    `GET /post/{post_id}/comments`

-----

## ℹ️ Note on Data

Since LinkedIn blocks bots, this tool uses a hybrid approach:

1.  **Real Data:** It tries to fetch the real Page Name and Description using scraping.
2.  **Sample Data:** It generates sample Posts and Comments so you can test the database features without getting blocked.

```
```
