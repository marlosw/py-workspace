from typing import List
from internal.dto.embrapa_producao_dto import EmbrapaComercializacaoDTO, EmbrapaExportacaoDTO, EmbrapaImportacaoDTO, EmbrapaProcessamentoDTO, EmbrapaProducaoDTO
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
        # prods = []
        for row in cur:
            prod = EmbrapaProcessamentoDTO(id=row[1], key=row[2], tipo=row[3], reg=row[4], classe=row[5], control=row[6], cultivar=row[7], ano=row[8], valor=row[9])
            prods.append(prod)
        return prods

    def selectComercializacaoPorAno(self, ano: int) -> List[EmbrapaComercializacaoDTO]:
        cursor = self.conn.db.execute("SELECT * FROM comercializacao WHERE ano = ?", (ano,))
        cur = cursor.fetchall()
        prods: List[EmbrapaComercializacaoDTO] = []
        for row in cur:
            prod = EmbrapaComercializacaoDTO(id=row[1], key=row[2], tipo=row[3], reg=row[4], control=row[5], cultivar=row[6], ano=row[7], quantidade=row[8])
            prods.append(prod)
        return prods

    def selectImportacaoPorAno(self, ano: int) -> List[EmbrapaImportacaoDTO]:
        cursor = self.conn.db.execute("SELECT * FROM importacao WHERE ano = ?", (ano,))
        cur = cursor.fetchall()
        prods: List[EmbrapaImportacaoDTO] = []
        for row in cur:
            prod = EmbrapaImportacaoDTO(id=row[1], pais=row[2], classe = row[3], ano=row[4], quantidade=row[5], valor=row[6])
            prods.append(prod)
        return prods

    def selectExportacaoPorAno(self, ano: int) -> List[EmbrapaExportacaoDTO]:
        cursor = self.conn.db.execute("SELECT * FROM exportacao WHERE ano = ?", (ano,))
        cur = cursor.fetchall()
        prods: List[EmbrapaExportacaoDTO] = []
        for row in cur:
            prod = EmbrapaExportacaoDTO(id=row[1], pais=row[2], classe = row[3], ano=row[4], quantidade=row[5], valor=row[6])
            prods.append(prod)
        return prods
