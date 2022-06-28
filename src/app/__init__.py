from typing import Union
from enum import Enum

from fastapi import FastAPI, Query, Header
from pydantic import BaseModel, HttpUrl

class Tags(Enum):
    items = "items"
    users = "users"

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

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

class UserBase(BaseModel):
    username: str
    email: str
    full_name: Union[str, None] = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/", tags=[Tags.items])
async def read_item(skip: int = 0, limit: int = 10, 
q: str = Query(min_length=3, title="Query string", deprecated=True),
hidden_query: Union[str, None] = Query(default=None, title="Hidden Query string", include_in_schema=False),
user_agent: Union[str, None] = Header(default=None)):
    return fake_items_db[skip : skip + limit]

@app.post("/items/", tags=[Tags.items], summary="Create an item")
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

@app.get("/items/{item_id}", tags=[Tags.items])
async def read_item(item_id: int, needy: str, skip: int = 0, limit: Union[int, None] = None):
    return {"item_id": item_id}

@app.put("/items/{item_id}", tags=[Tags.items])
async def create_item(item_id: int, item: Item, q: Union[str, None] = Query(default=None, min_length=3, max_length=20, regex="^fixedquery$")):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images

@app.post("/user/", response_model=UserOut, tags=[Tags.users])
async def create_user(user: UserIn):
    return user

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/keyword-weights/", response_model=dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}