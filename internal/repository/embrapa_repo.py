from typing import List
from internal.dto.embrapa_producao_dto import EmbrapaProcessamentoDTO, EmbrapaProducaoDTO
from internal.entity.embrapa_producao import EmbrapaProducao
from pkg.db.db import DbConnection
from pkg.repository.base_repository import BaseRepository


class EmbrapaRepo(BaseRepository):
    def __init__(self, conn: DbConnection):
        super().__init__(conn)

    def selectProducaoPorAno(self, ano: int) -> List[EmbrapaProducaoDTO]:
        cursor = self.conn.db.execute("SELECT * FROM producao WHERE ano = ?", (ano,))
        cur = cursor.fetchall()
        prods: List[EmbrapaProducaoDTO] = []
        for row in cur:
            prod = EmbrapaProducaoDTO(id=row[3], key=row[1], tipo=row[2], ano=row[6], produto=row[4], reg=row[5], valor=row[7])
            prods.append(prod)
        return prods
    
    def selectProcessamentoPorAno(self, ano: int) -> List[EmbrapaProcessamentoDTO]:
        cursor = self.conn.db.execute("SELECT * FROM processamento WHERE ano = ?", (ano,))
        cur = cursor.fetchall()
        prods: List[EmbrapaProcessamentoDTO] = []
        for row in cur:
            prod = EmbrapaProcessamentoDTO(id=row[1], key=row[2], tipo=row[3], reg=row[4], classe=row[5], control=row[6], cultivar=row[7], ano=row[8], valor=row[9])
            prods.append(prod)
        return prods
