from pydantic import BaseModel


class LinkData(BaseModel):
    original_url: str


class LinkDB(LinkData):
    short_id: int

    class Config:
        orm_mode = True
