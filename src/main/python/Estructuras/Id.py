from abc import ABC


class Id(ABC):
    def __init__(self, nombre, tdato, inicializado=False, accedido=False):
        self.nombre = nombre
        self.tdato = tdato
        self.inicializado = inicializado
        self.accedido = accedido
    
    def setInicializado(self):
        self.inicializado = True

    def setAccedido(self):
        self.accedido = True

class Variable(Id):
    pass

class Funcion(Id):
    def __init__(self, nombre, tdato, args, inicializado=False, accedido=False):
        super().__init__(nombre, tdato, inicializado, accedido)
        self.args = args
