class automovil:
    marca: str
    color: str 
    modelo: str
    anio: int
  

def __init__(self, marca: str):
    self.marca = marca

def set_color(self, color: str):
    self.color = color

def set_modelo(self, modelo: str):
    self.modelo = modelo

def set_anio(self, anio: int):
    self.anio = anio

def revisar_estado(self)-> bool:
    #codigo ..........
    return True

auto1 = automovil('Mazda')
auto2 = automovil('Toyota')
auto3 = automovil('Mazda')
auto4 = auto1

if auto1 == auto3:
    print("Los autos son iguales")  
else:
    print("Los autos son diferentes")   


