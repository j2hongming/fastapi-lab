from fastapi import APIRouter
from ...core import Tags
from ..endpoints import users, items

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=[Tags.users])
api_router.include_router(items.router, prefix="/items", tags=[Tags.items])