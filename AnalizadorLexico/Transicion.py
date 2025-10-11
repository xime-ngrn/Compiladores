from Estado import Estado

class Transicion:
    def __init__(self, c_inf=None, c_sup=None, edoDestino=None):
        if c_inf is None and c_sup is None and edoDestino is None:
            # Transición vacía
            self.SimboloInf = None
            self.SimboloSup = None
            self.EdoDestino = None

        elif isinstance(c_sup, Estado):  
            # Caso: Transicion(char c, Estado e)
            self.SimboloInf = c_inf
            self.SimboloSup = c_inf
            self.EdoDestino = c_sup

        else:
            # Caso: Transicion(char c_inf, char c_sup, Estado e)
            self.SimboloInf = c_inf
            self.SimboloSup = c_sup
            self.EdoDestino = edoDestino

    def __eq__(self, other):
        if not isinstance(other, Transicion):
            return False
        return (self.SimboloInf == other.SimboloInf and
                self.SimboloSup == other.SimboloSup and
                self.EdoDestino is other.EdoDestino)

    def __hash__(self):
        # EdoDestino se identifica por su IdEdo
        dest_id = None if self.EdoDestino is None else self.EdoDestino.IdEdo
        return hash((self.SimboloInf, self.SimboloSup, dest_id))

    def __repr__(self):
        return f"Trans({self.SimboloInf}-{self.SimboloSup} -> {None if self.EdoDestino is None else self.EdoDestino.IdEdo})"