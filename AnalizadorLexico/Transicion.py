import Estado

class Transicion:
    def __init__(self, c_inf = None, c_sup = None, edoDestino = None):

        if c_inf is None and c_sup is None and edoDestino is None:
            # Transición vacía
            self.SimboloInf = None
            self.SimboloSup = None
            self.EdoDestino = None
        elif c_sup is None and edoDestino is not None:
            # Caso: Transicion(char c, Estado e)
            self.SimboloInf = c_inf
            self.SimboloSup = c_inf
            self.EdoDestino = edoDestino
        else:
            # Caso: Transicion(char c_inf, char c_sup, Estado e)
            self.SimboloInf = c_inf
            self.SimboloSup = c_sup
            self.EdoDestino = edoDestino
    
    def tieneTransicion(self, c):
        resultados = set()
        if self.SimboloInf is not None and self.SimboloSup is not None:
            if self.SimboloInf <= c <= self.SimboloSup:
                resultados.add(self.EdoDestino)
        return resultados