import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from AFN import AFN, EPSILON
from AFD import AFD
from AnalizadorLexico import AnalizadorLexico

# Definimos una lista de los AFN y AFD que se van creando
afns = []
afds = []

# Funciones adicionales necesarias
def actualizarContador(cont_AFN):
    cont_AFN.set(f"Número total de AFN's: {len(afns)}")

def actualizarContador2(cont_AFD):
    cont_AFD.set(f"Número total de AFD's: {len(afds)}")


def obtener_indice(entry):
    if entry is None:
        messagebox.showerror("Error!", "No se ha detectado ningún Entry.")

    raw = entry.get().strip()
    if raw == "":
        messagebox.showerror("Error!", "El campo esta vacío. Ingrese un número válido.")
        entry.focus_set()
        return None

    if not raw.isdigit():
        messagebox.showerror("Error!", f"'{raw}' no es un número valido.")
        entry.focus_set()
        return None

    num = int(raw)

    if num < 1 or num > len(afns):
        messagebox.showerror("Error!", f"No existe un AFN con el numero {num}.")
        entry.focus_set()
        return None
    
    entry.delete(0, tk.END)

    return num

def imprimir_afn(afn, log_fun):
    log_fun("\n=== AFN RESULTANTE ===")
    log_fun(f"Estados Totales: {len(afn.Estados)}")
    log_fun(f"Estado Inicial: {afn.EdoInicial.IdEdo}")
    log_fun(f"Estados de Aceptación: {[e.IdEdo for e in afn.EdosAceptacion]}")
    log_fun(f"Alfabeto: {sorted(afn.Alfabeto)}")
    for e in sorted(afn.Estados, key=lambda x: x.IdEdo):
        log_fun(f" Estado {e.IdEdo} (Acept: {e.EdoAcept}):")
        for t in e.Transiciones:
            si = t.SimboloInf
            ss = t.SimboloSup
            dest = t.EdoDestino.IdEdo if t.EdoDestino is not None else None
            log_fun(f"   -> {si!r}-{ss!r} -> {dest}")
    log_fun("===============\n")

def imprimir_afd(lex, log_fun):
    afd = lex.Automata
    log_fun("\n=== AFD RESULTANTE ===")
    log_fun(f"Estados: {afd.NumEdos}")
    log_fun(f"Estado Inicial: {afd.EdoInicial}")
    log_fun(f"Estados de Aceptación: {afd.EdosAceptacion}")
    
    alfabeto_ordenado = sorted(afd.Alfabeto)
    log_fun(f"Alfabeto: {alfabeto_ordenado}\n")

    log_fun(f"* = Estado de Aceptación, > = Estado Inicial")
    log_fun("=== TABLA DE TRANSICIONES ===")

    # Definimos el ancho de las columnas
    col_estado_w = 6
    col_token_w = 8
    col_simbolo_w = 8

    # Encabezados
    header_parts = ["Edo".ljust(col_estado_w)]
    for s in alfabeto_ordenado:
         header_parts.append(s.center(col_simbolo_w))
    header_parts.append("TOKEN".ljust(col_token_w))
            
    header_str = f"| {' | '.join(header_parts)} |"
    separator = "=" * len(header_str)
            
    # Escribir encabezado
    log_fun(separator + "\n")
    log_fun(header_str + "\n")
    log_fun(separator + "\n")

    # Filas de transiciones
    for edo in afd.EdosAFD:
        if edo is None or edo.id == -1 or edo.id >= afd.NumEdos:
            continue
                
        # --- Columna ESTADO (Omitida para brevedad) ---
        simbolo_edo = ""
        if edo.id in afd.EdosAceptacion: 
            simbolo_edo = "*"
        if edo.id == afd.EdoInicial:
            simbolo_edo = ">"
                
        fila = [f"{simbolo_edo}{edo.id}".ljust(col_estado_w)]
        
        # --- Columnas de TRANSICIONES (Alfabeto) (Omitida para brevedad) ---
        for simbolo_char in alfabeto_ordenado:
            idx = ord(simbolo_char)
            destino = -1 # Trampa
                    
            if idx < len(edo.transAFD):
                destino = edo.transAFD[idx]
                    
            destino_str = str(destino) if destino != -1 else "-"
            fila.append(destino_str.center(col_simbolo_w))
                
        token = getattr(edo, 'Token', -1)    
        token_val = str(token) if token != -1 else "-"  
        fila.append(token_val.ljust(col_token_w))
                
        # Escribir la fila
        log_fun(f"| {' | '.join(fila)} |\n")

    log_fun(separator + "\n")
    log_fun(f"* = Estado de Aceptación, > = Estado Inicial\n")
    
    log_fun("==========================\n")

def guardarArchivo(afd_entry, log_fun, afds):
    if afd_entry is None:
        messagebox.showerror("Error!", "No se ha detectado ninguna entrada en el AFD.")
        return

    raw = afd_entry.get().strip()

    if raw == "":
        messagebox.showerror("Error!", "El campo está vacío. Ingrese un número válido.")
        afd_entry.focus_set()
        return None

    if not raw.isdigit():
        messagebox.showerror("Error!", f"'{raw}' no es un número válido.")
        afd_entry.focus_set()
        return None

    num = int(raw)
    
    if not afds or num < 1 or num > len(afds):
        messagebox.showerror("Error", f"No existe un AFD con el número {num} o la lista de AFDs está vacía.")
        afd_entry.focus_set()
        return None
    
    afd_entry.delete(0, tk.END)
    
    lex = afds[num - 1]
    afdG = lex.Automata 

    ruta = filedialog.asksaveasfilename(
        defaultextension=".txt",
        initialfile="afd_r.txt",
        title="Guardar AFD como",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )

    if not ruta:
        messagebox.showerror("Error!", "Guardado cancelado por el usuario.")
        log_fun("Operación cancelada.\n")
        return

    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            # Escribir los estados como numeros
            archivo.write(" ".join(str(i) for i in range(afdG.NumEdos)) + "\n")
            archivo.write(str(afdG.EdoInicial) + "\n")
            archivo.write(" ".join(str(i) for i in afdG.EdosAceptacion) + "\n")
            archivo.write(" ".join(sorted(afdG.Alfabeto)) + "\n")

            # Tabla de transicion
            for edo in afdG.EdosAFD:
                if edo is None or edo.id == -1 or edo.id >= afdG.NumEdos:
                    continue
                
                fila_e = []

                for simb in sorted(afdG.Alfabeto):
                    idx = ord(simb)
                    destino = -1

                    if idx < len(edo.transAFD):
                        destino = edo.transAFD[idx]

                    destino_str = str(destino) if destino != -1 else "-"

                    fila_e.append(destino_str)

                token = getattr(edo, 'Token', -1)
                token_val = str(token) if token != -1 else "-"

                fila_e.append(token_val)

                archivo.write(" ".join(fila_e) + "\n")
            
            messagebox.showinfo("Felicidades!", f"AFD guardado correctamente en: {ruta}\n")

            log_fun("\n==========================")
            log_fun(f"AFD {num} guardado correctamente en {ruta}")
            log_fun("==========================\n")
            
    except Exception as e:
        messagebox.showerror("Error!", "No se ha podido guardar el AFD.")
        log_fun(f"Error! {e}.")

def seleccionarAFD(ruta, log_fun):
    r = filedialog.askopenfilename(
        defaultextension=".txt",
        title="Seleccionar un AFD",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )

    if r:
        ruta.set(r)
        log_fun("\n==========================")
        log_fun(f"Archivo cargado desde: {r}")
        log_fun("==========================\n")
    else:
        messagebox.showerror("Error1", "La selección del AFD no es válida.")
        ruta.set("")
        return

def probarAFD(ruta, cad, log_fun):
    if not ruta:
        messagebox.showerror("Error!", "El archivo seleccionado no es válido.")
        log_fun("Operación cancelada.\n")
        return
    
    if cad is None:
        messagebox.showerror("Error!", "No se ha detectado ninguna entrada en el AFD.")
        return

    rutaArchivo = ruta.get().strip()
    cad = cad.get().strip()

    if cad == "":
        messagebox.showerror("Error!", "El campo está vacío. Ingrese un número válido.")
        cad.focus_set()
        return None
    
    lex = AnalizadorLexico()          # Nuevo
    lex.CargarArchivoAFD(rutaArchivo) # Cargar el AFD desde archivo
    lex.SetSigma(cad)                 # Inicializamos la cadena a analizar
    res = []                          # Analizamos la cadena
    while True:
        token = lex.yylex()
        if token == -1:
            break
        res.append((lex.yytext, token))


    if(res == -1):
        messagebox.showerror("Error!", f"No se han encontrado lexemas válidos para la cadena {cad}.")
    else:
        log_fun("\n==========================")
        log_fun(f"Lexemas encontrados en {cad}")
        
        for x, y in res:
            log_fun(f"{x} : {y}")

        log_fun("==========================\n")


# Opciones del AFN
def crearBasico1(entry_widget, token, log_fun, cont_AFN):
    print("Opcion seleccionada de Crear Basico\n")

    caracter = entry_widget.get().strip()
    entry_widget.delete(0, tk.END)

    token_raw = token.get().strip()
    token.delete(0, tk.END)

    if not token_raw.isdigit():
        messagebox.showerror("Error!", "El token debe ser un número.")
        token.focus_set()

    token_val = int(token_raw)

    print(f"Caracter recibido: {caracter}\n")
    print(f"Token asignado: {token_val}\n")

    if not caracter:
        messagebox.showerror("Error!", "Debes ingresar al menos un caracter para crear un AFN básico")
        return

    if len(caracter) > 1:
        messagebox.showerror("Error!", "Se ha detectado más de un caracter, se tomará solo el primero.")
        caracter = caracter[0]
        
    afn1 = AFN()
    afn1.CrearBasicoUno(caracter, token_val)
    afns.append(afn1)

    actualizarContador(cont_AFN)

    log_fun(f"AFN Basico 1 creado para el caracter: '{caracter}'")
    imprimir_afn(afn1, log_fun)

    print(f"Numero de AFN's totales {len(afns)}\n")

def crearBasico2(entry_widget1, entry_widget2, token, log_fun, cont_AFN):
    print("Opcion seleccionada de Crear Basico\n")

    caracter1 = entry_widget1.get().strip()
    caracter2 = entry_widget2.get().strip()
    entry_widget1.delete(0, tk.END)
    entry_widget2.delete(0, tk.END)

    token_raw = token.get().strip()
    token.delete(0, tk.END)

    if not token_raw.isdigit():
        messagebox.showerror("Error!", "El token debe ser un número.")
        token.focus_set()

    token_val = int(token_raw)

    print(f"Caracteres recibidos: {caracter1, caracter2}\n")
    print(f"Token asignado: {token_val}\n")

    if(not caracter1) and (not caracter2):
        messagebox.showerror("Error!", "Debes ingresar al menos un caracter para crear un AFN básico.")
        entry_widget1.focus_set()
        return
    
    if (len(caracter1) > 1) or (len(caracter2) > 1):
        messagebox.showinfo("Error!", "Se ha detectado más de un caracter, se tomará sólo el primero.")
        caracter1 = caracter1[0]
        caracter2 = caracter2[0]
        
    afn1 = AFN()
    afn1.CrearBasicoDos(caracter1, caracter2, token_val)
    afns.append(afn1)

    actualizarContador(cont_AFN)

    log_fun(f"AFN Básico 2 creado para los caracteres: '{caracter1} - {caracter2}'")
    imprimir_afn(afn1, log_fun)

    print(f"Número de AFN's totales {len(afns)}\n")

def unirAFN(afn1, afn2, log_fun, cont_AFN):
    print("Opcion seleccionada unir AFN\n")

    if(len(afns) < 2):
        messagebox.showerror("Error!", "Se necesitan al menos 2 AFN's para realizar esta operación.")
        return

    num1 = obtener_indice(afn1)
    num2 = obtener_indice(afn2)

    if num1 is None:
        messagebox.showerror("Error!", "Ingrese el número del AFN 1.")
        afn1.focus_set()
        return

    if num2 is None:
        messagebox.showerror("Error!", "Ingrese el número del AFN 2.")
        afn2.focus_set()
        return

    if num1 == num2:
        messagebox.showerror("Error!", "No se puede unir un AFN consigo mismo.")
        return

    a1 = afns[num1 - 1]
    a2 = afns[num2 - 1]

    a1.UnirAFN(a2)
    afns.pop(num2 - 1)

    actualizarContador(cont_AFN)

    log_fun(f"Se ha creado la unión entre los AFN's {num1} y {num2}.")
    imprimir_afn(a1, log_fun)

def concatenarAFN(afn1, afn2, log_fun, cont_AFN):
    print("Opcion seleccionada concatenar AFN\n")

    if(len(afns) < 2):
        messagebox.showerror("Error!", "Se necesitan al menos 2 AFN's para realizar esta operación.")
        log_fun("Operación cancelada.\n")
        return

    num1 = obtener_indice(afn1)
    num2 = obtener_indice(afn2)

    if(num1 is None) or (num2 is None):
        return

    if(num1 == num2):
        messagebox.showerror("Error!", "No se puede concatenar el AFN consigo mismo.")
        return

    a1 = afns[num1 - 1]
    a2 = afns[num2 - 1]
    
    a1.ConcatenarAFN(a2)
    afns.pop(num2 - 1)

    actualizarContador(cont_AFN)

    log_fun(f"Se ha creado la concatenación entre los AFN's.")
    imprimir_afn(a1, log_fun)

def cerrPostiva(afn, log_fun):
    print("Opcion seleccionada cerradura positiva AFN\n")

    if(len(afns) < 1):
        messagebox.showerror("Error!", "No hay AFN's disponibles.")
        return
    
    num = obtener_indice(afn)

    if num is None:
        return
    
    a = afns[num - 1]
    
    a.CerraduraPositiva()
    log_fun(f"Se ha creado la cerradura positiva del AFN.")
    imprimir_afn(a, log_fun)

def cerrKleene(afn, log_fun):
    print("Opcion seleccionada cerradura de kleene AFN\n")

    if(len(afns) < 1):
        messagebox.showerror("Error!", "No hay AFN's disponibles.")
        return

    num = obtener_indice(afn)

    if num is None:
        return

    a = afns[num - 1]
    
    a.CerraduraKleene()
    log_fun(f"Se ha creado la cerradura de Kleene del AFN.")
    imprimir_afn(a, log_fun)

def opcional(afn, log_fun):
    print("Opcion seleccionada opcional de un AFN\n")

    if(len(afns) < 1):
        messagebox.showerror("Error!", "No hay AFN's disponibles.")
        return

    num = obtener_indice(afn)

    if num is None:
        return

    a = afns[num - 1]
    
    a.Opcional()
    log_fun(f"Se ha creado la operación opcional del AFN.")
    imprimir_afn(a, log_fun)

# Funciones para hacer los AFD
def unirAFNS(num_afns, log_fun, cont_AFN):
    if num_afns is None:
        log_fun("Error! No se ha detectado ningun AFN")
        return 

    raw = num_afns.get().strip()
    print("Entry obtenido ", raw)
    if raw == "":
        messagebox.showerror("Error!", "El campo esta vacio. Ingrese un numero valido.")
        num_afns.focus_set()
        return

    try:
        indices = sorted(set(int(x.strip()) - 1 for x in raw.split(",")))
    except ValueError:
        messagebox.showerror("Error!", "Solo se permiten números separados por comas y sin espacios.")
        num_afns.focus_set()
        return
    
    print("Indices obtenidos ", indices)
    for i in indices:
        if (i < 0) or (i >= len(afns)):
            messagebox.showerror("Error!", f"El indice {i + 1} no es válido.")
            num_afns.focus_set()
            return
    
    if len(indices) < 2:
        messagebox.showerror("Error! Se deben seleccionar al menos 2 AFN's para unir.")
        num_afns.focus_set()
        return
    
    i_base = indices[0]
    base_afn = afns[i_base]

    # Unir los demás AFNs al base
    for i in reversed(indices[1:]):
        afn_a_unir = afns[i]
        base_afn.UnirAFNs([afn_a_unir])
        afns.pop(i)

    # Actualizar
    actualizarContador(cont_AFN)
    
    log_fun(f"Unión completada! El AFN {i_base + 1} ahora contiene la unión.")
    imprimir_afn(base_afn, log_fun)

def hacerAFD(afn, log_fun, cont_AFD):
    print("Opcion seleccionada convertir a AFD\n")

    num = obtener_indice(afn)

    a = afns[num - 1]

    afd = a.ConvertirAAFD()
    lex = AnalizadorLexico()
    lex.Automata = afd
    afds.append(lex)

    afns.pop(num - 1)
    actualizarContador2(cont_AFD)

    log_fun(f"Se ha creado el AFD a partir del AFN {num}.")
    imprimir_afd(lex, log_fun)


def main():
    # Definición de la ventana principal en Tkinter
    ventana = tk.Tk()
    ventana.title("Analizador Léxico")
    ventana.geometry("900x500")
    ventana.configure(bg = "white")

    style = ttk.Style()
    style.configure("TButton", background = "#f8f8f8", relief = "flat")
    style.map("TButton", background=[("active", "#e6e6e6")])
    style.configure("TNotebook", background="white")
    style.configure("TFrame", background="white")
    style.configure("TLabelframe", background="white")

    # Crear paneles
    paned_w = ttk.PanedWindow(ventana, orient = tk.HORIZONTAL)
    paned_w.pack(fill = "both", expand = True, padx = 10, pady = 10)
    
    panel_c = ttk.Frame(paned_w)
    panel_r = ttk.Frame(paned_w)

    paned_w.add(panel_c, weight = 3)
    paned_w.add(panel_r, weight = 1)

    panel_i = ttk.Frame(panel_c)
    panel_i.pack(fill = "x", pady = 5)

    # Contenedor de pestañas de panel_r
    tk.Label(panel_r, text = "Historial", fg = "black", bg = "white", font = ("Arial", 10, "bold")).pack(pady = 5)
    text_r = tk.Text(panel_r, wrap="none", height = 20, width = 50, bg="#fafafa", relief="flat")
    scrollbar_y = tk.Scrollbar(panel_r, orient="vertical", command = text_r.yview)
    text_r.config(yscrollcommand = scrollbar_y.set)
    scrollbar_x = tk.Scrollbar(panel_r, orient="horizontal", command=text_r.xview)
    text_r.config(xscrollcommand=scrollbar_x.set)

    scrollbar_y.pack(side = tk.RIGHT, fill = tk.Y)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    text_r.pack(fill = "both", expand = True, padx = 5, pady = 5)

    def log_resultado(mensaje):
        text_r.insert(tk.END, mensaje + "\n")
        text_r.see(tk.END) 

    # Contenedor de pestañas de panel_c
    notebookP = ttk.Notebook(panel_c)
    notebookP.pack(expand=True, fill="both", padx = 10, pady = 10)

    pestaña1 = tk.Frame(notebookP, bg = "lavender")
    pestaña2 = tk.Frame(notebookP, bg = "thistle1")
    pestaña3 = tk.Frame(notebookP, bg = "lightblue")
    pestaña4 = tk.Frame(notebookP, bg = "ivory2")

    notebookP.add(pestaña1, text="AFN")
    notebookP.add(pestaña2, text="Convertir a un AFD")
    notebookP.add(pestaña3, text="Descargar")
    notebookP.add(pestaña4, text="Probar AFD")

    # Contador de los AFD's
    cont_AFD = tk.StringVar()
    cont_AFD.set(f"Número total de AFD's: {len(afds)}")
    tk.Label(panel_i, textvariable = cont_AFD, font=("Arial", 9, "bold"), fg = "snow4").pack(side = tk.LEFT, padx = 20)

    # Contador de los AFN's
    cont_AFN = tk.StringVar()
    cont_AFN.set(f"Número total de AFN's: {len(afns)}")
    tk.Label(panel_i, textvariable = cont_AFN, font=("Arial", 9, "bold"), fg = "snow4").pack(side = tk.LEFT, padx = 20)


    # Pestaña 2
    notebookAFD = ttk.Notebook(pestaña2)
    notebookAFD.pack(expand = True, fill = "both", padx = 10, pady = 10)
    sub1AFD = tk.Frame(notebookAFD, bg = "thistle1") # Unir AFNS
    sub2AFD = tk.Frame(notebookAFD, bg = "thistle1") # Hacer AFD

    notebookAFD.add(sub1AFD, text = "Unir AFN's")
    notebookAFD.add(sub2AFD, text = "Hacer AFD")

    # Unir AFN's
    tk.Label(sub1AFD, text=" Unir AFN's ", font=("Arial", 11, "bold"), bg="thistle1").pack(pady=20)
    tk.Label(sub1AFD, text="Seleccione los AFN's a Unir (índices separados por comas sin espacios):", bg="thistle1").pack()
    num_AFNS = tk.Entry(sub1AFD, width=45, justify='center')
    num_AFNS.pack(pady=5)
    tk.Button(sub1AFD, text="   Ejecutar   ", command = lambda: unirAFNS(num_AFNS, log_resultado, cont_AFN)).pack(pady=10)

    tk.Label(sub2AFD, text="Convertir a un AFD", font=("Arial", 11, "bold"), bg="thistle1").pack(pady=20)
    tk.Label(sub2AFD, text="Ingrese el número del AFN:", bg="thistle1").pack()
    num_AFN = tk.Entry(sub2AFD, width=5, justify='center')
    num_AFN.pack(pady=5)
    tk.Button(sub2AFD, text="   Ejecutar   ", command = lambda: hacerAFD(num_AFN, log_resultado, cont_AFN)).pack(pady=10)


    # Pestaña 3
    tk.Label(pestaña3, text="Descargar AFD a Txt", font=("Arial", 11, "bold"), bg="lightblue").pack(pady=20)
    tk.Label(pestaña3, text="Ingrese el número del AFD:", bg="lightblue").pack()
    num_AFD = tk.Entry(pestaña3, width=5, justify='center')
    num_AFD.pack(pady=5)
    tk.Button(pestaña3, text="   Ejecutar   ", command=lambda: guardarArchivo(num_AFD, log_resultado, afds)).pack(pady=10)


    # Pestaña 4
    tk.Label(pestaña4, text="Probar AFD desde un archivo", font=("Arial", 11, "bold"), bg="ivory2").pack(pady=20)
    tk.Label(pestaña4, text="Seleccione el archivo del AFD (.txt)", bg="ivory2").pack()

    ruta = tk.StringVar(value="")
    tk.Label(pestaña4, textvariable=ruta, bg="ivory2", fg="slate gray", wraplength=350, font=("Arial", 8, "italic")).pack(pady=5)
    tk.Button(pestaña4, text="   Seleccionar Archivo AFD   ", command=lambda: seleccionarAFD(ruta, log_resultado)).pack(pady=10)

    tk.Label(pestaña4, text="Ingresa una cadena de prueba para el AFD:", bg="ivory2").pack()
    cad = tk.Entry(pestaña4, width=30, justify="center")
    cad.pack(pady=5)
    tk.Button(pestaña4, text="   Ejecutar   ", command=lambda: probarAFD(ruta, cad, log_resultado)).pack(pady=10)
    

    # Subpestañas del AFN (Pestaña 1)
    notebookAFN = ttk.Notebook(pestaña1)
    notebookAFN.pack(expand = True, fill = "both", padx = 10, pady = 10)

    sub1 = tk.Frame(notebookAFN, bg="lavender") # Crear basico 1
    sub2 = tk.Frame(notebookAFN, bg="lavender") # Crear basico 2
    sub3 = tk.Frame(notebookAFN, bg="lavender") # Unir (or)
    sub4 = tk.Frame(notebookAFN, bg="lavender") # Concatenar (and)
    sub5 = tk.Frame(notebookAFN, bg="lavender") # Cerradura +
    sub6 = tk.Frame(notebookAFN, bg="lavender") # Cerradura *
    sub7 = tk.Frame(notebookAFN, bg="lavender") # Opcional ?

    notebookAFN.add(sub1, text="Crear B1")
    notebookAFN.add(sub2, text="Crear B2")
    notebookAFN.add(sub3, text="Unir")
    notebookAFN.add(sub4, text="Concatenar")
    notebookAFN.add(sub5, text="Cerradura +")
    notebookAFN.add(sub6, text="Cerradura *")
    notebookAFN.add(sub7, text="Opcional ?")

    # AFN Basico 1
    tk.Label(sub1, text=" AFN Basico 1 ", font=("Arial", 11, "bold"), bg="lavender").pack(pady=20)
    tk.Label(sub1, text="Ingrese un caracter:", bg="lavender").pack()
    ec1 = tk.Entry(sub1, width=5, justify='center')
    ec1.pack(pady=5)
    tk.Label(sub1, text="Ingrese el token:", bg="lavender").pack()
    tk1 = tk.Entry(sub1, width=5, justify='center')
    tk1.pack(pady=5)
    tk.Button(sub1, text="   Ejecutar   ", command=lambda: crearBasico1(ec1, tk1, log_resultado, cont_AFN)).pack(pady=15)

    # AFN Basico 2
    tk.Label(sub2, text=" AFN Basico 2 ", font=("Arial", 11, "bold"), bg="lavender").pack(pady=20)
    tk.Label(sub2, text="Ingrese un caracter:", bg="lavender").pack()
    ec2 = tk.Entry(sub2, width=5, justify='center')
    ec2.pack(pady=5)
    tk.Label(sub2, text="Ingrese otro caracter:", bg="lavender").pack()
    ec3 = tk.Entry(sub2, width=5, justify='center')
    ec3.pack(pady=5)
    tk.Label(sub2, text="Ingrese el token:", bg="lavender").pack()
    tk2 = tk.Entry(sub2, width=5, justify='center')
    tk2.pack(pady=5)
    tk.Button(sub2, text="   Ejecutar   ", command=lambda: crearBasico2(ec2, ec3, tk2, log_resultado, cont_AFN)).pack(pady=10)

    # AFN Unir
    tk.Label(sub3, text="Unir AFN's").pack(pady=20)
    tk.Label(sub3, text="Ingrese el número del AFN 1:").pack()
    ec4 = tk.Entry(sub3, width=5, justify='center')
    ec4.pack(pady=5)
    tk.Label(sub3, text="Ingrese el número del AFN 2:").pack()
    ec5 = tk.Entry(sub3, width=5, justify='center')
    ec5.pack(pady=5)
    tk.Button(sub3, text="Ejecutar", command=lambda: unirAFN(ec4, ec5, log_resultado, cont_AFN)).pack(pady=10)

    # AFN Concatenar
    tk.Label(sub4, text="Concatenar AFN's").pack(pady=20)
    tk.Label(sub4, text="Ingrese el número del AFN 1:").pack()
    ec6 = tk.Entry(sub4, width=5, justify='center')
    ec6.pack(pady=5)
    tk.Label(sub4, text="Ingrese el número del AFN 2:").pack()
    ec7 = tk.Entry(sub4, width=5, justify='center')
    ec7.pack(pady=5)
    tk.Button(sub4, text="Ejecutar", command=lambda: concatenarAFN(ec6, ec7, log_resultado, cont_AFN)).pack(pady=10)

    # AFN Cerradura Positiva
    tk.Label(sub5, text="Cerradura Positiva").pack(pady=20)
    tk.Label(sub5, text="Ingrese el numero del AFN:").pack()
    ec8 = tk.Entry(sub5, width=5, justify='center')
    ec8.pack(pady=5)
    tk.Button(sub5, text="Ejecutar", command=lambda: cerrPostiva(ec8, log_resultado)).pack(pady=10)

    # AFN Cerradura de Kleene
    tk.Label(sub6, text="Cerradura de Kleene").pack(pady=20)
    tk.Label(sub6, text="Ingrese el número del AFN:").pack()
    ec9 = tk.Entry(sub6, width=5, justify='center')
    ec9.pack(pady=5)
    tk.Button(sub6, text="Ejecutar", command=lambda: cerrKleene(ec9, log_resultado)).pack(pady=10)

    # AFN Opcional
    tk.Label(sub7, text="Opcional").pack(pady=20)
    tk.Label(sub7, text="Ingrese el número del AFN:").pack()
    ec10 = tk.Entry(sub7, width=5, justify='center')
    ec10.pack(pady=5)
    tk.Button(sub7, text="Ejecutar", command=lambda: opcional(ec10, log_resultado)).pack(pady=10)


    ventana.mainloop()


if __name__ == "__main__":
    main()