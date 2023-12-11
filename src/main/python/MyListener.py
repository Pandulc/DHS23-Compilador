from compiladoresListener import compiladoresListener
from compiladoresParser import compiladoresParser
from TablaSimbolos import TS
from Id import Id


class MyListener(compiladoresListener):
    tablaSimbolos = TS()

    def enterPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("Comenzando la compilacion".center(40, "*"))
        print(self.tablaSimbolos.getContextos())

    def exitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("Fin de la compilacion".center(40, "*"))
        self.tablaSimbolos.borrarContexto()

    def enterBloque(self, ctx: compiladoresParser.BloqueContext):
        self.tablaSimbolos.agregarContexto()

    def exitBloque(self, ctx: compiladoresParser.BloqueContext):
        self.tablaSimbolos.borrarContexto()

    def exitDeclaracion(self, ctx: compiladoresParser.DeclaracionContext):
        if (self.tablaSimbolos.buscarLocal(ctx.getChild(1).getText()) == False):
            tdato = str(ctx.getChild(0).getText())
            name = str(ctx.getChild(1).getText())
            nuevaVar = Id(name, tdato)
            # Si el 3er hijo en la declaracion es distinto de vacio, existe definicion
            if (str(ctx.getChild(2).getText()) != ''):
                nuevaVar.setInicializado()
        else:
            print("Variable " + ctx.getChild(1).getText() +
                  " existente en el contexto")
            return
        self.tablaSimbolos.agregar(nuevaVar)
