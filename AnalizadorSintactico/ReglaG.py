class ReglaG:
    def __init__(self, simb_izq=None, lado_der=None):
        self.SimbIzq = simb_izq  # SimboloG
        self.LadoDer = lado_der if lado_der is not None else []  # Lista de SimboloG

    def __repr__(self):
        lado_izq = self.SimbIzq.NombSimb if self.SimbIzq else "None"
        lado_der = " ".join([s.NombSimb for s in self.LadoDer]) if self.LadoDer else ""
        return f"{lado_izq} -> {lado_der}"