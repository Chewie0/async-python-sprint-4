import asyncio
from http import HTTPStatus
import pytest
import pytest_asyncio
from httpx import AsyncClient

from .main import app
from src.core.config import settings


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def client():
    async with AsyncClient(
            app=app, base_url=f'http://{settings.project_host}:{settings.project_port}') as c:
        yield c


@pytest.mark.asyncio
async def test_create_url(client):
    response = await client.post('/api/v1/urls/',
                                 json={'original_url': 'https://www.google.com/'}
                                 )
    assert response.status_code == HTTPStatus.CREATED
    assert 'short_url' in response.json()


@pytest.mark.asyncio
async def test_redirect_to_origin_url(client):
    response = await client.post('/api/v1/urls/',
                                 json={'original_url': 'http://ya.ru'}
                                 )
    shot_url = response.json().get('short_url')
    get_short_url = await client.get(shot_url)
    assert get_short_url.status_code == HTTPStatus.TEMPORARY_REDIRECT
    assert get_short_url.headers.get('Location') == 'http://ya.ru'


@pytest.mark.asyncio
async def test_create_multi_urls(client):
    response = await client.post('/api/v1/urls/batch/',
                                 json=[
                                     {'original_url': 'https://www.google.com/'},
                                     {'original_url': 'http://ya.ru'}
                                 ]
                                 )
    assert response.status_code == HTTPStatus.CREATED
    results = response.json()
    assert isinstance(results, list)
    assert len(results) == 2
    for result in results:
        assert isinstance(result, dict)
        assert result.get('short_url')


@pytest.mark.asyncio
async def test_delete_url(client):
    response = await client.post('/api/v1/urls/',
                                 json={'original_url': 'https://www.google.com/'}
                                 )
    short_url = response.json().get('short_url')
    delete_response = await client.delete(f'{short_url}')
    assert delete_response.json().get('short_url') == short_url
    assert delete_response.json().get('deleted')
    get_response = await client.get(response.json().get('short_url'))
    assert get_response.status_code == HTTPStatus.GONE


@pytest.mark.asyncio
async def test_get_status(client):
    response = await client.post('/api/v1/urls/',
                                 json={'original_url': 'https://www.google123456.com/'}
                                 )
    shot_url = response.json().get('short_url')
    await client.get(shot_url)
    await client.get(shot_url)
    status_response = await client.get(f'{shot_url}/status/')
    assert status_response.json().get('click_count') == 2
    status_response_full = await client.get(f'{shot_url}/status/?full-info=true')
    results = status_response_full.json()
    assert len(results) == 2
    for result in results:
        assert result.get('created_at')
        assert result.get('client_host')
        assert result.get('client_port')


@pytest.mark.asyncio
async def test_ping_db(client):
    response = await client.get('/api/v1/db/ping')
    assert response.status_code == HTTPStatus.OK
