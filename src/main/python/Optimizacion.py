import re


class Optimizador:

    variables = dict()
    reemplazos = dict()
    src = open("./output/CodigoIntermedio.txt", "r")
    dest = open("./output/CodigoIntermedioOptimizado.txt", "w")

    def optimizarCodigoIntermedio(self):
        print('Comenzando optimizacion'.center(40, '*'))
        self.separarVariables()
        self.reemplazar()

    def separarVariables(self):
        self.src.seek(0)
        for linea in self.src:
            if '=' in linea:
                lista = linea.split(' =')
                variable = lista[0]
                igualacion = lista[1].replace('\n', '')

                self.variables[variable] = igualacion

        print('Todas las variables han sido obtenidas')

    def reemplazar(self):

        self.src.seek(0)
        for linea in self.src:

            if linea.startswith('label'):
                self.dest.write(linea)

            if linea.startswith('jmp'):
                self.dest.write(linea)

            if linea.startswith('pop'):
                self.dest.write(linea)

            if linea.startswith('push'):
                bandera = 0
                nuevaLinea = str()
                miembros = linea.replace('\n', '').split('push ')

                for key in self.variables:
                    if re.match(r't\d+', key):
                        if key in linea:
                            for miembro in miembros:
                                if key == miembro:
                                    nuevaLinea = linea.replace(
                                        key, self.variables[key])
                                    bandera = 1

                if bandera == 1:
                    for key in self.reemplazos:
                        if key in nuevaLinea:
                            nuevaLinea = nuevaLinea.replace(
                                key, self.variables[key])
                    self.dest.write(nuevaLinea)
                else:
                    self.dest.write(linea)

            if '=' in linea:
                miembros = linea.split(' = ')
                miembrosDerecha = miembros[1].replace('\n', '').split()
                # Miembro izquierdo es una variable
                if not re.match(r't\d+', miembros[0]):
                    nuevoMiembro = str()

                    for key in self.variables:
                        # Si la key no es exactamente igual al miembro derecho, pero esta en el, entonces se procesa
                        if key in miembros[1]:
                            # Se recorre todo lo que haya en el miembro derecho de la igualacion
                            for miembro in miembrosDerecha:
                                # Si la key coincide con el submiembro del miembro derecho, lo reemplaza
                                if key == miembro:
                                    index = miembrosDerecha.index(miembro)
                                    miembrosDerecha[index] = self.variables[key]
                            # Se unifican todos los submiembros del miembro derecho
                            nuevoMiembro = ' '.join(miembrosDerecha)
                            miembros[1] = nuevoMiembro

                    # Si el miembro derecho coincide con una operacion, esta se resuelve y se escribira el resultado
                    if re.match(r'^[0-9+\-*/%(). ]+$', miembros[1]):
                        miembros[1] = self.calcular(miembros[1])

                    # Reconstruimos la linea
                    nuevaLinea = str(miembros[0] + ' = ' + miembros[1] + '\n')

                    # Si el miembro derecho esta en variables, quiere decir que es una igualacion entre 2 variables, es decir
                    # una repeticion, por lo que es ignorada
                    if not miembros[1] in self.variables:
                        for key in self.reemplazos:
                            if key in miembros[1]:
                                nuevaLinea = nuevaLinea.replace(
                                    key, self.variables[key])
                        self.dest.write(nuevaLinea)
                    else:
                        self.reemplazos[miembros[0]] = miembros[1]

                    # Actualizamos el valor de la variable en el miembro izquierdo
                    if miembros[0] in self.variables:
                        if miembros[1] in self.variables:
                            for key in self.reemplazos:
                                if key == miembros[1]:
                                    miembros[1] = self.reemplazos[key]
                        self.variables[miembros[0]] = miembros[1]

                # Miembro izquierdo es un temporal
                else:
                    nuevoMiembro = str()

                    for key in self.variables:

                        if key in miembros[1]:
                            for miembro in miembrosDerecha:
                                if re.match(r't\d+', miembro):
                                    if key == miembro:
                                        index = miembrosDerecha.index(miembro)
                                        miembrosDerecha[index] = self.variables[key]

                    nuevoMiembro = ' '.join(miembrosDerecha)
                    if nuevoMiembro != '':
                        miembros[1] = nuevoMiembro

                    if re.match(r'^[0-9+\-*/%(). ]+$', miembros[1]):
                        miembros[1] = self.calcular(miembros[1])

                    self.variables[miembros[0]
                                   ] = miembros[1].replace('\n', '')

    def calcular(self, linea) -> str:
        cadena = linea.replace('push ', '')
        return str(eval(cadena))
