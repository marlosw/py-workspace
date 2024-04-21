from pkg.dto.base_dto import BaseDTO


class EmbrapaProducaoDTO():
    def __init__(self, id, key, tipo, reg, produto, ano, valor):
        self.id = id
        self.key = key
        self.tipo = tipo
        self.reg = reg
        self.produto = produto
        self.ano = ano
        self.valor = valor
        
class EmbrapaProcessamentoDTO():
    def __init__(self, id, key, tipo, reg, classe, control, cultivar, ano, valor):
        self.id = id
        self.key = key
        self.tipo = tipo
        self.reg = reg
        self.classe = classe
        self.control = control
        self.cultivar = cultivar
        self.ano = ano
        self.valor = valor


class EmbrapaComercializacaoDTO():
    def __init__(self, id, key, tipo, reg, control, cultivar, ano, quantidade): 
        self.id = id
        self.key = key  
        self.tipo = tipo     
        self.reg = reg      
        self.control = control
        self.cultivar = cultivar  
        self.ano = ano      
        self.quantidade = quantidade    

class EmbrapaImportacaoDTO():
    def __init__(self, id, pais, classe, ano, quantidade, valor):
        self.id = id
        self.pais = pais
        self.classe = classe
        self.ano = ano
        self.valor = quantidade
        self.valor = valor
    
class EmbrapaExportacaoDTO():
    def __init__(self, id, pais, classe, ano, quantidade, valor):
        self.id = id
        self.pais = pais
        self.classe = classe
        self.ano = ano
        self.valor = quantidade
        self.valor = valor
