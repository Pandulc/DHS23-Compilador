class Etiquetas:

    def __init__(self):
        self.counter = 0

    def next_etiqueta(self):
        etiqueta = f'l{self.counter}'
        self.counter += 1
        return etiqueta
