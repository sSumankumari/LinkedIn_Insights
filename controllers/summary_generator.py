import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash-lite')

def generate_ai_summary(page_data: dict, recent_posts: list) -> str:
    try:
        posts_text = "\n".join([f"- {p.get('content', '')[:100]}..." for p in recent_posts])

        prompt = f"""
        Act as a professional business analyst. 
        Analyze the following LinkedIn page data and provide a concise summary that include:

        Company Name: {page_data.get('name')}
        Industry: {page_data.get('industry')}
        Description: {page_data.get('description')}
        Follower Count: {page_data.get('followers')}

        Recent Post Topics:
        {posts_text}

        Please provide a response with:
        1. A 2-sentence executive summary of what the company does.
        2. The primary tone of their content (e.g., Hiring, Educational, Promotional).
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error generating summary: {str(e)}"