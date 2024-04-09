from fastapi import FastAPI
from api.handlers.embrapa_handler import router as embrapa_router
import uvicorn

from internal.repository.embrapa_repo import EmbrapaRepo
from internal.services.embrapa_service import EmbrapaService
from pkg.db.sqlitedb import SqliteDb


app = FastAPI()

app.include_router(embrapa_router, prefix="/embrapa")
# app.include_router(LifeCycle.router, tags=["lifecycle"])

# Produção
# http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv

# Processamento
# http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv
# http://vitibrasil.cnpuv.embrapa.br/download/ProcessaAmericanas.csv
# http://vitibrasil.cnpuv.embrapa.br/download/ProcessaMesa.csv
# http://vitibrasil.cnpuv.embrapa.br/download/ProcessaSemclass.csv

# Comercialização
# http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv

# Importação
# http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv
# http://vitibrasil.cnpuv.embrapa.br/download/ImpEspumantes.csv
# http://vitibrasil.cnpuv.embrapa.br/download/ImpFrescas.csv
# http://vitibrasil.cnpuv.embrapa.br/download/ImpPassas.csv
# http://vitibrasil.cnpuv.embrapa.br/download/ImpSuco.csv

# Exportação
# http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv
# http://vitibrasil.cnpuv.embrapa.br/download/ExpEspumantes.csv
# http://vitibrasil.cnpuv.embrapa.br/download/ExpUva.csv
# http://vitibrasil.cnpuv.embrapa.br/download/ExpSuco.csv

if __name__ == "__main__":
    db = SqliteDb()
    conn = db.connect(dbname='embrapa', conn_str='db/embrapa.db')
    repo = EmbrapaRepo(conn)
    service = EmbrapaService(repo)  
    service.processarDadosProducao()  
    service.processarDadosProcessamento() 
    service.processarArquivoComercializacao()
    uvicorn.run(app, host="0.0.0.0", port=8000)