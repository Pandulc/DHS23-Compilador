# implementar: with ManejoArchivo('nombre.txt') as nombre:


class ManejoArchivo:

    def __init__(self, nombre):
        self.nombre = nombre

    def __enter__(self):
        self.nombre = open(self.nombre, 'a')
        return self.nombre

    def __exit__(self, tipo_exceptcion, valor_excepcion, traza_error):
        if self.nombre:
            self.nombre.close()


if __name__ == '__main__':
    with ManejoArchivo('output/prueba.txt') as archivoPrueba:
        archivoPrueba.write('hola mundo')