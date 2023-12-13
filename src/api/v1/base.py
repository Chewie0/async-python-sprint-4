import sys
from fastapi import APIRouter
from .url import router
from .ping_db import ping_db_router

api_router = APIRouter()

@api_router.get('/')
async def root_handler():
    return {'version': 'v1'}


@api_router.get('/info')
async def info_handler():
    return {
        'api': 'v1',
        'python': sys.version_info
    }

api_router.include_router(router, prefix="/urls", tags=["urls"])
api_router.include_router(ping_db_router, prefix="/db", tags=["db"])