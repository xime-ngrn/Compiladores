class Estado:
    NumEstados = 0
    def __init__(self):
        self.IdEdo = Estado.numEstados
        Estado.NumEstados += 1
        self.EdoAcept = False
        self.Token = -1
        self.Transiciones = set()