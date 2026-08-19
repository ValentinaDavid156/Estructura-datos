# Código base — Semana 02
# Fuente: 01-Momento-1-Contrato-y-secuencia/02-Semana-02-ADT-y-Spec-Driven-Development/02-guia-de-laboratorio.html

class ElementoNoEncontradoError(Exception):
    pass

class BolsaDict:
    """Bolsa implementada como diccionario de conteos.

    Complejidad:
        agregar  -> O(1)
        sacar    -> O(1)
        cuantos  -> O(1)
        tamaño   -> O(1)
        contiene -> O(1)
    """

    def __init__(self):
        self._conteos = {}
        self._total = 0

    def agregar(self, elemento):
        self._conteos [elemento] = self._conteos.get(elemento, 0) + 1
        self._total += 1

    def sacar(self, elemento):
        if self._conteos.get (elemento, 0) == 0:
            raise ElementoNoEncontradoError(
                f"'{elemento}' no esta en la bolsa"
            )
        self._conteos [elemento] -= 1
        if self._conteos [elemento] == 0:
            del self._conteos[elemento]
        self._total -= 1

    def cuantos(self, elemento):
        return self._conteos.get(elemento, 0)

    def tamaño(self):
        return self._total

    def contiene(self, elemento):
        return elemento in self._conteos
