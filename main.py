from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.handlers.embrapa_handler import router as embrapa_router
import uvicorn

from internal.repository.embrapa_repo import EmbrapaRepo
from internal.services.embrapa_service import EmbrapaService
from pkg.db.sqlitedb import SqliteDb


@asynccontextmanager
async def lifespan(router: FastAPI):
    print("Setting up application")
    db = SqliteDb()
    conn = db.connect(dbname='embrapa', conn_str='db/embrapa.db')
    repo = EmbrapaRepo(conn)
    service = EmbrapaService(repo)
    return service

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})
app.include_router(embrapa_router, prefix="/embrapa")

if __name__ == "__main__":
    db = SqliteDb()
    conn = db.connect(dbname='embrapa', conn_str='db/embrapa.db')
    repo = EmbrapaRepo(conn)
    service = EmbrapaService(repo)  
    service.processarDadosProducao()  
    service.processarDadosProcessamento() 
    service.processarDadosComercializacao()
    service.processarDadosImportacao()
    service.processarDadosExportacao()

    uvicorn.run(app, host="0.0.0.0", port=8000)