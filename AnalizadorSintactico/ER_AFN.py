"""
Analizador sintáctico para construir un AFN a partir de una expresión regular.
Versión CORREGIDA con recursión adecuada en _Ep.
"""

from AnalizadorLexico.AFN import AFN
from AnalizadorLexico.AnalizadorLex import AnalizadorLex
from typing import Dict, Optional

class ER_AFN:
    def __init__(self, sigma: str, tokens: Dict[str, int], AFD_P: Optional[str]):
        self.lex = AnalizadorLex()
        self.tokens = tokens
        self.exp_regular = sigma
        self.result = None

        if AFD_P:
            self.lex.CargarArchivoAFD(AFD_P)

    def SetExpression(self, sigma: str) -> None:
        """Establece una nueva expresión regular"""
        self.exp_regular = sigma
        self.lex.SetSigma(sigma)

    def IniConversion(self) -> Optional[AFN]:
        """
        Inicia la conversión de la expresión regular a AFN.
        Retorna el AFN generado o None si hay error.
        """
        if not self.exp_regular:
            print("Error: expresión regular vacía.")
            self.result = None
            return None

        self.lex.SetSigma(self.exp_regular)
        afn = AFN()

        try:
            if self._E(afn):
                token = self.lex.yylex()
                if token == 0:  # Fin de cadena
                    self.result = afn
                    return self.result
                raise SyntaxError(f"Error: se esperaba fin de cadena, se obtuvo token {token}")
            raise SyntaxError("Error en el análisis de la expresión.")
        except SyntaxError as se:
            print(f"Error de sintaxis: {se}")
            self.result = None
            return None
        except Exception as e:
            print(f"Error inesperado durante el análisis: {e}")
            import traceback
            traceback.print_exc()
            self.result = None
            return None

    def _E(self, afn: AFN) -> bool:
        """E → T Ep"""
        return self._T(afn) and self._Ep(afn)

    def _Ep(self, afn: AFN) -> bool:
        """ Ep → | T Ep | ε """
        token = self.lex.yylex()

        if token == self.tokens['OR']:
            afn2 = AFN()
            if not self._T(afn2):
                raise SyntaxError("Error al parsear término después de '|'")
            if not self._Ep(afn2):
                raise SyntaxError("Error en la recursión de Ep")
            afn.UnirAFN(afn2)
            return True
        
        # ε: solo hacer UndoToken si no es fin de cadena
        if token != 0:
            self.lex.UndoToken()
        return True

    def _T(self, afn: AFN) -> bool:
        """T → C Tp"""
        return self._C(afn) and self._Tp(afn)

    def _Tp(self, afn: AFN) -> bool:
        """
        Tp → C Tp | ε }"""
        token = self.lex.yylex()

        if token in [self.tokens['SIMB'], self.tokens['PAR_I'], self.tokens['COR_I']]:
            self.lex.UndoToken()
            afn2 = AFN()
            if not self._C(afn2):
                return False
            if not self._Tp(afn2):
                return False
            afn.ConcatenarAFN(afn2)
            return True
        
        # ε: solo hacer UndoToken si no es fin de cadena
        if token != 0:
            self.lex.UndoToken()
        return True

    def _C(self, afn: AFN) -> bool:
        """C → F Cp"""
        return self._F(afn) and self._Cp(afn)

    def _Cp(self, afn: AFN) -> bool:
        """Cp → * | + | ? | ε"""
        token = self.lex.yylex()
        
        if token == self.tokens['CERR_POS']:
            afn.CerraduraPositiva()
            return True
        elif token == self.tokens['CERR_KLEEN']:
            afn.CerraduraKleene()
            return True
        elif token == self.tokens['OPC']:
            afn.Opcional()
            return True
        
        # ε: solo hacer UndoToken si no es fin de cadena
        if token != 0:
            self.lex.UndoToken()
        return True

    def _F(self, afn: AFN) -> bool:
        """F → (E) | symbol | [a-z]"""
        token = self.lex.yylex()
        
        # Caso 1: (E)
        if token == self.tokens['PAR_I']:
            if self._E(afn):
                token = self.lex.yylex()
                if token == self.tokens['PAR_D']:
                    return True
                raise SyntaxError("Se esperaba ')' para cerrar el paréntesis")
            return False
        
        # Caso 2: símbolo simple
        elif token == self.tokens['SIMB']:
            if not self.lex.yytext:
                raise SyntaxError("Lexema vacío para símbolo")
            simbolo = self.lex.yytext[0]
            afn.CrearBasicoUno(simbolo, token)
            return True
        
        # Caso 3: rango [a-z]
        elif token == self.tokens['COR_I']:
            return self._parsear_rango(afn)
        
        raise SyntaxError(f"Token inesperado: {token}. Se esperaba símbolo, '(' o '['")

    def _parsear_rango(self, afn: AFN) -> bool:
        """Parsea un rango del tipo [a-z]"""
        token = self.lex.yylex()
        if token != self.tokens['SIMB']:
            raise SyntaxError("Se esperaba un símbolo después de '['")
        
        simb1 = self.lex.yytext[0]
        
        token = self.lex.yylex()
        if token != self.tokens['GUION']:
            raise SyntaxError("Se esperaba '-' en el rango")
        
        token = self.lex.yylex()
        if token != self.tokens['SIMB']:
            raise SyntaxError("Se esperaba un símbolo después de '-'")
        
        simb2 = self.lex.yytext[0]
        
        # Validar que el rango sea válido
        if ord(simb1) > ord(simb2):
            raise SyntaxError(f"Rango inválido: [{simb1}-{simb2}]. El primer carácter debe ser menor o igual al segundo")
        
        token = self.lex.yylex()
        if token != self.tokens['COR_D']:
            raise SyntaxError("Se esperaba ']' para cerrar el rango")
        
        afn.CrearBasicoDos(simb1, simb2, self.tokens['SIMB'])
        return True

    def GetAFN(self) -> Optional[AFN]:
        """Devuelve el AFN resultante del análisis sintáctico"""
        return self.result