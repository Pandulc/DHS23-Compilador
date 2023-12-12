from compiladoresListener import compiladoresListener
from compiladoresParser import compiladoresParser
from Estructuras.TablaSimbolos import TS
from Estructuras.Id import *
import copy


class MyListener(compiladoresListener):
    tablaSimbolos = TS()
    listTdato = []
    listArgs = []
    isFuncion = 0

    def enterPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("Comenzando la compilacion".center(40, "*") + '\n')

    def exitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print('\n' + "Fin de la compilacion".center(40, "*"))
        self.tablaSimbolos.borrarContexto()

    def enterBloque(self, ctx: compiladoresParser.BloqueContext):
        self.tablaSimbolos.agregarContexto()

        # Verificacion de padre, que no sea if, for o while
        if ctx.parentCtx.getChild(0).getText() != 'int':
            if ctx.parentCtx.getChild(0).getText() != 'double':
                return

        # Proceso la lista de parametros de la funcion
        self.exitArgs(ctx.parentCtx.getChild(3))
        listaArgs = copy.deepcopy(self.listArgs)

        # Los guardo dentro de la tabla de simbolos, en el contexto de la funcion
        for var in listaArgs:
            self.tablaSimbolos.agregar(var)

    def exitBloque(self, ctx: compiladoresParser.BloqueContext):
        self.tablaSimbolos.borrarContexto()

    def exitDeclaracion(self, ctx: compiladoresParser.DeclaracionContext):
        if self.tablaSimbolos.buscarLocal(ctx.getChild(1).getText()) == False:
            tdato = str(ctx.getChild(0).getText())
            # salvo el tipo de dato en caso de haber una lista de variables
            self.listTdato.append(tdato)
            name = str(ctx.getChild(1).getText())
            nuevaVar = Variable(name, tdato)

            # Verificamos llamado a funcion
            if not ctx.getChild(2).getChild(1).getChild(0).getChild(0).getChild(0).getChild(0).getChild(0).getChild(0).getChild(0).getChild(0).getChildCount() == 4:
                # Si el 3er hijo en la declaracion es distinto de vacio, existe definicion
                if (str(ctx.getChild(2).getText()) != ''):
                    nuevaVar.setInicializado()
            else:
                self.tablaSimbolos.agregar(nuevaVar)
                print('Nuevo simbolo: ' + nuevaVar.nombre + ' agregado')
                self.listTdato.append(nuevaVar.nombre)
                self.listTdato.append(nuevaVar.tdato)
                self.isFuncion = 1
                self.exitCall_funcion(ctx.getChild(2).getChild(1).getChild(0).getChild(
                    0).getChild(0).getChild(0).getChild(0).getChild(0).getChild(0).getChild(0))
                return
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

        for var in contexto.getSimbolos().values():
            if var.nombre == ctx.getChild(0).getText():
                # Verifico que no sea llamado a funcion
                if not ctx.getChild(2).getChild(0).getChild(0).getChild(0).getChild(0).getChild(0).getChild(0).getChild(0).getChild(0).getChildCount() == 4:
                    varActualizada = Variable(
                        var.nombre, var.tdato, True)
                    self.tablaSimbolos.actualizar(varActualizada)
                    print('Variable ' + varActualizada.nombre + ' actualizada')
                # En caso de ser llamado a funcion, se actualiza cuando se comprueba que los tipos de datos son iguales (variable y retorno)
                else:
                    self.listTdato.append(var.nombre)
                    self.listTdato.append(var.tdato)
                    self.isFuncion = 1
                    self.exitCall_funcion(ctx.getChild(2).getChild(0).getChild(0).getChild(
                        0).getChild(0).getChild(0).getChild(0).getChild(0).getChild(0))

    def exitCall_funcion(self, ctx: compiladoresParser.Call_funcionContext):
        contexto = self.tablaSimbolos.buscar(ctx.getChild(0).getText())

        # Actualizacion de variable

        if self.isFuncion == 1:

            for var in contexto.getSimbolos().values():
                if var.nombre == ctx.getChild(0).getText():
                    break

            tdato = self.listTdato.pop()
            nombre = self.listTdato.pop()

            if var.tdato == tdato:
                print('La asignacion de: ' + nombre
                      + ' es posible')
                varActualizada = Variable(nombre, tdato, True)
                self.tablaSimbolos.actualizar(varActualizada)
            else:
                print('La asignacion de: ' +
                      nombre + ' no es posible: Error de tipo de dato')

            self.isFuncion = 0
            return

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
            print('Nuevo simbolo: ' + nuevaVar.nombre + ' agregado')
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
            print('Nuevo simbolo: ' + funcionVar.nombre + ' agregado')
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

    def exitRetornar(self, ctx: compiladoresParser.RetornarContext):

        funcionCtx = ctx.parentCtx
        while (True):
            if funcionCtx.getChild(0).getText() != 'int':
                if funcionCtx.getChild(0).getText() != 'double':
                    funcionCtx = funcionCtx.parentCtx
                else:
                    break
            else:
                break

        nombre = ctx.getChild(1).getChild(0).getChild(0).getChild(0).getChild(
            0).getChild(0).getChild(0).getChild(0).getChild(0).getText()

        if not nombre.replace('.', '', 1).isdigit():
            contexto = self.tablaSimbolos.buscar(nombre)

            if contexto == False:
                print('SIMBOLO ' + nombre + ' NO DEFINIDO')
                return

            for var in contexto.getSimbolos().values():
                if var.nombre == nombre:
                    break
        else:
            if '.' in nombre:
                var = Variable(nombre, 'double')
            else:
                var = Variable(nombre, 'int')

        if var.tdato == funcionCtx.getChild(0).getText():
            print('El tipo de dato retornado por ' +
                  funcionCtx.getChild(1).getText() + ' es correcto')

        else:
            print('El tipo de dato retornado por ' +
                  funcionCtx.getChild(1).getText() + ' no es correcto')

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

        if not nombre.replace('.', '', 1).isdigit():

            contexto = self.tablaSimbolos.buscar(nombre)

            if contexto == False:
                print('PARAMETRO ' + nombre + ' NO DEFINIDO')
                return

            for var in contexto.getSimbolos().values():
                if var.nombre == nombre:
                    self.listArgs.append(var)
        else:
            if '.' in nombre:
                var = Variable(nombre, 'double')
                self.listArgs.append(var)
            else:
                var = Variable(nombre, 'int')
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

        # Se verifica que no sea un numero
        if not nombre.replace('.', '', 1).isdigit():

            contexto = self.tablaSimbolos.buscar(nombre)

            if contexto == False:
                print('PARAMETRO ' + nombre + ' NO DEFINIDO')
                return

            for var in contexto.getSimbolos().values():
                if var.nombre == nombre:
                    self.listArgs.append(var)
                    break

        # En caso de ser un numero, verificamos si es entero o decimal
        else:
            if '.' in nombre:
                var = Variable(nombre, 'double')
                self.listArgs.append(var)
            else:
                var = Variable(nombre, 'int')
                self.listArgs.append(var)

        if ctx.getChild(2).getChildCount() != 0:
            self.exitLista_send_args(ctx.getChild(1))

        return
