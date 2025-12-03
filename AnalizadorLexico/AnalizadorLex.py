from .AFD import AFD
from .EdoAFD import EdoAFD

class AnalizadorLex:
    def __init__(self, sigma=""):
        self.Token = -1
        self.EdoActual = -1
        self.EdoTransicion = -1
        self.PasoPorEdoAcept = False
        self.IniLexema = -1
        self.FinLexema = -1
        self.IndiceCaracterActual = 0
        self.CaracterActual = ''
        self.Automata = AFD()
        self.yytext = ""
        self.CadenaSigma = sigma
        self.Pila = []

    def CargarArchivoAFD(self, ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                lineas = [line.strip() for line in archivo.readlines() if line.strip()]
                
                self.Automata.EdosAFD = []
                estados = list(map(int, lineas[0].split()))
                self.Automata.NumEdos = len(estados)

                for i in estados:
                    edo = EdoAFD()
                    edo.id = i
                    self.Automata.EdosAFD.append(edo)

                self.Automata.EdoInicial = int(lineas[1])
                self.Automata.EdosAceptacion = set(map(int, lineas[2].split()))
                
                simbolos_en_orden = lineas[3].split() 
                self.Automata.Alfabeto = set(simbolos_en_orden)

                tabla = lineas[4:]

                for i, linea in enumerate(tabla):
                    partes = linea.split()
                    num_simbolos = len(simbolos_en_orden)
                    transiciones_destino = partes[:num_simbolos]
                    
                    if len(partes) != num_simbolos + 1:
                        print("ERROR AL CARGAR AFD")
                        print(f"Error de formato en la línea {i+5}!")
                        print(f"Esperado: {num_simbolos} transiciones + 1 token. Encontrado: {len(partes)}")
                        continue
                         
                    token = partes[-1]
                    
                    if token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
                        self.Automata.EdosAFD[i].Token = int(token)
                    else:
                        self.Automata.EdosAFD[i].Token = -1

                    for idx_simb, simb in enumerate(simbolos_en_orden):
                        destino = transiciones_destino[idx_simb]
                        
                        if destino != "-" and destino != "-1":
                            self.Automata.EdosAFD[i].transAFD[ord(simb)] = int(destino)

        except FileNotFoundError:
            print(f"Error! Archivo no encontrado en la ruta: {ruta}")
        except Exception as e:
            print(f"Error al cargar el archivo AFD: {e}")
            
    def yylex(self):
        if self.IndiceCaracterActual >= len(self.CadenaSigma):
            self.Token = 0
            self.yytext = ""
            return 0  # Fin de cadena

        estados_por_id = {edo.id: edo for edo in self.Automata.EdosAFD if edo is not None}
        est_actual = self.Automata.EdoInicial
        i = self.IndiceCaracterActual

        longitud_valida = 0
        token_valido = -1
        ultimo_estado_valido = -1

        while i < len(self.CadenaSigma):
            c = self.CadenaSigma[i]
            idx = ord(c)

            if est_actual not in estados_por_id:
                break

            edo_actual = estados_por_id[est_actual]

            if 0 <= idx < len(edo_actual.transAFD):
                destino = edo_actual.transAFD[idx]
                if destino == -1:
                    break
            else:
                break

            est_actual = destino

            if est_actual in self.Automata.EdosAceptacion:
                token_valido_actual = getattr(estados_por_id[est_actual], "Token", -1)
                if token_valido_actual != -1:
                    longitud_valida = i - self.IndiceCaracterActual + 1
                    token_valido = token_valido_actual
                    ultimo_estado_valido = est_actual

            i += 1

        if longitud_valida > 0:
            self.Pila.append((
                self.IndiceCaracterActual,
                self.Token,
                self.yytext,
                self.IniLexema,
                self.FinLexema
            ))
            self.yytext = self.CadenaSigma[self.IndiceCaracterActual : self.IndiceCaracterActual + longitud_valida]
            self.IniLexema = self.IndiceCaracterActual
            self.FinLexema = self.IndiceCaracterActual + longitud_valida - 1
            self.IndiceCaracterActual += longitud_valida
            self.Token = token_valido
            return token_valido
        else:
            # Si no se encontró lexema válido, avanzar uno y devolver error
            self.yytext = self.CadenaSigma[self.IndiceCaracterActual]
            print(f"Error Léxico: carácter inválido '{self.yytext}' en posición {self.IndiceCaracterActual}")
            self.IniLexema = self.IndiceCaracterActual
            self.FinLexema = self.IndiceCaracterActual
            self.IndiceCaracterActual += 1
            self.Token = -1
            return -1

    def UndoToken(self):
        if self.Pila:
            (
                self.IndiceCaracterActual,
                self.Token,
                self.yytext,
                self.IniLexema,
                self.FinLexema
            ) = self.Pila.pop()
        else:
            print("No hay token para deshacer.")
   
    def GetEdoLexic(self):
        return {
            "IndiceCaracterActual": self.IndiceCaracterActual,
            "Token": self.Token,
            "yytext": self.yytext,
            "IniLexema": self.IniLexema,
            "FinLexema": self.FinLexema,
            "Pila": list(self.Pila)  # Copia de la pila
        }

    def SetEdoLexic(self, estado):
        self.IndiceCaracterActual = estado.get("IndiceCaracterActual", -1)
        self.Token = estado.get("Token", -1)
        self.yytext = estado.get("yytext", "")
        self.IniLexema = estado.get("IniLexema", -1)
        self.FinLexema = estado.get("FinLexema", -1)
        self.Pila = list(estado.get("Pila", []))

    def SetSigma(self, sigma):
        self.CadenaSigma = sigma
        self.PasoPorEdoAcept = False
        self.IniLexema = 0
        self.FinLexema = -1
        self.IndiceCaracterActual = 0
        self.Token = -1
        self.Pila.clear()    
    
    def CadenaXAnalizar(self):
        return self.CadenaSigma[self.IndiceCaracterActual:]
    
    def Lexema(self):
        return self.yytext

    def HayMasTokens(self):
        # Verifica si quedan más tokens por analizar
        return self.IndiceCaracterActual < len(self.CadenaSigma)