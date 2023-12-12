class Optimizador:

    variables = dict()

    def optimizarCodigoIntermedio(self):
        print('Comenzando optimizacion')
        self.separarVariables()
        self.reemplazarTemporal()

    def separarVariables(self):
        with open("./output/CodigoIntermedio.txt", "r") as archivo:
            for linea in archivo:
                if '=' in linea:
                    lista = linea.split(' =')
                    variable = lista[0]
                    igualacion = lista[1].replace('\n', '')
                    self.variables[variable] = igualacion

        print('Todas las variables han sido obtenidas')

    def reemplazarTemporal(self):
        pass
