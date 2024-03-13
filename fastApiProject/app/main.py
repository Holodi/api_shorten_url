from fastapi import FastAPI, HTTPException
from app.models import Link
import pymongo

app = FastAPI()
client = pymongo.MongoClient("mongodb://admin:password@mongo:27017/")
db = client["url_shortener"]
collection = db["links"]


@app.post("/shorten/")
async def shorten_url(link: Link):
    doc = {"original_url": link.original_url}
    result = collection.insert_one(doc)
    short_id = str(result.inserted_id)
    return {"short_id": short_id}


@app.get("/redirect/{short_id}/")
async def redirect(short_id: str):
    doc = collection.find_one_and_update(
        {"_id": short_id},
        {"$inc": {"click_count": 1}}
    )
    if doc:
        original_url = doc["original_url"]
        return {"redirect_url": original_url}
    else:
        raise HTTPException(status_code=404, detail="Link not found")


@app.get("/")
async def homepage():
    return {"message": "Welcome to the URL shortener service"}


@app.get("/clicks/{short_id}/")
async def get_click_count(short_id: str):
    doc = collection.find_one({"_id": short_id})
    if doc:
        click_count = doc.get("click_count", 0)
        return {"click_count": click_count}
    else:
        raise HTTPException(status_code=404, detail="Link not found")


@app.get("/user_links/{user_id}/")
async def get_user_links(user_id: str):
    user_links = []
    cursor = collection.find({"user_id": user_id})
    for link in cursor:
        link_info = {
            "original_url": link["original_url"],
            "click_count": link.get("click_count", 0)
        }
        user_links.append(link_info)
    return user_links
