from pydantic import BaseModel


class LinkData(BaseModel):
    original_url: str
    click_count: int = 0


class LinkDB(LinkData):
    short_id: str

    class Config:
        orm_mode = True


class Link(BaseModel):
    original_url: str
