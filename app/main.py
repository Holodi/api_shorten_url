from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymongo

app = FastAPI()
client = pymongo.MongoClient("mongodb://admin:password@mongo:27017/")
db = client["url_shortener"]
collection = db["links"]


class Link(BaseModel):
    original_url: str


@app.post("/shorten/")
async def shorten_url(link: Link):
    doc = {"original_url": link.original_url}
    result = collection.insert_one(doc)
    short_id = str(result.inserted_id)
    return {"short_id": short_id}


@app.get("/redirect/{short_id}/")
async def redirect(short_id: str):
    doc = collection.find_one({"_id": short_id})
    if doc:
        original_url = doc["original_url"]
        return {"redirect_url": original_url}
    else:
        raise HTTPException(status_code=404, detail="Link not found")


@app.get("/")
async def homepage():
    return {"message": "Welcome to the URL shortener service"}
