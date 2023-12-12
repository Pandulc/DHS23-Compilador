class Contexto:

    def __init__(self):
        self._simbolos = dict()

    def agregarSimbolo(self, variable):
        self._simbolos[variable.nombre] = variable

    def getSimbolos(self) -> dict:
        return self._simbolos
