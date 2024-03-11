import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Link(BaseModel):
    original_url: str


@app.post("/shorten/")
async def shorten_url(link: Link):
    with open("links.json", "r") as file:
        links = json.load(file)
    short_id = len(links) + 1
    links[str(short_id)] = link.original_url
    with open("links.json", "w") as file:
        json.dump(links, file)
    return {"short_id": short_id}


@app.get("/redirect/{short_id}/")
async def redirect(short_id: int):
    with open("links.json", "r") as file:
        links = json.load(file)
    original_url = links.get(str(short_id))
    if original_url:
        return {"redirect_url": original_url}
    else:
        raise HTTPException(status_code=404, detail="Link not found")


@app.get("/")
async def homepage():
    return {"message": "Welcome to the URL shortener service"}
