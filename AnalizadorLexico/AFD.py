from EdoAFD import EdoAFD

class AFD():
    def __init__(self, n=0):
        if n > 0:
            self.EdosAFD = [EdoAFD() for _ in range(n)]
            for i, edo in enumerate(self.EdosAFD):
                edo.id = i
        else:
            self.EdosAFD = []
            
        self.Alfabeto = set()
        self.NumEdos = n
        self.EdosAceptacion = set()
        self.EdoInicial = 0

    def _ensure_index(self, idx):
        """Asegura que exista un estado con índice idx en self.EdosAFD."""
        while idx >= len(self.EdosAFD):
            nuevo = EdoAFD()
            nuevo.id = len(self.EdosAFD)
            self.EdosAFD.append(nuevo)
        self.NumEdos = len(self.EdosAFD)


    def AgregarTransicion(self, desde, hacia, simbolo):
        """Agrega una transición desde un estado hacia otro con un símbolo dado."""
        if not isinstance(simbolo, str) or len(simbolo) != 1:
            raise ValueError(f"El símbolo '{simbolo}' debe ser un carácter único (str de longitud 1).")

        # Asegurar que existan los índices
        self._ensure_index(desde)
        self._ensure_index(hacia)

        # Registrar transición
        self.EdosAFD[desde].transAFD[ord(simbolo)] = hacia

    

