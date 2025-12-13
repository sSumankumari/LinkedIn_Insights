from fastapi import FastAPI
from routes.page_routes import router

app = FastAPI(title="LinkedIn Insights Microservice")
app.include_router(router)

@app.get("/")
def root():
    return {"status": "LinkedIn Insights Service Running"}
