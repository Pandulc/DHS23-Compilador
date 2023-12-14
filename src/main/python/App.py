import sys
from antlr4 import *
from compiladoresLexer import compiladoresLexer
from compiladoresParser import compiladoresParser
from MyListener import MyListener
from MyVisitor import MyVisitor
from Optimizacion import Optimizador


def main(argv):
    archivo = "input/decl.c"
    if len(argv) > 1:
        archivo = argv[1]
    input = FileStream(archivo)
    lexer = compiladoresLexer(input)
    stream = CommonTokenStream(lexer)
    parser = compiladoresParser(stream)
    listener = MyListener()
    parser.addParseListener(listener)
    tree = parser.programa()
    # En caso de haber existido un error, la ejecucion se detendra y no
    # se construira codigo intermedio
    if listener.error == 0:
        visitor = MyVisitor()
        visitor.visit(tree)
        optimizador = Optimizador()
        optimizador.optimizarCodigoIntermedio()
    else:
        print('Ha ocurrido un error, revisar el archivo ./output/Errores&Warnings.txt. No se genero codigo intermedio')


if __name__ == '__main__':
    main(sys.argv)
