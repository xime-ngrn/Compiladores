class SimboloG:
    def __init__(self, nomb_simb: str = "", es_terminal: bool = False, token: int = -1):
        self.NombSimb = nomb_simb
        self.EsTerminal = es_terminal
        self.Token = token

    def __repr__(self):
        tipo = "T" if self.EsTerminal else "NT"
        return f"{self.NombSimb}({tipo})"

    def __eq__(self, other):
        if not isinstance(other, SimboloG):
            return False
        return self.NombSimb == other.NombSimb and self.EsTerminal == other.EsTerminal

    def __hash__(self):
        return hash((self.NombSimb, self.EsTerminal))