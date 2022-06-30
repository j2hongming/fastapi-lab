from typing import Union

from fastapi import FastAPI
from .routers.v1 import api_router
from .core import ModelName



app = FastAPI()
app.include_router(api_router, prefix='/v1')


@app.get("/")
async def root():
    return {"message": "Hello World"}



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