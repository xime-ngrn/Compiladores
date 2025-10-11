class Estado:
    NumEstados = 0
    def __init__(self):
        self.IdEdo = Estado.NumEstados
        Estado.NumEstados += 1
        self.EdoAcept = False
        self.Token = -1
        self.Transiciones = set()
        
    def TieneTransicionCon(self, c):
        r = set()
        for t in self.Transiciones:
            if t.SimboloInf <= c <= t.SimboloSup:
                r.add(t.EdoDestino)
        return r
    
    def __str__(self):
        return f"Estado({self.IdEdo}, Acept: {self.EdoAcept}, Token: {self.Token})"
    
    def __hash__(self):
        return hash(self.IdEdo)