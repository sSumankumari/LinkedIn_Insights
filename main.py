from fastapi import FastAPI
import uvicorn
from routes.page_routes import router
import os

app = FastAPI(title="LinkedIn Insights Microservice")
app.include_router(router)

@app.get("/")
def root():
    return {"status": "LinkedIn Insights Service Running"}

if __name__ == "__main__":
    print("Starting FastAPI server at http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)