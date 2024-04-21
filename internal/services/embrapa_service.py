from typing import List
import numpy as np
import pandas as pd
from pandas import read_csv
import requests

from internal.dto.embrapa_producao_dto import EmbrapaComercializacaoDTO, EmbrapaExportacaoDTO, EmbrapaImportacaoDTO, EmbrapaProcessamentoDTO, EmbrapaProducaoDTO
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
        
        #Removendo acentos e colocando em maiúsculas
        cols = p.select_dtypes(include=['object']).columns
        p[cols] = p[cols].apply(lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.upper())

        df = p.melt(id_vars=['key', 'tipo', 'id', 'produto', 'reg'], value_vars=list(p.columns[2:]), var_name='ano', value_name='quantidade')
        df['ano'] = pd.to_numeric(df['ano'], errors='coerce').fillna(0).astype(int)
        df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce').fillna(0).astype(int)

        self.repo.saveDataframe(df, 'producao')

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

        #Removendo acentos e colocando em maiúsculas
        cols = p.select_dtypes(include=['object']).columns
        p[cols] = p[cols].apply(lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.upper())

        df = p.melt(id_vars=['id', 'key', 'tipo', 'reg', 'classe', 'control', 'cultivar'], value_vars=list(p.columns[2:]), var_name='ano', value_name='quantidade')
        df['ano'] = pd.to_numeric(df['ano'], errors='coerce').fillna(0).astype(int)
        df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce').fillna(0).astype(int)
        
        self.repo.saveDataframe(df, table_name, if_exists)

    def processarDadosComercializacao(self): 
        # Realizando o download do arquivo em memória
        url = 'http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv'
        s = requests.Session()
        r = s.get(url, stream=True)
        header = ['id', 'control', 'cultivar']      
        # Este arquivo não possui cabeçalho, então eu preciso criar um cabeçalho para ele  
        p = read_csv(r.raw, header=None, sep=';', encoding='latin1')
        ano = 1970
        for col in p.columns[3:]:
            header.append(str(ano))
            ano += 1        
        p.columns = header

        # Removendo os espaços em branco do campo cultivar
        p['cultivar'] = p['cultivar'].str.strip()

        # Adicionando campos para enriquecer os dados com uma chave, o tipo, o registro
        # O arquivo contém dados analíticos e sintéticos, então eu preciso identificar cada um deles.  
        # Para isso, eu criei um campo chamado reg, que conterá o tipo de registro analítico ou sintético.
        # O que diferencia um registro analítico de um sintético é que o sintético é todo em maiúsculo. 
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

        # Removendo acentos e colocando em maiúsculas
        cols = p.select_dtypes(include=['object']).columns
        p[cols] = p[cols].apply(lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.upper())

        # O arquivo vem com as colunas de quantidades pivoteadas pelo ano, então eu preciso derreter (unpivot) o dataframe     
        df = p.melt(id_vars=['id', 'key', 'tipo', 'reg', 'control', 'cultivar'], value_vars=list(p.columns[2:]), var_name='ano', value_name='quantidade')
        # Convertendo os tipos para criar a tabela no SQLITE com os tipos corretos
        df['ano'] = pd.to_numeric(df['ano'], errors='coerce').fillna(0).astype(int)
        df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce').fillna(0).astype(int)   
        # Salvando os dados no SQLITE     
        self.repo.saveDataframe(df, 'comercializacao', 'replace')
    
    def processarDadosImportacao(self):
        self.processarArquivoImportacao('http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv', classe='VINHOS_MESA', table_name='importacao', if_exists='replace')
        self.processarArquivoImportacao('http://vitibrasil.cnpuv.embrapa.br/download/ImpEspumantes.csv', classe='ESPUMANTES', table_name='importacao', if_exists='append')
        self.processarArquivoImportacao('http://vitibrasil.cnpuv.embrapa.br/download/ImpFrescas.csv', classe='UVAS_FRESCAS', table_name='importacao', if_exists='append')
        self.processarArquivoImportacao('http://vitibrasil.cnpuv.embrapa.br/download/ImpPassas.csv', classe='UVAS_PASSAS', table_name='importacao', if_exists='append')
        self.processarArquivoImportacao('http://vitibrasil.cnpuv.embrapa.br/download/ImpSuco.csv', classe='SUCO_UVA', table_name='importacao', if_exists='append')

    def processarArquivoImportacao(self, file_name: str, classe, table_name: str, if_exists='replace'): 
        # Realizando o download do arquivo em memória
        url = file_name
        s = requests.Session()
        r = s.get(url, stream=True)
        p = read_csv(r.raw, header=0, sep=';', encoding='latin1')

        # Removendo acentos e colocando em maiúsculas dos nomes das colunas
        p.rename(columns={'Id': 'ID', 'País': 'PAIS'}, inplace=True)        
        
        # Adicionando um campo para especificar a classe do produto, que é passada por parâmetro
        classes = []
        for line in p.iterrows():
            classes.append(classe)
        p.insert(2, 'CLASSE', classes)

        #Removendo acentos e colocando em maiúsculas
        cols = p.select_dtypes(include=['object']).columns
        p[cols] = p[cols].apply(lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.upper())

        # O arquivo contempla a quantidade e o valor em colunas alternadas, repetindo o ano.
        # Aqui eu estou dividindo o dataframe em dois, um para a quantidade e outro para o valor.  
        # Pegando as colunas de quantidade, com índices ímpares       
        cols_qtd = list(range(3, len(p.columns), 2))
        # Pegando as colunas de valor, com índices pares
        cols_val = list(range(4, len(p.columns), 2))

        # O arquivo vem com as colunas de valores e quantidades pivoteadas, então eu preciso derreter (unpivot) os dataframes
        df1 = p.melt(id_vars=['ID', 'PAIS', 'CLASSE'], value_vars=list(p.columns[cols_qtd]), var_name='ANO', value_name='QUANTIDADE')
        df2 = p.melt(id_vars=['ID', 'PAIS', 'CLASSE'], value_vars=list(p.columns[cols_val]), var_name='ANO', value_name='VALOR')

        # Removendo o .1 que aparece no final do ano para o valor, pois o pandas não permite colunas com o mesmo nome.
        # Então, para cada ano ele criou uma coluna com o nome do ano e outra com o nome do ano + .1
        df2['ANO'] = df2['ANO'].map(lambda x: x.replace('.1', ''))

        # Juntando os dois dataframes para contemplar em um único dataframe a quantidade e o valor.
        df = df1.join(df2.set_index(['ID', 'PAIS', 'CLASSE', 'ANO']), on=['ID', 'PAIS', 'CLASSE', 'ANO'], how='inner')

        # Convertendo os tipos para criar a tabela no SQLITE com os tipos corretos
        df['ANO'] = pd.to_numeric(df['ANO'], errors='coerce').fillna(0).astype(int)
        df['QUANTIDADE'] = pd.to_numeric(df['QUANTIDADE'], errors='coerce').fillna(0).astype(int)       
        df['VALOR'] = pd.to_numeric(df['VALOR'], errors='coerce').fillna(0).astype(float) 

        # Salvando os dados no SQLITE
        self.repo.saveDataframe(df, table_name, if_exists)

    def processarDadosExportacao(self):
        self.processarArquivoImportacao('http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv', classe='VINHOS_MESA', table_name='exportacao', if_exists='replace')
        self.processarArquivoImportacao('http://vitibrasil.cnpuv.embrapa.br/download/ExpEspumantes.csv', classe='ESPUMANTES', table_name='exportacao', if_exists='append')
        self.processarArquivoImportacao('http://vitibrasil.cnpuv.embrapa.br/download/ExpUva.csv', classe='UVAS_FRESCAS', table_name='exportacao', if_exists='append')
        self.processarArquivoImportacao('http://vitibrasil.cnpuv.embrapa.br/download/ExpSuco.csv', classe='SUCO_UVA', table_name='exportacao', if_exists='append')

    def selectProducaoPorAno(self, ano) -> List[EmbrapaProducaoDTO]:
        prods = self.repo.selectProducaoPorAno(ano)
        return prods

    def selectProcessamentoPorAno(self, ano) -> List[EmbrapaProcessamentoDTO]:
        prods = self.repo.selectProcessamentoPorAno(ano)
        return prods
    
    def selectComercializacaoPorAno(self, ano) -> List[EmbrapaComercializacaoDTO]:
        prods = self.repo.selectComercializacaoPorAno(ano)
        return prods

    def selectExportacaoPorAno(self, ano) -> List[EmbrapaExportacaoDTO]:
        prods = self.repo.selectExportacaoPorAno(ano)
        return prods
    
    def selectImportacaoPorAno(self, ano) -> List[EmbrapaImportacaoDTO]:
        prods = self.repo.selectImportacaoPorAno(ano)
        return prods