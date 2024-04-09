from pkg.repository.base_repository import BaseRepository


class BaseService():
    def __init__(self, repo: BaseRepository):
        self.repo = repo
