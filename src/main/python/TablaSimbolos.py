from Contexto import Contexto

class TS:
    _instance = None
    _ctx = []

    def __new__(cls):
        if TS._instance is None:
            TS._instance = object.__new__(cls)
            TS._ctx.append(Contexto())
        return (TS._instance)
    
    def getCtx(self):
        return TS._ctx
    
    # Cada vez que se ingrese en un bloque, se agrega un contexto a la lista
    def agregarContexto(self):
        TS._ctx.append(Contexto())

    # Cada vez que salimos de un bloque, se elimina el contexto de la lista
    def borrarContexto(self):
        TS._ctx.pop()

    # Agregamos un ID en el ultimo contexto registrado
    # Dentro de la lista de contextos, tomo el ultimo diccionario
    # la entrada es {nombreId, Id}
    def agregar(self, variable):
        TS._ctx[-1].agregarSimbolo(variable)

    # Para el ultimo contexto guardado, buscamos por la key, el nombre del ID
    # Si esta en el diccionario, return true, else false
    def buscarLocal(self, nombre): 
        if nombre in TS._ctx[-1].getSimbolos:
            return True
        return False
    
    # Buscamos la key en cualquiera de los contextos almacenados
    # Recorremos desde el global hacia el ultimo
    def buscar(self, nombre):
        for context in TS._ctx[::-1]:
            if nombre in context.getSimbolos():
                return True
        return False

