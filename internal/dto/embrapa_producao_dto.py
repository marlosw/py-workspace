from pkg.dto.base_dto import BaseDTO


class EmbrapaProducaoDTO(BaseDTO):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get('id')
        self.key = kwargs.get('key')
        self.tipo = kwargs.get('tipo')
        self.ano = kwargs.get('ano')
        self.produto = kwargs.get('produto')
        self.reg = kwargs.get('reg')
        self.valor = kwargs.get('valor')

class EmbrapaProcessamentoDTO(BaseDTO):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get('id')
        self.key = kwargs.get('key')
        self.tipo = kwargs.get('tipo')
        self.reg = kwargs.get('reg')
        self.classe = kwargs.get('classe')
        self.control = kwargs.get('control')
        self.cultivar = kwargs.get('cultivar')
        self.ano = kwargs.get('ano')
        self.valor = kwargs.get('valor')
        
