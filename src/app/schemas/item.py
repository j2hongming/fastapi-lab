from typing import Union
from pydantic import BaseModel, HttpUrl

class TestImage(BaseModel):
    url: str
    name: str

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: set[str] = set()
    image: Union[TestImage, None] = None
    images: Union[list[Image], None] = None