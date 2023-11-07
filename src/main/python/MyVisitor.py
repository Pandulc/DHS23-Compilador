from compiladoresVisitor import compiladoresVisitor
from compiladoresParser import compiladoresParser
from Util.ManejoArchivos import *
from Util.Temporales import *


class MyVisitor(compiladoresVisitor):

    _temporales = []
    generador_temporales = Temporales()

    def visitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("Visitando arbol")
        self.f = open("./output/CodigoIntermedio.txt", "w")

        self.visitChildren(ctx)
        self.f.close()

    def visitDeclaracion(self, ctx: compiladoresParser.DeclaracionContext):

        self.visitDefinicion(ctx.getChild(2))

        self.f.write(ctx.getChild(1).getText() +
                     " = " + self._temporales.pop())

      # Visit a parse tree produced by compiladoresParser#definicion.
    def visitDefinicion(self, ctx: compiladoresParser.DefinicionContext):
        self.visitOpar(ctx.getChild(1))
        return

    def visitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        self.visitOpar(ctx.getChild(2))

        self.f.write(ctx.getChild(0).getText() +
                     " = " + self._temporales.pop())

    def visitOpar(self, ctx: compiladoresParser.OparContext):
        self.visitExpresion(ctx.getChild(0))
        return

    def visitExpresion(self, ctx: compiladoresParser.ExpresionContext):
        temporal = self.generador_temporales.next_temporal()
        self._temporales.append(temporal)
        self.f.write(temporal + " = " + self.visitTermino(ctx.getChild(0)) + " " +
                     ctx.getChild(1).getChild(0).getText() + " " + self.visitExp(ctx.getChild(1)) + "\n")

        return

    def visitExp(self, ctx: compiladoresParser.ExpContext):
        if ctx.getChild(2).getChildCount() == 0:
            return self.visitTermino(ctx.getChild(1))

        temporal = self.generador_temporales.next_temporal()
        self._temporales.append(temporal)
        self.f.write(temporal + " = " + self.visitTermino(ctx.getChild(1)) + " " +
                     ctx.getChild(2).getChild(0).getText() + " " + self.visitExp(ctx.getChild(2)) + "\n")

        return self._temporales.pop()

    def visitTermino(self, ctx: compiladoresParser.TerminoContext):
        temporal = self.generador_temporales.next_temporal()
        self._temporales.append(temporal)

        if ctx.getChild(0).getChildCount() == 3:
            self.visitExpresion(ctx.getChild(0).getChild(1))
            self.f.write(temporal + " = " + self._temporales.pop() + "\n")

        if ctx.getChild(0).getChildCount() == 2:
            self.f.write(temporal + " = " + ctx.getChild(0).getChild(
                0).getText() + ctx.getChild(0).getChild(1).getText() + "\n")

        if ctx.getChild(0).getChildCount() == 1:
            self.f.write(temporal + " = " +
                         ctx.getChild(0).getChild(0).getText() + "\n")

        return self.visitTerm(ctx.getChild(1))

    def visitTerm(self, ctx: compiladoresParser.TermContext):
        if ctx.getChildCount() == 0:
            return self._temporales.pop()

        temporal = self.generador_temporales.next_temporal()

        self.f.write(temporal + " = " + self._temporales.pop() + " " + ctx.getChild(0).getText() + " " +
                     self.visitFactor(ctx.getChild(1)) + "\n")

        self._temporales.append(temporal)
        return self.visitTerm(ctx.getChild(2))

    def visitFactor(self, ctx: compiladoresParser.FactorContext):
        if ctx.getChildCount() == 3:
            self.visitExpresion(ctx.getChild(1))
        if ctx.getChildCount() == 2:
            return ctx.getChild(0).getText() + ctx.getChild(1).getText()
        else:
            return ctx.getChild(0).getText()


if __name__ == "__main__":
    pass
