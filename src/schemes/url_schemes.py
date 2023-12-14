from datetime import datetime as dt
from typing import List
from pydantic import UUID4, computed_field, BaseModel, RootModel
from src.core import settings


class UrlBase(BaseModel):
    original_url: str


class UrlCreate(UrlBase):
    pass


class UrlUpdate(BaseModel):
    deleted: bool


class MultiUrlCreate(RootModel):
    root: List[UrlBase]


class UrlResponse(UrlBase):
    id: UUID4
    original_url: str
    created_at: dt
    deleted: bool

    @computed_field
    def short_url(self) -> str:
        return f'http://{settings.project_host}:{settings.project_port}/api/v1/urls/{self.id}'

    class Config:
        populate_by_name = True
        from_attributes = True


class MultiUrlResponse(RootModel):
    root: List[UrlResponse]


class UrlClickResponse(BaseModel):
    client_host: str
    client_port: int
    created_at: dt

    class Config:
        from_attributes = True


class UrlStatusCount(BaseModel):
    click_count: int


class UrlStatus(RootModel):
    root: List[UrlClickResponse]
