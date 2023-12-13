import os
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = Field('short-url-service', env='PROJECT_NAME')
    PROJECT_HOST: str = Field('127.0.0.1', env='PROJECT_HOST')
    PROJECT_PORT: str = Field('8080', env='PROJECT_HOST')
    BASE_DIR: str = Field(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), env='BASE_DIR')
    DB_DSN: str = Field(env='DB_DSN')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
