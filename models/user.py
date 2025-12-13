def user_schema(data: dict) -> dict:
    return {
        "page_id": data.get("page_id"),
        "name": data.get("name"),
        "designation": data.get("designation"),
        "profile_url": data.get("profile_url"),
    }
