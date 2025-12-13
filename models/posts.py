def post_schema(data: dict) -> dict:
    return {
        "page_id": data.get("page_id"),
        "post_id": data.get("post_id"),
        "content": data.get("content"),
        "likes": data.get("likes"),
        "comments_count": data.get("comments_count"),
        "created_at": data.get("created_at"),
    }
