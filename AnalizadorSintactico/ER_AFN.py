from AnalizadorLexico.AFN import AFN
from AnalizadorLexico.AnalizadorLex import AnalizadorLex

#Creacion del AFN a partir de una ER
class ER_AFN:
    def __init__(self, sigma):
        self.ExpRegular = sigma
        self.Res = None
        self.L = AnalizadorLex(sigma)

    def SetExpresion(self, sigma):
        self.ExpRegular = sigma
        self.L.SetSigma(sigma)

    def IniConversion(self):
        self.L.SetSigma(self.ExpRegular)  # Inicializar lexer
        f = AFN()
        if self.E(f):
            token = self.L.yylex()
            if token == 0:
                self.Res = f
                return True
        return False

    def E(self, A1):
        if self.T(A1):
            if self.Ep(A1):
                return True
        return False

    def Ep(self, A1):
        token = self.L.yylex()
        if token == 10:  # '|'
            A2 = AFN()
            if self.T(A2):
                A1.UnirAFN(A2)
                if self.Ep(A1):
                    return True
            return False
        self.L.UndoToken()
        return True

    def T(self, A1):
        if self.C(A1):
            if self.Tp(A1):
                return True
        return False

    def Tp(self, A1):
        token = self.L.yylex()
        if token == 20:  # concatenación (implícita)
            A2 = AFN()
            if self.C(A2):
                A1.ConcatenarAFN(A2)
                if self.Tp(A1):
                    return True
            return False
        self.L.UndoToken()
        return True

    def C(self, A1):
        if self.F(A1):
            if self.Cp(A1):
                return True
        return False

    def Cp(self, A1):
        token = self.L.yylex()
        if token == 30:
            A1.CerraduraPositiva()
        elif token == 40:
            A1.CerraduraKleene()
        elif token == 50:
            A1.Opcional()
        else:
            self.L.UndoToken()
        return True

    def F(self, A1):
        token = self.L.yylex()
        if token == 60:  # '('
            if self.E(A1):
                token = self.L.yylex()
                if token == 70:  # ')'
                    return True
            return False
        elif token == 80:  # símbolo normal
            simb1 = self.L.yytext[0]
            A1.CrearBasicoUno(simb1, 80)
            return True
        elif token == 90:  # '['
            token = self.L.yylex()
            if token == 80:
                simb1 = self.L.yytext[0]
                token = self.L.yylex()
                if token == 110:
                    token = self.L.yylex()
                    if token == 80:
                        simb2 = self.L.yytext[0]
                        token = self.L.yylex()
                        if token == 100:
                                                   # Verificamos que simb1 y simb2 sean válidos
                            if (simb1.isdigit() and simb2.isdigit()) or \
                            (simb1.islower() and simb2.islower()) or \
                            (simb1.isupper() and simb2.isupper()):
                                A1.CrearBasicoDos(simb1, simb2, 80)
                            return True
                        else:
                            print(f"Error: Rango inválido '{simb1}-{simb2}'")
            return False
        return False