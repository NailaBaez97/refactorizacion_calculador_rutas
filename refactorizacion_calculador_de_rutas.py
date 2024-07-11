class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.mapa = [["."] * columnas for _ in range(filas)]
        self.inicio = None
        self.fin = None
        self.obstaculos = []

    def agregar_obstaculo(self, x, y):
        if self.es_celda_valida(x, y):
            self.mapa[y][x] = "X"
            self.obstaculos.append((x, y))

    def quitar_obstaculo(self, x, y):
        if self.es_celda_valida(x, y):
            self.mapa[y][x] = "."
            self.obstaculos.remove((x, y))

    def es_accesible(self, x, y):
        return self.es_celda_valida(x, y) and self.mapa[y][x] != "X"

    def es_celda_valida(self, x, y):
        return 0 <= x < self.columnas and 0 <= y < self.filas

    def imprimir_mapa(self):
        for fila in self.mapa:
            print(" ".join(str(cell) for cell in fila))


class CalculadoraRuta:
    def __init__(self, mapa):
        self.mapa = mapa

    def heuristica(self, nodo, fin):
        return abs(nodo[0] - fin[0]) + abs(nodo[1] - fin[1])

    def obtener_vecinos(self, nodo):
        vecinos = []
        movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for movimiento in movimientos:
            nueva_posicion = nodo[0] + movimiento[0], nodo[1] + movimiento[1]
            if self.mapa.es_accesible(nueva_posicion[0], nueva_posicion[1]):
                vecinos.append(nueva_posicion)
        return vecinos

    def construir_camino(self, padres, nodo_final):
        camino = []
        actual = nodo_final
        while actual:
            camino.append(actual)
            actual = padres.get(actual)
        camino.reverse()

        camino_diccionario = {}
        for (x, y) in camino:
            if self.mapa.mapa[y][x] not in ("I", "F"):
                camino_diccionario[(x, y)] = '*'
        return camino_diccionario

    def implementar_algoritmo_a_estrella(self):
        x_inicio, y_inicio = self.mapa.inicio
        x_fin, y_fin = self.mapa.fin
        nodo_inicial = (x_inicio, y_inicio)
        nodo_final = (x_fin, y_fin)

        lista_visitar = [nodo_inicial]
        lista_visitado = []
        g = {nodo_inicial: 0}
        h = {nodo_inicial: self.heuristica(nodo_inicial, nodo_final)}
        f = {nodo_inicial: h[nodo_inicial]}
        padres = {nodo_inicial: None}

        while lista_visitar:
            menor_costo = min(lista_visitar, key=lambda nodo: f[nodo])

            if menor_costo == nodo_final:
                camino_diccionario = self.construir_camino(padres, nodo_final)
                for (x, y), valor in camino_diccionario.items():
                    self.mapa.mapa[y][x] = valor
                return camino_diccionario

            lista_visitar.remove(menor_costo)
            lista_visitado.append(menor_costo)

            for vecino in self.obtener_vecinos(menor_costo):
                if vecino in lista_visitado:
                    continue

                tentative_g = g[menor_costo] + 1

                if vecino not in lista_visitar:
                    lista_visitar.append(vecino)
                elif tentative_g >= g.get(vecino, float('inf')):
                    continue

                padres[vecino] = menor_costo
                g[vecino] = tentative_g
                h[vecino] = self.heuristica(vecino, nodo_final)
                f[vecino] = g[vecino] + h[vecino]

        return None


class VistaUsuario:
    def __init__(self):
        self.mapa = None

    def obtener_datos_usuario(self):
        while True:
            try:
                filas = int(input("Ingrese la cantidad de filas: "))
                columnas = int(input("Ingrese la cantidad de columnas: "))
                if filas < 2 or columnas < 2:
                    print("El tamanho ingresado no es valido")
                else:
                    break
            except ValueError:
                print("Por favor, ingrese un numero valido.")

        self.mapa = Mapa(filas, columnas)

        while True:
            try:
                inicio = input("Ingrese las coordenadas de Inicio (x,y) separadas por comas: ")
                x_inicio, y_inicio = map(int, inicio.split(','))
                fin = input("Ingrese las coordenadas de fin (x,y) separadas por comas: ")
                x_fin, y_fin = map(int, fin.split(','))

                if not self.mapa.es_celda_valida(x_inicio, y_inicio):
                    print("La coordenada de inicio esta fuera de rango")
                    continue

                if not self.mapa.es_celda_valida(x_fin, y_fin):
                    print("La coordenada de fin esta fuera de rango")
                    continue

                self.mapa.mapa[y_inicio][x_inicio] = "I"
                self.mapa.mapa[y_fin][x_fin] = "F"
                self.mapa.inicio = (x_inicio, y_inicio)
                self.mapa.fin = (x_fin, y_fin)
                break
            except ValueError:
                print("Por favor, ingrese coordenadas validas separadas por comas.")

        self.mapa.imprimir_mapa()

        
        while True:
            try:
                obstaculos = int(input("Ingrese la cantidad de obstaculos que desee: "))
                for i in range(obstaculos):
                    while True:
                        try:
                            posicion_obstaculos = input(f"Ingrese la coordenada del obstaculo nro {i+1} (x,y) separadas por comas: ")
                            x_obstaculo, y_obstaculo = map(int, posicion_obstaculos.split(','))

                            if not self.mapa.es_celda_valida(x_obstaculo, y_obstaculo):
                                print("Las coordenadas del obstaculo estan fuera del rango.")
                            elif (x_obstaculo, y_obstaculo) in [self.mapa.inicio, self.mapa.fin]:
                                print("La coordenada no puede estar en la posicion del inicio o fin.")
                            else:
                                self.mapa.agregar_obstaculo(x_obstaculo, y_obstaculo)
                                break
                        except ValueError:
                            print("Por favor, ingrese coordenadas validas separadas por comas.")
                break
            except ValueError:
                print("Por favor, ingrese un numero valido.")

        self.mapa.imprimir_mapa()

        # Opcion para eliminar obstaculos
        quitar = input("Desea eliminar algun obstaculo? (s/n): ")
        if quitar.lower() == 's':
            while True:
                try:
                    obstaculos_eliminar = int(input("Ingrese la cantidad de obstaculos que desee eliminar: "))
                    for i in range(obstaculos_eliminar):
                        while True:
                            try:
                                posicion_obstaculo_eliminar = input(f"Ingrese la coordenada del obstaculo a eliminar nro {i+1} (x,y) separadas por comas: ")
                                x_obstaculo_eliminar, y_obstaculo_eliminar = map(int, posicion_obstaculo_eliminar.split(','))

                                if not self.mapa.es_celda_valida(x_obstaculo_eliminar, y_obstaculo_eliminar):
                                    print("Las coordenadas del obstaculo estan fuera del rango.")
                                elif (x_obstaculo_eliminar, y_obstaculo_eliminar) not in self.mapa.obstaculos:
                                    print("No hay un obstaculo en esa coordenada.")
                                else:
                                    self.mapa.quitar_obstaculo(x_obstaculo_eliminar, y_obstaculo_eliminar)
                                    break
                            except ValueError:
                                print("Por favor, ingrese coordenadas validas separadas por comas.")
                    break
                except ValueError:
                    print("Por favor, ingrese un numero valido.")


        return self.mapa, x_inicio, y_inicio, x_fin, y_fin


if __name__ == "__main__":
    # Crear instancia de InterfazUsuario para obtener datos del usuario
    interfaz = VistaUsuario()
    mapa, x_inicio, y_inicio, x_fin, y_fin = interfaz.obtener_datos_usuario()

    if mapa:
        # Crear instancia de CalculadoraRuta para calcular la ruta
        calculadora = CalculadoraRuta(mapa)
        camino_diccionario = calculadora.implementar_algoritmo_a_estrella()

        if camino_diccionario:
            # Imprimir el mapa con el camino encontrado
            mapa.imprimir_mapa()
        else:
            print("No se encontro un camino valido.")
