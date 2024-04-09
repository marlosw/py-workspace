from typing import List
import pandas as pd
from pandas import read_csv
import requests

from internal.dto.embrapa_producao_dto import EmbrapaProcessamentoDTO, EmbrapaProducaoDTO
from internal.repository.embrapa_repo import EmbrapaRepo


class EmbrapaService():
    def __init__(self, repo: EmbrapaRepo):
        self.repo = repo

    def processarDadosProducao(self): 
    # Download the file
        url = 'http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv'
        s = requests.Session()
        r = s.get(url, stream=True)
        p = read_csv(r.raw, header=0, sep=';', encoding='latin1')
        p['produto'] = p['produto'].str.strip()
        keys = []
        tipos = []
        tipos_regs = []
        for line in p.iterrows():
            id = str(line[1]['id'])
            produto = str(line[1]['produto'])
            if produto.isupper():
                main_id = id
                tipo = produto
                reg = 'SINTETICO'
            else:
                reg = 'ANALITICO'  
            keys.append(main_id + '-' + id)
            tipos.append(tipo)
            tipos_regs.append(reg)
        p.insert(0, 'key', keys)
        p.insert(1, 'tipo', tipos)
        p.insert(6, 'reg', tipos_regs)
        df = p.melt(id_vars=['key', 'tipo', 'id', 'produto', 'reg'], value_vars=list(p.columns[2:]), var_name='ano', value_name='quantidade')
        df['ano'] = pd.to_numeric(df['ano'], errors='coerce').fillna(0).astype(int)
        df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce').fillna(0).astype(int)

        self.repo.saveDataframe(df, 'producao')


# http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv
# http://vitibrasil.cnpuv.embrapa.br/download/ProcessaAmericanas.csv
# http://vitibrasil.cnpuv.embrapa.br/download/ProcessaMesa.csv
# http://vitibrasil.cnpuv.embrapa.br/download/ProcessaSemclass.csv
    def processarDadosProcessamento(self):
        self.processarArquivoProcessamento('http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv', classe='VINIFERAS', table_name='processamento', if_exists='replace')
        self.processarArquivoProcessamento('http://vitibrasil.cnpuv.embrapa.br/download/ProcessaAmericanas.csv', classe='AMERICANAS', table_name='processamento', if_exists='append')
        self.processarArquivoProcessamento('http://vitibrasil.cnpuv.embrapa.br/download/ProcessaMesa.csv', classe='MESA', table_name='processamento', if_exists='append')

    def processarArquivoProcessamento(self, file_name: str, classe, table_name: str, if_exists='replace'): 
    # Download the file
        url = file_name # 'http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv'
        s = requests.Session()
        r = s.get(url, stream=True)
        p = read_csv(r.raw, header=0, sep='\t', encoding='latin1')
        p['cultivar'] = p['cultivar'].str.strip()
        keys = []
        tipos = []
        tipos_regs = []
        classes = []
        for line in p.iterrows():
            id = str(line[1]['id'])
            control = str(line[1]['control'])             
            if control.isupper():
                main_id = id
                tipo = control
                reg = 'SINTETICO'
            else:
                reg = 'ANALITICO'  
            keys.append(main_id + '-' + id)
            tipos.append(tipo)
            tipos_regs.append(reg)
            classes.append(classe)
        p.insert(0, 'key', keys)
        p.insert(1, 'tipo', tipos)
        p.insert(6, 'reg', tipos_regs)
        p.insert(7, 'classe', classes)
        df = p.melt(id_vars=['id', 'key', 'tipo', 'reg', 'classe', 'control', 'cultivar'], value_vars=list(p.columns[2:]), var_name='ano', value_name='quantidade')
        df['ano'] = pd.to_numeric(df['ano'], errors='coerce').fillna(0).astype(int)
        df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce').fillna(0).astype(int)
        # df.to_csv('ProcessaViniferas.csv', index=False)
        
        self.repo.saveDataframe(df, table_name, if_exists)

    def processarArquivoComercializacao(self): 
    # Download the file
        url = 'http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv'
        s = requests.Session()
        r = s.get(url, stream=True)
        header = ['id', 'control', 'cultivar']        
        p = read_csv(r.raw, header=None, sep=';', encoding='latin1')
        ano = 1970
        for col in p.columns[3:]:
            header.append(str(ano))
            ano += 1        
        p.columns = header
        p['cultivar'] = p['cultivar'].str.strip()
        print(p)
        keys = []
        tipos = []
        tipos_regs = []
        for line in p.iterrows():
            id = str(line[1]['id'])
            control = str(line[1]['control'])             
            if control.isupper():
                main_id = id
                tipo = control
                reg = 'SINTETICO'
            else:
                reg = 'ANALITICO'  
            keys.append(main_id + '-' + id)
            tipos.append(tipo)
            tipos_regs.append(reg)
        p.insert(0, 'key', keys)
        p.insert(1, 'tipo', tipos)
        p.insert(6, 'reg', tipos_regs)
        df = p.melt(id_vars=['id', 'key', 'tipo', 'reg', 'control', 'cultivar'], value_vars=list(p.columns[2:]), var_name='ano', value_name='quantidade')
        df['ano'] = pd.to_numeric(df['ano'], errors='coerce').fillna(0).astype(int)
        df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce').fillna(0).astype(int)        
        # df.to_csv('comercializacao.csv', index=False)        
        self.repo.saveDataframe(df, 'comercializacao', 'replace')
    
    def selectProducaoPorAno(self, ano) -> List[EmbrapaProducaoDTO]:
        prods = self.repo.selectProducaoPorAno(ano)
        return prods

    def selectProcessamentoPorAno(self, ano) -> List[EmbrapaProcessamentoDTO]:
        prods = self.repo.selectProcessamentoPorAno(ano)
        return prods
