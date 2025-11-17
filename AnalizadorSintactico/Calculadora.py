from AnalizadorLexico import AnalizadorLexico

class Calculadora: 
    def __init__(self, Token, AFD = None):
        self.lex = AnalizadorLexico()
        self.Tokens = Token
        if AFD:
             self.lex.CargarArchivoAFD(AFD)  
        self.Token = -1

    def SintacExpAritm(self):
        self.Token
        if self.E():
            Token = self.lex.yylex()
            if Token == 0:
                return True
            return False
    
    def E(self):
        if self.T():
            if self.Ep():
                return True
            return False
       
    def Ep(self):
        self.Token = self.lex.yylex()
        if self.Token == self.Tokens.get("SUMA") or self.Token == self.Tokens.get("RESTA"):
            if self.T():
                if self.Ep():
                    return True
            return False
        self.lex.UndoToken()
        return True
    
    def T(self):
        if self.P():
            if self.Tp():
                return True
        return False
    
    def Tp(self):
        self.Token = self.lex.yylex()
        if self.Token == self.Tokens.get("PROD") or self.Token == self.Tokens.get("DIV"):
            if self.P():
                if self.Tp():
                    return True
            return False
        self.lex.UndoToken()
        return True
    
    def P(self):
        if self.F():
            if self.Pp():
                return True
        return False
    
    def Pp(self):
        self.Token = self.lex.yylex()
        if self.Token == self.Tokens.get("EXP"):
            if self.F():
                if self.Pp():
                    return True
            return False
        self.lex.UndoToken()
        return True
    
    def F(self):
        # Manejo de paréntesis
        self.Token = self.lex.yylex()
        if self.Token == self.Tokens.get('PAR_I'):
            if self.E():
                self.Token = self.lex.yylex()
                if self.Token == self.Tokens.get("PAR_D"):
                    return True
            return False
        
        #Funciones trigonométricas y logarítmicas
        elif self.Token in [self.Tokens.get(f) for f in ["SEN", "COS", "TAN", "ASEN", "ACOS", "ATAN", "LOG", "LN", "EXP"]]:
            self.Token = self.lex.yylex()
            if self.Token == self.Tokens.get("PAR_I"):
                if self.E():
                    self.Token = self.lex.yylex()
                    if self.Token == self.Tokens.get("PAR_D"):
                        return True
            return False
        
        # Manejo de números y constantes
        elif self.Token == self.Tokens.get("PI"):
            self.Token = self.lex.yylex()
            return True
    
        elif self.Token == self.Tokens.get("NUM"):
            return True
        
        return False