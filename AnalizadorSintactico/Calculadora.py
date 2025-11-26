# calculadora_parser.py
"""Analizador sintáctico por descenso recursivo para una calculadora científica.
Versión corregida: maneja lookahead correctamente, consume tokens en el lugar
adecuado y considera fin de entrada cuando el token == 0 (o -1 mapeado a 0).
Se construye la notación postfija y se evalúa la expresión numéricamente.
"""

from AnalizadorLexico.AnalizadorLex import AnalizadorLex
import math
from typing import Dict, Any


class Calculadora:
    def __init__(self, Tokens: Dict[str, int], AFD: str):
        self.lex = AnalizadorLex()
        self.Tokens = Tokens
        self._token = None
        self._lexema = ""
        self._postfija = []
        self._resultado = 0.0

        if AFD:
            self.lex.CargarArchivoAFD(AFD)

    @property
    def resultado(self) -> float:
        return self._resultado

    @property
    def postfija(self):
        return self._postfija

    def next_token(self) -> int:
        raw = self.lex.yylex()
        if raw == -1:
            raw = 0
        self._token = raw

        self._lexema = getattr(self.lex, "yytext", "") or ""

        # print(f"[NEXT_TOKEN] Token: {self._token}, Lexema: '{self._lexema}'")
        return self._token

    def SintacExpAritm(self) -> bool:
        # Punto de entrada del análisis sintáctico

        self._postfija = []
        self._resultado = 0.0

        self.next_token()

        # Cadena vacía, sin nada que analizar
        if self._token == 0:
            print("Error: expresión vacía.")
            return False

        # Error enviado desde el analizador léxico
        if self._token == -1:
            print("Error léxico al inicio.")
            return False

        valor = self.E()
        if valor is False:
            print("Error: expresión inválida.")
            return False

        # El token 0 indica fin de cadena
        if self._token == 0:
            self._resultado = valor
            return True

        # Si quedan más tokens por analizar y no es posible debido a algún error proveniente del analizador léxico
        print(f"Error: tokens restantes después de la expresión. Token: {self._token}, Lexema: '{self._lexema}'")
        return False

    # E -> T { (+|-) T }
    def E(self):
        izq = self.T()
        if izq is False:
            return False

        # mientras el lookahead sea + o -
        while self._token in (self.Tokens.get("SUMA"), self.Tokens.get("RESTA")):
            op = self._token
            # consumir operador
            self.next_token()
            der = self.T()
            if der is False:
                return False

            if op == self.Tokens.get("SUMA"):
                self._postfija.append("+")
                izq = izq + der
            else:
                self._postfija.append("-")
                izq = izq - der

        return izq

    # T -> P { (*|/) P }
    def T(self):
        izq = self.P()
        if izq is False:
            return False

        while self._token in (self.Tokens.get("PROD"), self.Tokens.get("DIV")):
            op = self._token
            
            # Siguiente token después de PROD o DIV
            self.next_token()
            der = self.P()
            if der is False:
                return False

            if op == self.Tokens.get("PROD"):
                self._postfija.append("*")
                izq = izq * der
            else:
                if der == 0:
                    print("Error: división por cero.")
                    return False
                self._postfija.append("/")
                izq = izq / der

        return izq

    # P -> F [ ^ P ]
    def P(self):
        izq = self.F()
        if izq is False:
            return False

        if self._token == self.Tokens.get("EXP"):
            # Siguiente token después de ^
            self.next_token()
            der = self.P()
            if der is False:
                return False
            self._postfija.append("^")
            try:
                izq = izq ** der
            except (OverflowError, ValueError) as e:
                print(f"Error en exponenciación: {e}")
                return False

        return izq

    # F -> ( E ) | NUM | PI | funciones | -F   (soporte para negativo unario)
    def F(self):
        # Paréntesis
        if self._token == self.Tokens.get("PAR_I"):
            # Siguiente token después de (
            self.next_token()
            valor = self.E()
            if valor is False:
                return False
            
            if self._token == self.Tokens.get("PAR_D"):
                # Siguiente token después de )
                self.next_token()
                return valor
            print("Error: paréntesis de cierre ')' faltante.")
            return False

        # Funciones científicas (cada token corresponde al nombre en Tokens)
        funciones: Dict[str, Any] = {
            "SIN": math.sin,
            "COS": math.cos,
            "TAN": math.tan,
            "ASIN": math.asin,
            "ACOS": math.acos,
            "ATAN": math.atan,
            "LOG": math.log10,
            "LN": math.log,
            "EXP_FN": math.exp,
        }

        for nombre, fn in funciones.items():
            if self._token == self.Tokens.get(nombre):
                fun = self._lexema

                # Siguiente token después de la función
                self.next_token()
                
                if self._token != self.Tokens.get("PAR_I"):
                    print(f"Error: se esperaba '(' después de {nombre}.")
                    return False
                # Siguiente token después de (
                self.next_token()
                valor = self.E()
                if valor is False:
                    return False
                if self._token != self.Tokens.get("PAR_D"):
                    print(f"Error: paréntesis de cierre ')' faltante en función {nombre}.")
                    return False
                # Siguiente token después de )
                self.next_token()
                
                self._postfija.append(fun)
                try:
                    resultado_fn = funciones[fun](valor)
                except (ValueError, ZeroDivisionError) as e:
                    print(f"Error en función {nombre}: {e}")
                    return False
                return resultado_fn

        # Constante PI
        if self._token == self.Tokens.get("PI"):
            self._postfija.append("pi")
            # Siguiente token después de PI
            self.next_token()
            return math.pi

        # Número
        if self._token == self.Tokens.get("NUM"):
            lex = self._lexema
            self._postfija.append(lex)
            # Siguiente token después de NUM y conversión a su valor
            try:
                valor = float(lex)
            except (ValueError, TypeError):
                print(f"Error: numero inválido '{lex}'.")
                return False
            
            # Siguiente token después de NUM
            self.next_token()
            return valor

        # Menos unario
        if self._token == self.Tokens.get("RESTA"):
            # Siguiente token después de -
            self.next_token()
            valor = self.F()
            if valor is False:
                return False
            self._postfija.append("neg")
            return -valor

        # Si no llega a un token valido
        if self._token == 0:
            print("Error sintáctico: fin inesperado de la expresión.")
        else:
            print(f"Error sintáctico: token inesperado '{self._lexema}' (id: {self._token})")
        return False

    def Evaluar(self, expresion: str) -> Dict[str, Any]:
        expresion = expresion.replace("\t", "").replace("\n", "")
        
        self.lex.SetSigma(expresion)
        exito = self.SintacExpAritm()
        return {
            "exito": exito,
            "resultado": self._resultado if exito else None,
            "postfija": self._postfija.copy() if exito else [],
            "error": None if exito else "Error en el análisis sintáctico"
        }
