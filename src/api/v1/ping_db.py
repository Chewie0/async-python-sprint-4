from asyncpg import ConnectionDoesNotExistError
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import OperationalError
from starlette.responses import JSONResponse

from src.core.logger import logger
from src.db.db import get_session

ping_db_router = APIRouter()


@ping_db_router.get("/ping")
async def ping(session: AsyncSession = Depends(get_session)):
    try:
        logger.info(f'Ping database')
        await session.execute(text("SELECT 1"))
        return JSONResponse(status_code=status.HTTP_200_OK, content={'details': 'Database connection is ok'})
    except OperationalError:
        logger.error(f'Ping database err')
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'details': 'Error database connection'})
    except ConnectionDoesNotExistError:
        logger.error(f'Ping database err')
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'details': 'Connection to database was closed'})
