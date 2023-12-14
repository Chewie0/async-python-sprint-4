import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = 'short-url-service'
    project_host: str = '127.0.0.1'
    project_port: int = 8080
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_dsn: str = ...
    db_echo: bool = False

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
