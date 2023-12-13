from src.models.urls_model import Urls as UrlsModel
from src.models.urls_model import UrlsClick as UrlClickModel
from src.schemes.url_schemes import UrlCreate, MultiUrlCreate

from .base import RepositoryDB


class UrlRepository(RepositoryDB[UrlsModel, UrlClickModel, UrlCreate, MultiUrlCreate]):
    pass


url_crud = UrlRepository(UrlsModel, UrlClickModel)
