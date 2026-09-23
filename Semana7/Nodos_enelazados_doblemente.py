"Crear una lista enlazada donde se pueda hacer y deshacer un Nodo - lista de datos "

class Nodo: 
        def __init__(self, dato = None, anterior=None, siguiente=None):
              self.anterior = anterior
              self.siguiente = siguiente
              self.dato = dato

class ListadoblementeEnlazada:
        def __init__(self):
              self.cabeza = None
              self.cola = None
              self.actual = None
              self.tamaño = 0
              
        def insertar (self, dato):
              nuevo_nodo = Nodo(dato=dato)

              if self.cabeza is None:
                  self.cabeza = nuevo_nodo
                  self.cola = nuevo_nodo
              else:
                    nuevo_nodo.anterior = self.cola
                    self.cola.siguiente = nuevo_nodo
                    self.cola = nuevo_nodo

              self.actual = nuevo_nodo
              self.tamaño += 1
              print (f"Se ha insertado el nodo con dato: {dato}")

        def deshacer(self):
              if self.actual and self.actual.anterior:
                    self.actual = self.actual.anterior
                    print(f"Deshacer a: {self.actual.dato}")
              else:
                    print(f"No hay más datos para deshacer.") 

        def rehacer(self):
              if self.actual and self.actual.siguiente:
                    self.actual = self.actual.siguiente
                    print(f"Rehacer a: {self.actual.dato}")
              else:
                    print(f"No hay más datos para rehacer.")   

        def mostrar_estado(self):
              if self.actual:
                    print(f"Estado actual: {self.actual.dato}")
              else:
                    print("Lista vacía o no hay estado actual.")
                        
                    
                  
                 
