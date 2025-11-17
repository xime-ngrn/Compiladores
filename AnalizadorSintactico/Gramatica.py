from SimboloG import SimboloG
from ReglaG import ReglaG
class Gramatica():
    def __init__(self):
        self.NumReglas = 0
        self.Reglas = []
        self.VN = set()
        self.VT = set()
        self.SimboloInicial = SimboloG()
    
    #Operacion First
    def First(self, l = None):
        if l == None or len(l) == 0:
            return set()

        R = set()

        if l[0].EsTerminal:
            R.add(l[0])
            return R
        
        for i in range(self.NumReglas):
            if self.Reglas[i].SimbIzq.NombSimb == l[0].NombSimb:
                R |= (self.First(self.Reglas[i].LadoDer))
        
        if "ε" in R:
            if len(l) == 1:
                return R
            R |= self.First(l[1:])
        return R
    
    #Operacion Follow
    def Follow(self, s = SimboloG()):
        j = None
        R = set()

        if s.EsTerminal:
            return R
        
        if s == self.SimboloInicial:
            R.add("$")

        for i in range(self.NumReglas):
            if s in self.Reglas[i].LadoDer:
                j = self.Reglas[i].LadoDer.index(s)

            if j == len(self.Reglas[i].LadoDer) - 1:
                if s == self.Reglas[i].SimbIzq:
                    continue
                R |= self.Follow(self.Reglas[i].SimbIzq)
                continue

            self.Aux = self.First(self.Reglas[i].LadoDer[j+1:])
            
            if "ε" in self.Aux:
                self.Aux = self.Aux - {"ε"}
                R |= self.Aux
                R |= self.Follow(self.Reglas[i].SimbIzq)
                continue
            R |= self.Aux
        
        return R

    def G(self):
        if self.Reglas():
            return True
        return False
    
    def Reglas(self):
        self.Token = None
        if self.Regla():
            self.Token = self.Lexic.yylex
            if self.Token == "PUNTO-COMA":
                if self.ReglasP():
                    return True
            return False
    
    def ReglasP(self):
        self.Token = None
        self.EdoLexico = self.Lexic.EdoActual

        if self.Regla():
            self.Token = self.Lexic.yylex()
            if self.Token == [self.Token]:
                if self.ReglasP():
                    return True
                return False
        self.Lexic.SetEstado(self.EdoLexico)
        return True
    
    def Regla(self):
        self.LexemaLadoIzq = ""
        self.Token = None

        if self.LadoIzq(self.LexemaLadoIzq):
            self.Token = self.Lexic.yylex()
            if self.Token == "FLECHA":
                if self.LadoDer(self.LexemaLadoIzq):
                    return True

        return False

    def LadoIzq(self, LexemaLadoIzq):
        s = SimboloG()
        self.Token = self.Lexic.yylex()

        if self.Token == "SIMBOLO":
            s.NumbSimb = self.Lexic.yytext
            s.EsTerminal = False
            self.VN.add(s)
            LexemaLadoIzq = self.Lexic.yytext
            return True
        
        return False
    
    def LadoDer(self, LexemaLadoIzq):
        l = []
        self.Token = None

        if self.SecSimbolos(l):
            regla = ReglaG()
            regla.SimbIzq = SimboloG()
            regla.SimbIzq.NombSimb = LexemaLadoIzq
            regla.SimbIzq.EsTerminal = False
            regla.LadoDer = l
            self.Reglas.append(regla)
            self.NumReglas += 1
            return True
        
        return False
    
    def SecSimbolos(self, l = []):
        self.Token = self.Lexic.yylex()
        
        if self.Token == "SIMBOLO":
            s = SimboloG()
            s.NombSimb = self.Lexic.yytext
            if (self.SecSimbolosP(l)):
                l.addinicio(s)
                return True
        
        return False
    
    def SecSimbolosP(self, l = []):
        self.Token = self.Lexic.yylex()

        if self.Token == "SIMBOLO":
            s = SimboloG()
            s.NombSimb = self.Lexic.yytext
            if(self.SecSimbolosP(l)):
                l.insert(0, s)
                return True
        
        self.Lexic.UndoToken()
        return True