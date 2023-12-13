import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.core.config import settings

from src.api.v1 import base
from src.core.logger import logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)
app.include_router(base.api_router, prefix='/api/v1')

if __name__ == '__main__':
    logger.info(f'Start server on http://{settings.PROJECT_HOST}:{settings.PROJECT_PORT}')
    uvicorn.run(
        'main:app',
        host=settings.PROJECT_HOST,
        port=settings.PROJECT_PORT,
    )