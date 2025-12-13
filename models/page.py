def page_schema(data: dict) -> dict:
    return {
        "page_id": data.get("page_id"),
        "name": data.get("name"),
        "url": data.get("url"),
        "linkedin_id": data.get("linkedin_id"),
        "profile_pic": data.get("profile_pic"),
        "description": data.get("description"),
        "website": data.get("website"),
        "industry": data.get("industry"),
        "followers": data.get("followers"),
        "head_count": data.get("head_count"),
        "specialities": data.get("specialities", []),
    }
