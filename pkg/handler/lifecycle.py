from fastapi import APIRouter, FastAPI
from fastapi.routing import Lifespan
from requests import Session
from uvicorn import Config

router = APIRouter()

@router.lifespan
class LifeCycle(Lifespan): 
    def __init__(self, app: FastAPI, db: Session, config: Config):
        self.app = app
        self.db = db
        self.config = config
        self._setup()

    def _setup(self):
        self.app.add_event_handler("startup", self._startup)
        self.app.add_event_handler("shutdown", self._shutdown)

    async def _startup(self):
        print("Starting up")

    async def _shutdown(self):
        print("Shutting down")

    def __del__(self):
        self.db.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def __enter__(self):
        return self