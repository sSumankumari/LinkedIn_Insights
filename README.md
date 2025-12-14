# LinkedIn Insights Microservice 🚀

A backend microservice built with **FastAPI**, **Selenium**, and **MongoDB** to collect, store, and analyze LinkedIn Company Page data. The project also includes **AI-powered summaries** using **Google Gemini**.

## What This Project Does

* Scrapes LinkedIn company page data (followers, industry, description)
* Saves scraped data in MongoDB to avoid repeated scraping
* Allows **force refresh** to fetch fresh data anytime
* Generates **AI-based company summaries** using Gemini
* Provides clean REST APIs with Swagger documentation

## Tech Stack

* **Backend:** FastAPI
* **Scraping:** Selenium + Chrome
* **Database:** MongoDB (Local or Atlas)
* **AI:** Google Gemini API
* **API Testing:** Postman

## Prerequisites

Make sure you have the following installed:

* Python **3.9 or above**
* MongoDB (running locally or Atlas connection)
* Google Chrome browser
* Git

## Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/sSumankumari/LinkedIn_Insights.git
cd LinkedIn_Insights
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables Setup

Create a `.env` file in the root directory and add the following values:

```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017/linkedin_db

# LinkedIn Login (Required for scraping)
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password

# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key
```

## Running the Application

Start the FastAPI server using:

```bash
python main.py
```

Once running, the server will be available at:

```
http://127.0.0.1:8000
```

## API Documentation (Swagger)

FastAPI automatically provides API documentation.

Open your browser and visit:

```
http://127.0.0.1:8000/docs
```

You can test all APIs directly from this page.

## API Endpoints Overview

### 🔹 Company Page APIs

| Method | Endpoint                       | Description                                      |
| ------ | ------------------------------ | ------------------------------------------------ |
| GET    | `/page/{page_id}`              | Get company data (DB first, scrape if not found) |
| GET    | `/page/{page_id}?refresh=true` | Force fresh scraping and update DB               |
| GET    | `/page/{page_id}/summary`      | Generate AI-based company summary                |

### 🔹 Search API

| Method | Endpoint        | Description                                      |
| ------ | --------------- | ------------------------------------------------ |
| GET    | `/pages/search` | Search companies by name, industry, or followers |

### 🔹 Related Data APIs

| Method | Endpoint                    | Description              |
| ------ | --------------------------- | ------------------------ |
| GET    | `/page/{page_id}/posts`     | Get recent company posts |
| GET    | `/page/{page_id}/employees` | Get company employees    |
| GET    | `/post/{post_id}/comments`  | Get comments for a post  |

## Using Postman for Testing

1. Open **Postman**
2. Import the provided Postman collection JSON file
3. Use requests like:

   * `Get Page Details`
   * `Force Refresh`
   * `Get AI Summary`

This makes the project easy to **present and demo**.

## How Scraping Works (Simple Explanation)

Because LinkedIn blocks bots aggressively, this project uses a **safe hybrid approach**:

1. Scrapes real company data from hidden JSON inside the page source
2. Stores valid scraped data in MongoDB
3. If some data (like comments) is blocked, mock/sample data is used

This ensures:

* APIs never break
* Database relations remain testable
* Assignment/demo requirements are satisfied

## 🧪 API Testing
A Postman collection (`LinkedIn Insights Microservice.postman_collection.json`) is included to easily test and demo all APIs.

## Project Folder Structure

```
LinkedIn_Insights/
├── config/
│   └── db.py                 # MongoDB connection
├── controllers/
│   ├── scraper.py            # Selenium scraping logic
│   └── summary_generator.py  # Gemini AI integration
├── routes/
│   └── page_routes.py        # API routes
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
└── .env                      # Environment variables
```

## Disclaimer

This project is created **only for learning and assignment purposes**. Scraping LinkedIn may violate their Terms of Service. Use responsibly.
