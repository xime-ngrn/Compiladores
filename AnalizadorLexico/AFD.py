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

    def cargarArchivo(self, ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                lineas = [line.strip() for line in archivo.readlines() if line.strip()]
                
                self.EdosAFD = []
                estados = list(map(int, lineas[0].split()))
                self.NumEdos = len(estados)

                for i in estados:
                    edo = EdoAFD()
                    edo.id = i
                    self.EdosAFD.append(edo)

                self.EdoInicial = int(lineas[1])
                self.EdosAceptacion = set(map(int, lineas[2].split()))
                
                simbolos_en_orden = lineas[3].split() 
                self.Alfabeto = set(simbolos_en_orden) 

                # LECTURA DE LA TABLA DE TRANSICIONES
                tabla = lineas[4:]

                for i, linea in enumerate(tabla):
                    partes = linea.split()
                    
                    # El número de transiciones debe ser igual al número de símbolos.
                    num_simbolos = len(simbolos_en_orden)
                    transiciones_destino = partes[:num_simbolos]
                    
                    # Verificación de longitud de la línea
                    if len(partes) != num_simbolos + 1:
                         print(f"Error de formato en la línea {i+5}!")
                         print(f"Esperado: {num_simbolos} transiciones + 1 token. Encontrado: {len(partes)}")
                         continue
                         
                    token = partes[-1]
                    
                    # Asignar Token
                    if token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
                        self.EdosAFD[i].Token = int(token)
                    else:
                        self.EdosAFD[i].Token = -1

                    transiciones_del_estado = []
                    for idx_simb, simb in enumerate(simbolos_en_orden):
                        destino = transiciones_destino[idx_simb]
                        
                        if destino != "-":
                            self.EdosAFD[i].transAFD[ord(simb)] = int(destino)
                            transiciones_del_estado.append((simb, int(destino)))
                        else:
                            transiciones_del_estado.append((simb, destino))

        except FileNotFoundError:
            print(f"Error! Archivo no encontrado en la ruta: {ruta}")
        except Exception as e:
            print(f"Error! No se ha podido cargar el archivo. Detalles: {e}")

    def evaluarCad(self, cadena):
        resultados = {}
        inicio = 0
        estados_por_id = {edo.id: edo for edo in self.EdosAFD if edo is not None}

        while inicio < len(cadena):
            est_actual = self.EdoInicial
            i = inicio
            
            # Variables para rastrear la coincidencia más larga (Maximal Munch)
            longitud_valida = 0
            token_valido = -1
            ultimo_estado_valido = -1

            print(f"\n--- Iniciando escaneo desde índice {inicio} ('{cadena[inicio:]}') ---")

            while i < len(cadena):
                c = cadena[i]
                idx = ord(c)
                
                print(f"  > Pos {i}, Carácter '{c}'. Estado actual: {est_actual}")

                if est_actual not in estados_por_id:
                    # Verificar si el estado tiene la transiciónif est_actual not in estados_por_id:
                    print(f"  > Detenido: Estado {est_actual} no existe en el AFD.")
                    break
            
                edo_actual = estados_por_id[est_actual]
                
                # Verificar si el estado tiene la transición
                destino = None
                if 0 <= idx < len(edo_actual.transAFD):
                    destino = edo_actual.transAFD[idx]
                    if destino == -1:
                        destino = None
                    
                if destino is not None:
                    est_actual = destino
                    
                    # Validar que el destino sea un estado válido
                    if est_actual not in estados_por_id:
                        print(f"  > Detenido: Transición a estado inválido ({est_actual}).")
                        break 

                    # Registrar la coincidencia si el nuevo estado es de aceptación
                    if est_actual in self.EdosAceptacion:
                        token_valido_actual = getattr(estados_por_id[est_actual], "Token", -1)
                        
                        # Solo actualizamos si encontramos un token válido
                        if token_valido_actual != -1: 
                            longitud_valida = i - inicio + 1
                            token_valido = token_valido_actual
                            ultimo_estado_valido = est_actual
                            print(f"  >Coincidencia temporal: Longitud {longitud_valida}, Token {token_valido}.")
                    
                    i += 1
                else:
                    # No hay transición: el lexema terminó
                    print(f"  > Detenido: No hay transición para el carácter '{c}' desde estado {est_actual}.")
                    break

            if longitud_valida > 0:
                lexema = cadena[inicio : inicio + longitud_valida]
                resultados[lexema] = token_valido 

                print(f"*** Lexema Encontrado: '{lexema}' (Token {token_valido}) ***")
                
                inicio += longitud_valida
            else:
                # No se encontró ninguna coincidencia válida
                print(f"Error Léxico! Carácter no reconocido en posición {inicio}: '{cadena[inicio]}'")
                print("El AFD no pudo formar un lexema válido con el carácter actual.")
                resultados[cadena[inicio]] = "ERROR"
                inicio += 1

        return resultados