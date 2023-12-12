from compiladoresListener import compiladoresListener
from compiladoresParser import compiladoresParser
from TablaSimbolos import TS
from Id import *
import copy


class MyListener(compiladoresListener):
    tablaSimbolos = TS()
    listTdato = []
    listArgs = []

    def enterPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("Comenzando la compilacion".center(40, "*") + '\n')

    def exitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print('\n' + "Fin de la compilacion".center(40, "*"))
        self.tablaSimbolos.borrarContexto()

    def enterBloque(self, ctx: compiladoresParser.BloqueContext):
        self.tablaSimbolos.agregarContexto()

    def exitBloque(self, ctx: compiladoresParser.BloqueContext):
        self.tablaSimbolos.borrarContexto()

    def exitDeclaracion(self, ctx: compiladoresParser.DeclaracionContext):
        if self.tablaSimbolos.buscarLocal(ctx.getChild(1).getText()) == False:
            tdato = str(ctx.getChild(0).getText())
            # salvo el tipo de dato en caso de haber una lista de variables
            self.listTdato.append(tdato)
            name = str(ctx.getChild(1).getText())
            nuevaVar = Variable(name, tdato)
            # Si el 3er hijo en la declaracion es distinto de vacio, existe definicion
            if (str(ctx.getChild(2).getText()) != ''):
                nuevaVar.setInicializado()
        else:
            print("Variable " + ctx.getChild(1).getText() +
                  " existente en el contexto")
            return
        self.tablaSimbolos.agregar(nuevaVar)
        print('Nuevo simbolo: ' + nuevaVar.nombre + ' agregado')

        self.listTdato.pop()

        return

    def exitLista_var(self, ctx: compiladoresParser.Lista_varContext):
        if ctx.getChildCount() != 0:
            if self.tablaSimbolos.buscarLocal(ctx.getChild(1).getText()) == False:
                # como el Listener recorre el arbol de abajo hacia arriba, obtenemos el tipo
                # de dato subiendo el contexto hacia la declaracion
                if len(self.listTdato) == 0:
                    auxCtx = ctx
                    while (auxCtx.parentCtx.getChild(0).getText() == ','):
                        auxCtx = auxCtx.parentCtx
                    self.listTdato.append(
                        auxCtx.parentCtx.getChild(0).getText())

                tdato = self.listTdato.pop()
                self.listTdato.append(tdato)
                name = str(ctx.getChild(1).getText())
                nuevaVar = Variable(name, tdato)
                # Si el 3er hijo en la declaracion es distinto de vacio, existe definicion
                if (str(ctx.getChild(2).getText()) != ''):
                    nuevaVar.setInicializado()
            else:
                print("Variable " + ctx.getChild(1).getText() +
                      " existente en el contexto")
                return
            self.tablaSimbolos.agregar(nuevaVar)
            print('Nuevo simbolo: ' + nuevaVar.nombre + ' agregado')

            self.listTdato.pop()

        return

    def exitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        contexto = self.tablaSimbolos.buscar(ctx.getChild(0).getText())
        if contexto == None:
            print('LA VARIABLE NO ESTA DEFINIDA, NO SE REALIZO LA ASIGNACION')
            return
        for var in contexto.getSimbolos():
            if var == ctx.getChild(0).getText():
                varActualizada = Variable(
                    contexto.getSimbolos()[var].nombre, contexto.getSimbolos()[var].tdato, True)
                self.tablaSimbolos.actualizar(varActualizada)
                print('Variable ' + varActualizada.nombre + ' actualizada')

    def exitCall_funcion(self, ctx: compiladoresParser.Call_funcionContext):
        contexto = self.tablaSimbolos.buscar(ctx.getChild(0).getText())

        if contexto == False:
            print('FUNCION INEXISTENTE')
            return

        funcionVar = Funcion('', '', [])
        for var in contexto.getSimbolos().values():
            if var.nombre == ctx.getChild(0).getText():
                funcionVar = var
                break

        self.exitSend_args(ctx.getChild(2))

        if len(funcionVar.args) != len(self.listArgs):
            print('Faltan parametros en la llamada de funcion')
            return

        for var1, var2 in zip(funcionVar.args, self.listArgs):
            if var1.tdato != var2.tdato:
                print('Error: el parametro ' + var2 +
                      ' no es del tipo esperado')
                return

    def exitProto_funcion(self, ctx: compiladoresParser.Proto_funcionContext):
        self.listArgs.clear()
        if self.tablaSimbolos.buscar(ctx.getChild(1).getText()) == False:
            tdato = ctx.getChild(0).getText()
            nombre = ctx.getChild(1).getText()
            self.exitArgs(ctx.getChild(3))
            listaArgs = copy.deepcopy(self.listArgs)
            nuevaVar = Funcion(nombre, tdato, listaArgs)
            self.tablaSimbolos.agregar(nuevaVar)
            print('Nuevo simbolo ' + nuevaVar.nombre + ' agregado')
        else:
            print('SIMBOLO YA DEFINIDO')

    def exitFuncion(self, ctx: compiladoresParser.FuncionContext):
        self.listArgs.clear()

        tdato = ctx.getChild(0).getText()
        nombre = ctx.getChild(1).getText()
        self.exitArgs(ctx.getChild(3))
        listaArgs = copy.deepcopy(self.listArgs)
        funcionVar = Funcion(nombre, tdato, listaArgs)
        funcionVar.setAccedido()

        contexto = self.tablaSimbolos.buscar(nombre)

        # Si no existio prototipo de la funcion, se agrega a la tabla de simbolos
        if contexto == False:
            self.tablaSimbolos.agregar(funcionVar)
            print('Nuevo simbolo ' + funcionVar.nombre + ' agregado')
            return

        # Si existe prototipo, verifico que la implementacion se corresponda
        for var in contexto.getSimbolos().values():
            if var.nombre == funcionVar.nombre:
                if var.tdato == funcionVar.tdato:
                    for arg1, arg2 in zip(var.args, funcionVar.args):
                        # En caso que el prototipo tenga nombre en el argumento
                        if arg1.nombre != '':
                            if arg1.nombre == arg2.nombre:
                                if arg1.tdato == arg2.tdato:
                                    pass
                                else:
                                    print(
                                        'LA IMPLEMENTACION DE ' + funcionVar.nombre + ' NO SE CORRESPONDE CON EL PROTOTIPO')
                                    return
                            else:
                                print(
                                    'LA IMPLEMENTACION DE ' + funcionVar.nombre + ' NO SE CORRESPONDE CON EL PROTOTIPO')
                                return
                    print('La implementacion de ' + funcionVar.nombre +
                          ' se corresponde con su prototipo')
                    return

        print(
            'LA IMPLEMENTACION DE ' + funcionVar.nombre + ' NO SE CORRESPONDE CON EL PROTOTIPO')
        return

    def exitArgs(self, ctx: compiladoresParser.ArgsContext):
        if ctx.getChildCount() != 0:
            nombre = ctx.getChild(1).getText()
            tdato = ctx.getChild(0).getText()
            nuevoArg = Variable(nombre, tdato)
            self.listArgs.append(nuevoArg)
            self.exitLista_args(ctx.getChild(2))

    def exitLista_args(self, ctx: compiladoresParser.Lista_argsContext):
        if ctx.getChildCount() != 0:
            nombre = ctx.getChild(2).getText()
            tdato = ctx.getChild(1).getText()
            nuevoArg = Variable(nombre, tdato)
            self.listArgs.append(nuevoArg)
            self.exitLista_args(ctx.getChild(3))

    def exitSend_args(self, ctx: compiladoresParser.Send_argsContext):
        self.listArgs.clear()
        if ctx.getChildCount() == 0:
            return

        nombre = str()
        if ctx.getChild(0).getChild(0).getChild(0).getChildCount == 2:
            nombre = ctx.getChild(0).getChild(
                0).getChild(0).getChild(1).getText()
        elif ctx.getChild(0).getChild(0).getChild(0).getChild(0).getChildCount() == 0:
            nombre = ctx.getChild(0).getChild(
                0).getChild(0).getChild(0).getText()

        contexto = self.tablaSimbolos.buscar(nombre)

        if contexto == False:
            print('PARAMETRO ' + nombre + ' NO DEFINIDO')
            return

        for var in contexto.getSimbolos().values():
            if var.nombre == nombre:
                self.listArgs.append(var)

        self.exitLista_send_args(ctx.getChild(1))

        return

    def exitLista_send_args(self, ctx: compiladoresParser.Lista_send_argsContext):
        if ctx.getChildCount() == 0:
            return

        nombre = str()
        if ctx.getChild(1).getChild(0).getChild(0).getChildCount == 2:
            nombre = ctx.getChild(1).getChild(
                0).getChild(0).getChild(1).getText()
        elif ctx.getChild(1).getChild(0).getChild(0).getChild(0).getChildCount() == 0:
            nombre = ctx.getChild(1).getChild(
                0).getChild(0).getChild(0).getText()

        contexto = self.tablaSimbolos.buscar(nombre)

        if contexto == False:
            print('PARAMETRO ' + nombre + ' NO DEFINIDO')
            return

        for var in contexto.getSimbolos().values():
            if var.nombre == nombre:
                self.listArgs.append(var)
                break

        if ctx.getChild(2).getChildCount() != 0:
            self.exitLista_send_args(ctx.getChild(1))

        return
