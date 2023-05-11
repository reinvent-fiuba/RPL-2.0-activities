import uvicorn
from fastapi import FastAPI

from src.routers.activities import router as activities_router
from src.routers.categories import router as categories_router

app = FastAPI()

app.include_router(activities_router)
app.include_router(categories_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


def start():
    print("Starting RPL 2.0 Activities Service...")
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
