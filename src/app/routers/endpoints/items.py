from typing import Union

from fastapi import APIRouter, Query, Header
from ...schemas.item import Item, Image

router = APIRouter()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@router.get("/")
async def read_item(skip: int = 0, limit: int = 10, 
q: str = Query(min_length=3, title="Query string", deprecated=True),
hidden_query: Union[str, None] = Query(default=None, title="Hidden Query string", include_in_schema=False),
user_agent: Union[str, None] = Header(default=None)):
    return fake_items_db[skip : skip + limit]

@router.post("/", summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@router.get("/{item_id}")
async def read_item(item_id: int, needy: str, skip: int = 0, limit: Union[int, None] = None):
    return {"item_id": item_id}

@router.put("/{item_id}")
async def create_item(item_id: int, item: Item, q: Union[str, None] = Query(default=None, min_length=3, max_length=20, regex="^fixedquery$")):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

@router.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images