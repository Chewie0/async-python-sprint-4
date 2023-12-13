from typing import Any, Optional, Annotated, Union
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.services.url import url_crud
from src.schemes import url_schemes
from src.db.db import get_session
from src.core.logger import logger

router = APIRouter()


@router.get('/{url_id}', response_model=url_schemes.UrlResponse, description='Redirect to original URL if it exists')
async def get_origin_url(*, db: AsyncSession = Depends(get_session), url_id: str, request: Request) -> Any:
    entity_url = await url_crud.get(db=db, obj_id=url_id)
    logger.info(f'Get url {url_id}')
    if not entity_url:
        logger.info(f'No such url in database {url_id}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    elif entity_url.deleted:
        logger.info(f'Url is deleted {url_id}')
        raise HTTPException(status_code=status.HTTP_410_GONE, detail='Url is deleted')
    await url_crud.add_click(db=db, obj_in=entity_url.id, request=request)
    return RedirectResponse(entity_url.original_url)


@router.post('/', response_model=url_schemes.UrlResponse, status_code=status.HTTP_201_CREATED)
async def create_short_url(*, db: AsyncSession = Depends(get_session), entity_in: url_schemes.UrlCreate) -> Any:
    entity_url = await url_crud.create(db=db, obj_in=entity_in)
    logger.info(f'Create new url {entity_url.id}')
    return entity_url


@router.post('/batch/', response_model=url_schemes.MultiUrlResponse, status_code=status.HTTP_201_CREATED)
async def create_short_url(*, db: AsyncSession = Depends(get_session), entity_in: url_schemes.MultiUrlCreate) -> Any:
    entity_urls = await url_crud.create_multi(db=db, obj_in=entity_in)
    logger.info('Multiple create new urls')
    return entity_urls


@router.delete('/{url_id}', response_model=url_schemes.UrlResponse, description='Set status deleted to url')
async def delete_url(*, db: AsyncSession = Depends(get_session), url_id: str) -> Any:
    entity_url = await url_crud.get(db=db, obj_id=url_id)
    if not entity_url:
        logger.info(f'No such url in database {url_id}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    await url_crud.delete(db=db, obj_id=url_id)
    logger.info(f'Delete url {entity_url.id}')
    return entity_url


@router.get('/{url_id}/status/', response_model=Union[url_schemes.UrlStatus | url_schemes.UrlStatusCount],
            description='Get status of url')
async def get_status(*, db: AsyncSession = Depends(get_session),
                     full_info: Annotated[Optional[bool], Query(alias="full-info")] = False,
                     max_result: Annotated[Optional[int], Query(alias="max-result")] = 10, offset: int = 0,
                     url_id: str) -> Any:
    entity_url = await url_crud.get(db=db, obj_id=url_id)
    if not entity_url:
        logger.info(f'No such url in database {url_id}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    result = await url_crud.get_status(db=db, obj_id=url_id, full_info=full_info, limit=max_result, offset=offset)
    if isinstance(result, int):
        logger.info(f'Get status of url {url_id}')
        return JSONResponse(status_code=status.HTTP_200_OK, content={'click_count': result})
    return result
