from fastapi import APIRouter
from internal.services.embrapa_service import EmbrapaService
from internal.repository.embrapa_repo import EmbrapaRepo
from pkg.db.sqlitedb import SqliteDb

router = APIRouter()

@router.get("/producao/{ano}")
async def getProducaoPorAno(ano: int):
    db = SqliteDb()
    conn = db.connect(dbname='embrapa', conn_str='db/embrapa.db')
    repo = EmbrapaRepo(conn)
    service = EmbrapaService(repo)  
    list = service.selectProducaoPorAno(ano)
    return list 

@router.get("/processamento/{ano}")
async def getComercializacaoPorAno(ano: int):
    db = SqliteDb()
    conn = db.connect(dbname='embrapa', conn_str='db/embrapa.db')
    repo = EmbrapaRepo(conn)
    service = EmbrapaService(repo)  
    list = service.selectProcessamentoPorAno(ano)
    return list

@router.get("/comercializacao/{ano}")
async def getComercializacaoPorAno(ano: int):
    db = SqliteDb()
    conn = db.connect(dbname='embrapa', conn_str='db/embrapa.db')
    repo = EmbrapaRepo(conn)
    service = EmbrapaService(repo)  
    list = service.selectComercializacaoPorAno(ano)
    return list

@router.get("/exportacao/{ano}")
async def getExportacaoPorAno(ano: int):
    db = SqliteDb()
    conn = db.connect(dbname='embrapa', conn_str='db/embrapa.db')
    repo = EmbrapaRepo(conn)
    service = EmbrapaService(repo)  
    list = service.selectExportacaoPorAno(ano)
    return list

@router.get("/importacao/{ano}")
async def getImportacaoPorAno(ano: int):
    db = SqliteDb()
    conn = db.connect(dbname='embrapa', conn_str='db/embrapa.db')
    repo = EmbrapaRepo(conn)
    service = EmbrapaService(repo)  
    list = service.selectImportacaoPorAno(ano)
    return list

