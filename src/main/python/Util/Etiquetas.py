class Etiquetas:
    # dict = {<ID> = [labelFunc, labelRet]}
    _funciones = dict()
    _counter = 0

    def next_etiqueta(self):
        etiqueta = f'l{Etiquetas._counter}'
        Etiquetas._counter += 1
        return etiqueta

    def etiqueta_funcion(self, identificador):
        # si el identificador existe, me devuelve la lista de etiquetas
        for id in Etiquetas._funciones:
            if str(id) == str(identificador):
                return Etiquetas._funciones[id]
        # si el identificador no existe, debo generar las etiquetas para la funcion
        list = []
        etiqueta1 = Etiquetas.next_etiqueta(self)
        etiqueta2 = Etiquetas.next_etiqueta(self)

        list.append(etiqueta1)
        list.append(etiqueta2)

        Etiquetas._funciones[identificador] = list

        return list
