
from pkg.entity.base_entity import BaseEntity


class EmbrapaProducao(BaseEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get('id')
        self.key = kwargs.get('key')
        self.tipo = kwargs.get('tipo')
        self.ano = kwargs.get('ano')
        self.produto = kwargs.get('produto')
        self.reg = kwargs.get('reg')
        self.valor = kwargs.get('valor')
        