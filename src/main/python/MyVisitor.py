from compiladoresVisitor import compiladoresVisitor
from compiladoresParser import compiladoresParser
from Util.Temporales import *
from Util.Etiquetas import *


class MyVisitor(compiladoresVisitor):

    _temporales = []
    _etiquetas = []
    generador_temporales = Temporales()
    generador_etiquetas = Etiquetas()

    def visitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("Visitando arbol")
        self.f = open("./output/CodigoIntermedio.txt", "w")

        self.visitChildren(ctx)

        self.f.close()

    def visitDeclaracion(self, ctx: compiladoresParser.DeclaracionContext):

        if ctx.getChild(2).getChildCount() != 0:
            self.visitDefinicion(ctx.getChild(2))
            self.f.write(ctx.getChild(1).getText() +
                         " = " + self._temporales.pop() + '\n')
        return

    def visitDefinicion(self, ctx: compiladoresParser.DefinicionContext):
        self.visitOplo(ctx.getChild(1))
        return

    def visitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        self.visitOplo(ctx.getChild(2))

        self.f.write(ctx.getChild(0).getText() +
                     " = " + self._temporales.pop() + '\n')

    def visitIf_stmt(self, ctx: compiladoresParser.If_stmtContext):
        self.visitOplo(ctx.getChild(2))

        if (ctx.getChild(5) == None):
            etiqueta = self.generador_etiquetas.next_etiqueta()
            self.f.write('ifn ' + self._temporales.pop() +
                         ' jmp' + etiqueta + '\n')
            self.visitBloque(ctx.getChild(4))
            self.f.write('label ' + etiqueta + '\n')
        else:
            etiqueta1 = self.generador_etiquetas.next_etiqueta()
            etiqueta2 = self.generador_etiquetas.next_etiqueta()
            self.f.write('ifn ' + self._temporales.pop() +
                         ' jmp ' + etiqueta1 + '\n')
            self.visitBloque(ctx.getChild(4))
            self.f.write('jmp ' + etiqueta2 + '\n')
            self.f.write('label ' + etiqueta1 + '\n')
            self.visitElse_stmt(ctx.getChild(5))
            self.f.write('label ' + etiqueta2 + '\n')

        return

    def visitElse_stmt(self, ctx: compiladoresParser.If_stmtContext):
        self.visitBloque(ctx.getChild(1))
        return

    def visitFor_stmt(self, ctx: compiladoresParser.For_stmtContext):
        etiqueta1 = self.generador_etiquetas.next_etiqueta()
        self.visitAsignacion(ctx.getChild(2))
        self.f.write('label ' + etiqueta1 + '\n')

        etiqueta2 = self.generador_etiquetas.next_etiqueta()
        self.visitOplo(ctx.getChild(4))
        self.f.write('ifn ' + self._temporales.pop() +
                     ' jmp' + etiqueta2 + '\n')
        self.visitInstrucciones(ctx.getChild(8))
        self.visitAsignacion(ctx.getChild(6))
        self.f.write('jmp ' + etiqueta1 + '\n')
        self.f.write('label ' + etiqueta2 + '\n')

    def visitWhile_stmt(self, ctx: compiladoresParser.While_stmtContext):
        etiqueta1 = self.generador_etiquetas.next_etiqueta()
        self.f.write('label ' + etiqueta1 + '\n')

        etiqueta2 = self.generador_etiquetas.next_etiqueta()
        self.visitOplo(ctx.getChild(2))
        self.f.write('ifn ' + self._temporales.pop() +
                     ' jmp' + etiqueta2 + '\n')
        self.visitInstrucciones(ctx.getChild(4))
        self.f.write('jmp ' + etiqueta1 + '\n')
        self.f.write('label ' + etiqueta2 + '\n')

    def visitOplo(self, ctx: compiladoresParser.OploContext):
        return self.visitLogic_expresion(ctx.getChild(0))

    def visitLogic_expresion(self, ctx: compiladoresParser.Logic_expresionContext):

        self.visitLogic_termino(ctx.getChild(0))

        if ctx.getChild(1).getChildCount() != 0:
            temporal = self.generador_temporales.next_temporal()
            self.f.write(temporal + ' = ' + self._temporales.pop() + ' ' + ctx.getChild(
                1).getChild(0).getText() + ' ' + self.visitLogic_expr(ctx.getChild(1)) + '\n')
            self._temporales.append(temporal)

        return

    def visitLogic_expr(self, ctx: compiladoresParser.Logic_exprContext):
        self.visitLogic_termino(ctx.getChild(1))

        if ctx.getChild(2).getChildCount() != 0:
            temporal = self.generador_temporales.next_temporal()

            self.f.write(temporal + ' = ' + self._temporales.pop() + ' ' + ctx.getChild(
                2).getChild(0).getText() + ' ' + self.visitLogic_expr(ctx.getChild(2)) + '\n')

            self._temporales.append(temporal)

        return self._temporales.pop()

    def visitLogic_termino(self, ctx: compiladoresParser.Logic_terminoContext):
        self.visitLogic_factor(ctx.getChild(0))

        if ctx.getChild(1).getChildCount() != 0:

            temporal = self.generador_temporales.next_temporal()
            self.f.write(temporal + ' = ' + self._temporales.pop() + ' ' + ctx.getChild(
                1).getChild(0).getText() + ' ' + self.visitLogic_term(ctx.getChild(1)) + '\n')
            self._temporales.append(temporal)

        return

    def visitLogic_term(self, ctx: compiladoresParser.Logic_termContext):

        self.visitLogic_factor(ctx.getChild(1))

        if ctx.getChild(2).getChildCount() != 0:
            temporal = self.generador_temporales.next_temporal()

            self.f.write(temporal + ' = ' + self._temporales.pop() + ' ' + ctx.getChild(
                2).getChild(0).getText() + ' ' + self.visitLogic_term(ctx.getChild(2)) + '\n')

            self._temporales.append(temporal)

        return self._temporales.pop()

    def visitLogic_factor(self, ctx: compiladoresParser.Logic_factorContext):
        if ctx.getChildCount() == 1:
            if ctx.getChild(0).getChildCount() == 1:
                self.visitOpar(ctx.getChild(0))
                return
            if ctx.getChild(0).getChildCount() == 3:
                self.visitComp(ctx.getChild(0))
                return
        else:
            self.visitLogic_expresion(ctx.getChild(1))

    def visitComp(self, ctx: compiladoresParser.CompContext):
        self.visitOpar(ctx.getChild(2))
        self.visitOpar(ctx.getChild(0))

        temporal = self.generador_temporales.next_temporal()

        self.f.write(temporal + " = " + self._temporales.pop() + " " +
                     ctx.getChild(1).getText() + " " + self._temporales.pop() + '\n')

        self._temporales.append(temporal)

    def visitOpar(self, ctx: compiladoresParser.OparContext):
        self.visitExpresion(ctx.getChild(0))
        return

    def visitExpresion(self, ctx: compiladoresParser.ExpresionContext):
        self.visitTermino(ctx.getChild(0))

        if ctx.getChild(1).getChildCount() != 0:
            temporal = self.generador_temporales.next_temporal()

            self.f.write(temporal + " = " + self._temporales.pop() + " " +
                         ctx.getChild(1).getChild(0).getText() + " " + self.visitExp(ctx.getChild(1)) + "\n")
            self._temporales.append(temporal)

        return

    def visitExp(self, ctx: compiladoresParser.ExpContext):
        self.visitTermino(ctx.getChild(1))

        if ctx.getChild(2).getChildCount() != 0:
            temporal = self.generador_temporales.next_temporal()

            self.f.write(temporal + " = " + self._temporales.pop() + " " +
                         ctx.getChild(2).getChild(0).getText() + " " + self.visitExp(ctx.getChild(2)) + "\n")
            self._temporales.append(temporal)

        return self._temporales.pop()

    def visitTermino(self, ctx: compiladoresParser.TerminoContext):
        self.visitFactor(ctx.getChild(0))

        if ctx.getChild(1).getChildCount() != 0:
            temporal = self.generador_temporales.next_temporal()

            self.f.write(temporal + ' = ' + self._temporales.pop() + ' ' + ctx.getChild(
                1).getChild(0).getText() + ' ' + self.visitTerm(ctx.getChild(1)) + '\n')
            self._temporales.append(temporal)

        return

    def visitTerm(self, ctx: compiladoresParser.TermContext):
        self.visitFactor(ctx.getChild(1))

        if ctx.getChild(2).getChildCount() != 0:
            temporal = self.generador_temporales.next_temporal()

            self.f.write(temporal + ' = ' + self._temporales.pop() + ' ' + ctx.getChild(
                2).getChild(0).getText() + ' ' + self.visitTerm(ctx.getChild(2)) + '\n')
            self._temporales.append(temporal)

        return self._temporales.pop()

    def visitFactor(self, ctx: compiladoresParser.FactorContext):

        if ctx.getChildCount() == 3:
            self.visitExpresion(ctx.getChild(1))
            return
        if ctx.getChildCount() == 2:
            temporal = self.generador_temporales.next_temporal()
            self.f.write(temporal + ' = ' +
                         ctx.getChild(0).getText() + ctx.getChild(1).getText() + '\n')
            self._temporales.append(temporal)
            return
        if ctx.getChildCount() == 1:
            temporal = self.generador_temporales.next_temporal()
            self.f.write(temporal + ' = ' + ctx.getChild(0).getText() + '\n')
            self._temporales.append(temporal)
            return


if __name__ == "__main__":
    pass
