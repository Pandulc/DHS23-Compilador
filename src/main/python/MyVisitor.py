from compiladoresVisitor import compiladoresVisitor
from compiladoresParser import compiladoresParser
from Util.ManejoArchivos import *

class MyVisitor(compiladoresVisitor):
    def visitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("Visitando arbol")
        return self.visitDeclaracion(compiladoresParser.DeclaracionContext)
    
    def visitDeclaracion(self, ctx: compiladoresParser.DeclaracionContext):
        print(ctx.getChild(0).getText())
    
    
if __name__ == "__main__":
    pass