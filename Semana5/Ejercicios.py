class Nodo:

    def __init__(self, dato, siguiente=None):
        self.dato = dato
        self.siguiente = None

a = Nodo (5)
b = Nodo (10)

print ("Referencia del objeto a:", a)
print ("Referencia del objeto b:", b)

a.siguiente = b

c = Nodo(15)
d = Nodo(20)
b.siguiente = c
c.siguiente = d
print ("Referencia del objeto c:", c)
print ("Referencia del objeto d:", d)


#------------------------------------------
#ASIGNACIÓN DE NODO A OTRO NODO DEL MEDIO
#------------------------------------------

n1 = Nodo(1)
n2 = Nodo(2)
n3 = Nodo(3)

n1.siguiente = n3
# Opción 1: Variable temporal
temp = n1.siguiente
n1.siguiente = n2
n1.siguiente.siguiente = temp

#Opción 2: sin variable temporal
n1.siguiente = n2
n2.siguiente = n3



