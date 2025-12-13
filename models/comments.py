def comment_schema(data: dict) -> dict:
    return {
        "comment_id": data.get("comment_id"),
        "post_id": data.get("post_id"),
        "page_id": data.get("page_id"),
        "author_name": data.get("author_name"),
        "content": data.get("content"),
        "created_at": data.get("created_at")
    }