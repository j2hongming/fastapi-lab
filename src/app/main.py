from typing import Union
import secrets
from functools import lru_cache

from fastapi import FastAPI, Depends, Security, status
from fastapi.exceptions import HTTPException
from fastapi.security.api_key import APIKeyHeader
from .routers.v1 import api_router
from .core import ModelName
from .core.config import Settings



api_key_header_auth = APIKeyHeader(
    name="X-API-KEY",
    description="Mandatory API Token, required for all endpoints",
    auto_error=True,
)


async def get_api_key(api_key_header: str = Security(api_key_header_auth)):
    correct_api_key = secrets.compare_digest(api_key_header, "12345")
    if not correct_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key",
        )

app = FastAPI(dependencies=[Security(get_api_key)])
# add the v1 routers
app.include_router(api_router, prefix='/v1')

# load environment variables
@lru_cache()
def get_settings():
    return Settings()



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }

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