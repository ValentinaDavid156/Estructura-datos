"Crear un Carrucel "

class Nodo:
    def __init__(self, dato=None, anterior=None, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente
        self.anterior = anterior

class Rutina_carrucel:
    def __init__(self):
        self.cabeza=None
        self.cola=None
        self.actual=None
        self.tamaño=0

    def insertar_ejercicio_inicial(self, dato):
        nuevo_nodo = Nodo(dato=dato)

        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
            nuevo_nodo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = nuevo_nodo
            self.actual = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.cola
            nuevo_nodo.siguiente = self.cabeza
            self.cola.siguiente = nuevo_nodo
            self.cabeza.anterior = nuevo_nodo
            self.cola = nuevo_nodo

        self.tamaño += 1
        print(f"Se ha insertado el ejercicio: {dato}")

    def siguiente_ejercicio(self):
        if self.actual:
            self.actual = self.actual.siguiente
            print(f"Ejercicio actual: {self.actual.dato}")

    def anterior_ejercicio(self):
        if self.actual:
            self.actual = self.actual.anterior
            print(f"Ejercicio actual: {self.actual.dato}")


if __name__ == "__main__":
    carrusel = Rutina_carrucel()

    carrusel.insertar_ejercicio_inicial("Sentadillas")
    carrusel.insertar_ejercicio_inicial("Press de banca")
    carrusel.insertar_ejercicio_inicial("Peso muerto")
    carrusel.insertar_ejercicio_inicial("Dominadas")

    print("\n--- Avanzando ---")
    carrusel.siguiente_ejercicio()
    carrusel.siguiente_ejercicio()

    print("\n--- Devolviéndose ---")
    carrusel.anterior_ejercicio()