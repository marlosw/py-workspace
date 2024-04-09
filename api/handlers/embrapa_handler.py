import json
import jsonpickle
from fastapi import APIRouter
from internal.services.embrapa_service import EmbrapaService
from internal.repository.embrapa_repo import EmbrapaRepo
from pkg.db.sqlitedb import SqliteDb

router = APIRouter()

service: EmbrapaService

@router.get("/producao/{ano}")
async def getProducaoPorAno(ano: int):
    db = SqliteDb()
    conn = db.connect(dbname='embrapa', conn_str='db/embrapa.db')
    repo = EmbrapaRepo(conn)
    service = EmbrapaService(repo)  
    list = service.selectProducaoPorAno(ano)
    # jsonpickle.set_encoder_options('json', indent=2)
    return jsonpickle.encode(list, unpicklable=False)

@router.get("/processamento/{ano}")
async def getProcessamentoPorAno(ano: int):
    db = SqliteDb()
    conn = db.connect(dbname='embrapa', conn_str='db/embrapa.db')
    repo = EmbrapaRepo(conn)
    service = EmbrapaService(repo)  
    list = service.selectProcessamentoPorAno(ano)
    jsonpickle.set_encoder_options('json', indent=2)
    return jsonpickle.encode(list, unpicklable=False)