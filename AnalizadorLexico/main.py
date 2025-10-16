import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from AFN import AFN, EPSILON

# Definimos una lista de los AFN y AFD que se van creando
afns = []
afds = []

# Funciones adicionales necesarias
def actualizarContador(cont_AFN):
    cont_AFN.set(f"Numero total de AFN's: {len(afns)}")

def actualizarContador2(cont_AFD):
    cont_AFD.set(f"Numero total de AFD's: {len(afds)}")


def obtener_indice(entry, log_fun):
    if entry is None:
        log_fun("Error! No se ha detectado ningun Entry.")

    raw = entry.get().strip()
    if raw == "":
        log_fun("Error! El campo esta vacio. Ingrese un numero valido.")
        entry.focus_set()
        return None

    if not raw.isdigit():
        log_fun(f"Error! '{raw}' no es un número valido.")
        entry.focus_set()
        return None

    num = int(raw)

    if num < 1 or num > len(afns):
        log_fun(f"Error: no existe un AFN con el numero {num}.")
        entry.focus_set()
        return None
    
    entry.delete(0, tk.END)

    return num

def imprimir_afn(afn, log_fun):
    log_fun("\n=== AFN ===\n")
    log_fun(f"Estados totales: {len(afn.Estados)}")
    log_fun(f"Estado inicial: {afn.EdoInicial.IdEdo}")
    log_fun(f"Estados de aceptación: {[e.IdEdo for e in afn.EdosAceptacion]}")
    log_fun(f"Alfabeto: {sorted(afn.Alfabeto)}")
    for e in sorted(afn.Estados, key=lambda x: x.IdEdo):
        log_fun(f" Estado {e.IdEdo} (Acept: {e.EdoAcept}):")
        for t in e.Transiciones:
            si = t.SimboloInf
            ss = t.SimboloSup
            dest = t.EdoDestino.IdEdo if t.EdoDestino is not None else None
            log_fun(f"   -> {si!r}-{ss!r} -> {dest}")
    log_fun("\n===============\n")

def imprimir_afd(afd, log_fun):
    log_fun("\n=== AFD RESULTANTE ===\n")
    log_fun(f"Estados totales: {afd.NumEdos}")
    log_fun(f"Estado inicial: {afd.EdoInicial}")
    log_fun(f"Estados de aceptación: {afd.EdosAceptacion}")
    
    alfabeto_ordenado = sorted(afd.Alfabeto)
    log_fun(f"Alfabeto: {alfabeto_ordenado}\n")

    log_fun(f"* = Estado de Aceptación, > = Estado Inicial")
    log_fun("\n==========================\n")

def guardarArchivo(afd_entry, log_fun, afds):
    if afd_entry is None:
        log_fun("Error! No se ha detectado ninguna entrada en el AFD.")
        return

    raw = afd_entry.get().strip()

    if raw == "":
        log_fun("Error! El campo esta vacio. Ingrese un numero valido.")
        afd_entry.focus_set()
        return None

    if not raw.isdigit():
        log_fun(f"Error! '{raw}' no es un número valido.")
        afd_entry.focus_set()
        return None

    num = int(raw)
    
    # Manejo del caso donde 'afds' no existe o está vacío.
    if not afds or num < 1 or num > len(afds):
        log_fun(f"Error: no existe un AFD con el numero {num} o la lista de AFDs está vacía.")
        afd_entry.focus_set()
        return None
    
    afd_entry.delete(0, tk.END)
    
    afdG = afds[num - 1] 

    ruta = filedialog.asksaveasfilename(
        defaultextension=".txt",
        initialfile="afd_resultado_tabla.txt",
        title="Guardar AFD como",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )

    if not ruta:
        log_fun("Error! Guardado cancelado por el usuario.")
        return

    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            # 1. Información General
            archivo.write("=== AFD GENERADO ===\n")
            archivo.write(f"Estados: {afdG.NumEdos}\n")
            archivo.write(f"Inicial: {afdG.EdoInicial}\n")
            archivo.write(f"Aceptacion: {' '.join(str(e) for e in afdG.EdosAceptacion)}\n")
            
            alfabeto_ordenado = sorted(afdG.Alfabeto)
            archivo.write(f"Alfabeto: {alfabeto_ordenado}\n\n") 

            #Tabla de transiciones
            archivo.write("=== TABLA DE TRANSICIONES ===\n")
            
            # Determinar el ancho máximo para los estados y destinos
            max_state_len = max(len(str(edo.id)) for edo in afdG.EdosAFD if edo and edo.id != -1) if afdG.EdosAFD else 2
            max_token_len = max(len(str(getattr(edo, 'Token', '-1'))) for edo in afdG.EdosAFD if edo and edo.id != -1) if afdG.EdosAFD else 2
            
            # El ancho de la columna debe ser al menos 3 para cubrir los símbolos, estados y los guiones (-)
            col_w = max(3, max_state_len, max_token_len)
            
            # Construir la primera fila (encabezado de transiciones)
            header_symbols = ""
            for s in alfabeto_ordenado:
                # Usar center() para que los símbolos queden centrados en la columna
                header_symbols += s.center(col_w) + " "
            
            # Escribir el encabezado del alfabeto
            # Se añade un espacio antes para alinear con la primera columna de la tabla real (la de los estados)
            archivo.write(" " * col_w + " " + header_symbols.rstrip() + "\n")
            
            # 2. Cuerpo de la matriz
            for edo in afdG.EdosAFD:
                if edo is None or edo.id == -1 or edo.id >= afdG.NumEdos:
                    continue
                
                # --- Columna ESTADO ---
                # Escribir el ID del estado (sin el símbolo > o *)
                # Se utiliza ljust() para asegurar la alineación de la primera columna
                fila_str = str(edo.id).ljust(col_w) + " "
                
                # --- Columnas de TRANSICIONES (Alfabeto) ---
                for simbolo_char in alfabeto_ordenado:
                    idx = ord(simbolo_char)
                    destino = -1 # Trampa
                    
                    if idx < len(edo.transAFD):
                        destino = edo.transAFD[idx]
                    
                    # El destino puede ser un solo estado o una lista/conjunto de estados (para NFA, aunque aquí es AFD)
                    # Usamos '-' si el destino es -1 (trampa)
                    destino_str = str(destino) if destino != -1 else "-"
                    
                    # El destino debe ser centrado en la columna
                    fila_str += destino_str.center(col_w) + " "
                
                # --- Columna TOKEN ---
                token = getattr(edo, 'Token', -1)
                token_val = str(token) if token != -1 else "-"
                
                # El token debe ser centrado o alineado para mantener el formato de matriz
                fila_str += token_val.center(col_w)
                
                # Escribir la fila
                archivo.write(fila_str + "\n")
            
            archivo.write("\n")
            archivo.write("\n==========================\n")
            
            messagebox.showinfo("Felicidades!", f"AFD guardado correctamente en: {ruta}\n")
            log_fun(f"AFD {num} guardado correctamente en {ruta}")
            
    except Exception as e:
        messagebox.showinfo("Error!", f"No se ha podido guardar el AFD.\n")
        log_fun(f"Error! {e}.")


""" Comentando mi hermosa creacion porque a la señorita no le gusta :c
def guardarArchivo(afd_entry, log_fun):
    if afd_entry is None:
        log_fun("Error! No se ha detectado ninguna entrada en el AFD.")
        return

    raw = afd_entry.get().strip()

    if raw == "":
        log_fun("Error! El campo esta vacio. Ingrese un numero valido.")
        afd_entry.focus_set()
        return None

    if not raw.isdigit():
        log_fun(f"Error! '{raw}' no es un número valido.")
        afd_entry.focus_set()
        return None

    num = int(raw)
    
    if num < 1 or num > len(afds):
        log_fun(f"Error: no existe un AFD con el numero {num}.")
        afd_entry.focus_set()
        return None
    
    afd_entry.delete(0, tk.END)
    
    afdG = afds[num - 1] # Obtener el objeto AFD (índice 0-based)

    ruta = filedialog.asksaveasfilename(
        defaultextension=".txt",
        initialfile="afd_resultado_tabla.txt",
        title="Guardar AFD como",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )

    if not ruta:
        log_fun("Error! Guardado cancelado por el usuario.")
        return

    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            # 1. Información General
            archivo.write("=== AFD GENERADO ===\n")
            archivo.write(f"Estados: {afdG.NumEdos}\n")
            archivo.write(f"Inicial: {afdG.EdoInicial}\n")
            archivo.write(f"Aceptacion: {' '.join(str(e) for e in afdG.EdosAceptacion)}\n")
            
            alfabeto_ordenado = sorted(afdG.Alfabeto)
            archivo.write(f"Alfabeto: {alfabeto_ordenado}\n\n") 

            #Tabla de transiciones
            archivo.write("=== TABLA DE TRANSICIONES ===\n")

            # Definir el ancho de las columnas
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
            archivo.write(separator + "\n")
            archivo.write(header_str + "\n")
            archivo.write(separator + "\n")

            # Filas de transiciones
            for edo in afdG.EdosAFD:
                if edo is None or edo.id == -1 or edo.id >= afdG.NumEdos:
                    continue
                
                # --- Columna ESTADO (Omitida para brevedad) ---
                simbolo_edo = ""
                if edo.id in afdG.EdosAceptacion: 
                    simbolo_edo = "*"
                if edo.id == afdG.EdoInicial:
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
                archivo.write(f"| {' | '.join(fila)} |\n")

            archivo.write(separator + "\n")
            archivo.write(f"* = Estado de Aceptación, > = Estado Inicial\n")
            archivo.write("\n")
            
            archivo.write("\n==========================\n")
            
            messagebox.showinfo("Felicidades!", f"AFD guardado correctamente en: {ruta}\n")
            log_fun(f"AFD {num} guardado correctamente en {ruta}")
            
    except Exception as e:
        messagebox.showinfo("Error!", f"No se ha podido guardar el AFD.\n")
        log_fun(f"Error! {e}.")
"""
# Opciones del AFN
def crearBasico1(entry_widget, log_fun, cont_AFN):
    print("Opcion seleccionada de Crear Basico\n")

    caracter = entry_widget.get().strip()
    entry_widget.delete(0, tk.END)

    token_val = (len(afns)  + 1) * 10

    print(f"Caracter recibido: {caracter}\n")
    print(f"Token asignado automáticamente: {token_val}\n")

    if not caracter:
        log_fun("Error! Debes ingresar al menos un caracter para crear un AFN basico")
        return

    if len(caracter) > 1:
        log_fun(f"Error! Se ha detectado mas de un caracter, se tomara solo el primero.\n")
        caracter = caracter[0]
        
    afn1 = AFN()
    afn1.CrearBasicoUno(caracter, token_val)
    afns.append(afn1)

    actualizarContador(cont_AFN)

    log_fun(f"AFN Basico 1 creado para el caracter: '{caracter}'")
    imprimir_afn(afn1, log_fun)

    print(f"Numero de AFN's totales {len(afns)}\n")

def crearBasico2(entry_widget1, entry_widget2, log_fun, cont_AFN):
    print("Opcion seleccionada de Crear Basico\n")

    caracter1 = entry_widget1.get().strip()
    caracter2 = entry_widget2.get().strip()
    entry_widget1.delete(0, tk.END)
    entry_widget2.delete(0, tk.END)

    token_val = (len(afns) + 1) * 10

    print(f"Caracteres recibidos: {caracter1, caracter2}\n")
    print(f"Token asignado automáticamente: {token_val}\n")

    if(not caracter1) and (not caracter2):
        log_fun(f"Error! Debes ingresar al menos un caracter para crear un AFN basico")
        return

    
    if (len(caracter1) > 1) or (len(caracter2) > 1):
        log_fun(f"Error! Se ha detectado mas de un caracter, se tomara solo el primero.\n")
        caracter1 = caracter1[0]
        caracter2 = caracter2[0]
        
    afn1 = AFN()
    afn1.CrearBasicoDos(caracter1, caracter2, token_val)
    afns.append(afn1)

    actualizarContador(cont_AFN)

    log_fun(f"AFN Basico 2 creado para los caracteres: '{caracter1} - {caracter2}'")
    imprimir_afn(afn1, log_fun)

    print(f"Numero de AFN's totales {len(afns)}\n")

def concatenarAFN(afn1, afn2, log_fun, cont_AFN):
    print("Opcion seleccionada concatenar AFN\n")

    if(len(afns) < 2):
        log_fun("Error! Se necesitan al menos 2 AFN's para realizar esta operacion.")
        return

    num1 = obtener_indice(afn1, log_fun)
    num2 = obtener_indice(afn2, log_fun)

    if(num1 is None) or (num2 is None):
        return

    if(num1 == num2):
        log_fun("Error! No se puede concatenar el AFN consigo mismo.")
        return

    a1 = afns[num1 - 1]
    a2 = afns[num2 - 1]
    
    a1.ConcatenarAFN(a2)
    afns.pop(num2 - 1)

    actualizarContador(cont_AFN)

    log_fun(f"Se ha creado la concatenacion entre los AFN's.")
    imprimir_afn(a1, log_fun)

def cerrPostiva(afn, log_fun):
    print("Opcion seleccionada cerradura positiva AFN\n")

    if(len(afns) < 1):
        log_fun("Error! No hay AFN's disponibles.")
        return
    
    num = obtener_indice(afn, log_fun)

    if num is None:
        return
    
    a = afns[num - 1]
    
    a.CerraduraPositiva()
    log_fun(f"Se ha creado la cerradura positiva del AFN.")
    imprimir_afn(a, log_fun)

def cerrKleene(afn, log_fun):
    print("Opcion seleccionada cerradura de kleene AFN\n")

    if(len(afns) < 1):
        log_fun("Error! No hay AFN's disponibles.")
        return

    num = obtener_indice(afn, log_fun)

    if num is None:
        return

    a = afns[num - 1]
    
    a.CerraduraKleene()
    log_fun(f"Se ha creado la cerradura de Kleene del AFN.")
    imprimir_afn(a, log_fun)

def opcional(afn, log_fun):
    print("Opcion seleccionada opcional de un AFN\n")

    if(len(afns) < 1):
        log_fun("Error! No hay AFN's disponibles.")
        return

    num = obtener_indice(afn, log_fun)

    if num is None:
        return

    a = afns[num - 1]
    
    a.Opcional()
    log_fun(f"Se ha creado la operacion opcional del AFN.")
    imprimir_afn(a, log_fun)

# Funciones para hacer los AFD
def unirAFNS(num_afns, log_fun, cont_AFN):
    if num_afns is None:
        log_fun("Error! No se ha detectado ningun AFN")
        return 

    raw = num_afns.get().strip()
    print("Entry obtenido ", raw)
    if raw == "":
        log_fun("Error! El campo esta vacio. Ingrese un numero valido.")
        num_afns.focus_set()
        return

    try:
        indices = sorted(set(int(x.strip()) - 1 for x in raw.split(",")))
    except ValueError:
        log_fun("Error! Solo se permiten numeros separados por comas y sin espacios.")
        num_afns.focus_set()
        return
    
    print("Indices obtenidos ", indices)
    for i in indices:
        if (i < 0) or (i >= len(afns)):
            log_fun(f"Error! El indice {i + 1} no es valido.")
            num_afns.focus_set()
            return
    
    if len(indices) < 2:
        log_fun("Error! Se deben seleccionar al menos 2 AFN's para unir.")
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
    
    log_fun(f"✅ Unión completada! AFN {i_base + 1} ahora contiene la unión.")
    imprimir_afn(base_afn, log_fun)

def hacerAFD(afn, log_fun, cont_AFD):
    print("Opcion seleccionada convertir a AFD\n")

    num = obtener_indice(afn, log_fun)

    a = afns[num - 1]

    afd = a.ConvertirAAFD()
    afds.append(afd)

    afns.pop(num - 1)
    actualizarContador2(cont_AFD)

    log_fun(f"Se ha creado el AFD a partir del AFN {num}.")
    imprimir_afd(afd, log_fun)



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
    text_r = tk.Text(panel_r, wrap = tk.WORD, height = 20, width = 50, bg="#fafafa", relief="flat")
    scrollbar = tk.Scrollbar(panel_r, command = text_r.yview)
    text_r.config(yscrollcommand = scrollbar.set)

    scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
    text_r.pack(fill = "both", expand = True, padx = 5, pady = 5)

    def log_resultado(mensaje):
        text_r.insert(tk.END, mensaje + "\n")
        text_r.see(tk.END) 

    # Contenedor de pestañas de panel_c
    notebookP = ttk.Notebook(panel_c)
    notebookP.pack(expand=True, fill="both", padx = 10, pady = 10)

    pestaña1 = tk.Frame(notebookP, bg="lavender")
    pestaña2 = tk.Frame(notebookP, bg="thistle1")
    pestaña3 = tk.Frame(notebookP, bg="lightblue")

    notebookP.add(pestaña1, text="AFN")
    notebookP.add(pestaña2, text="Convertir a un AFD")
    notebookP.add(pestaña3, text="Descargar")

    # Contador de los AFD's
    cont_AFD = tk.StringVar()
    cont_AFD.set(f"Numero total de AFD's: {len(afds)}")
    tk.Label(panel_i, textvariable = cont_AFD, font=("Arial", 9, "bold"), fg = "snow4").pack(side = tk.LEFT, padx = 20)

    # Contador de los AFN's
    cont_AFN = tk.StringVar()
    cont_AFN.set(f"Numero total de AFN's: {len(afns)}")
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
    tk.Label(sub1AFD, text="Seleccione los AFN's a Unir:", bg="thistle1").pack()
    num_AFNS = tk.Entry(sub1AFD, width=5, justify='center')
    num_AFNS.pack(pady=5)
    tk.Button(sub1AFD, text="   Ejecutar   ", command = lambda: unirAFNS(num_AFNS, log_resultado, cont_AFN)).pack(pady=10)


    tk.Label(sub2AFD, text="Convertir a un AFD", font=("Arial", 11, "bold"), bg="thistle1").pack(pady=20)
    tk.Label(sub2AFD, text="Ingrese el numero del AFN:", bg="thistle1").pack()
    num_AFN = tk.Entry(sub2AFD, width=5, justify='center')
    num_AFN.pack(pady=5)
    tk.Button(sub2AFD, text="   Ejecutar   ", command = lambda: hacerAFD(num_AFN, log_resultado, cont_AFN)).pack(pady=10)

    # Pestaña 3
    tk.Label(pestaña3, text="Descargar AFD a Txt", font=("Arial", 11, "bold"), bg="lightblue").pack(pady=20)
    tk.Label(pestaña3, text="Ingrese el numero del AFD:", bg="lightblue").pack()
    num_AFD = tk.Entry(pestaña3, width=5, justify='center')
    num_AFD.pack(pady=5)
    tk.Button(pestaña3, text="   Ejecutar   ", command=lambda: guardarArchivo(num_AFD, log_resultado, afds)).pack(pady=10)


    # Subpestañas del AFN (Pestaña 1)
    notebookAFN = ttk.Notebook(pestaña1)
    notebookAFN.pack(expand = True, fill = "both", padx = 10, pady = 10)

    sub1 = tk.Frame(notebookAFN, bg="lavender") # Crear basico 1
    sub2 = tk.Frame(notebookAFN, bg="lavender") # Crear basico 2
    sub3 = tk.Frame(notebookAFN, bg="lavender") # Concatenar
    sub4 = tk.Frame(notebookAFN, bg="lavender") # Cerradura +
    sub5 = tk.Frame(notebookAFN, bg="lavender") # Cerradura *
    sub6 = tk.Frame(notebookAFN, bg="lavender") # Opcional ?

    notebookAFN.add(sub1, text="Crear B1")
    notebookAFN.add(sub2, text="Crear B2")
    notebookAFN.add(sub3, text="Concatenar")
    notebookAFN.add(sub4, text="Cerradura +")
    notebookAFN.add(sub5, text="Cerradura *")
    notebookAFN.add(sub6, text="Opcional ?")
    
    # AFN Basico 1
    tk.Label(sub1, text=" AFN Basico 1 ", font=("Arial", 11, "bold"), bg="lavender").pack(pady=20)
    tk.Label(sub1, text="Ingrese un caracter:", bg="lavender").pack()
    ec1 = tk.Entry(sub1, width=5, justify='center')
    ec1.pack(pady=5)
    tk.Button(sub1, text="   Ejecutar   ", command=lambda: crearBasico1(ec1, log_resultado, cont_AFN)).pack(pady=15)

    # AFN Basico 2
    tk.Label(sub2, text=" AFN Basico 2 ", font=("Arial", 11, "bold"), bg="lavender").pack(pady=20)
    tk.Label(sub2, text="Ingrese un caracter:", bg="lavender").pack()
    ec2 = tk.Entry(sub2, width=5, justify='center')
    ec2.pack(pady=5)
    tk.Label(sub2, text="Ingrese otro caracter:", bg="lavender").pack()
    ec3 = tk.Entry(sub2, width=5, justify='center')
    ec3.pack(pady=5)
    tk.Button(sub2, text="   Ejecutar   ", command=lambda: crearBasico2(ec2, ec3, log_resultado, cont_AFN)).pack(pady=10)

    # AFN Concatenar
    tk.Label(sub3, text=" Concatenar AFN's ", font=("Arial", 11, "bold"), bg="lavender").pack(pady=20)
    tk.Label(sub3, text="Ingrese el numero del AFN 1:", bg="lavender").pack()
    ec4 = tk.Entry(sub3, width=5, justify='center')
    ec4.pack(pady=5)
    tk.Label(sub3, text="Ingrese el numero del AFN 2:", bg="lavender").pack()
    ec5 = tk.Entry(sub3, width=5, justify='center')
    ec5.pack(pady=5)
    tk.Button(sub3, text="   Ejecutar   ", command=lambda: concatenarAFN(ec4, ec5, log_resultado, cont_AFN)).pack(pady=10)

    # AFN Cerradura Positiva
    tk.Label(sub4, text=" Cerradura Positiva ", font=("Arial", 11, "bold"), bg="lavender").pack(pady=20)
    tk.Label(sub4, text="Ingrese el numero del AFN:", bg="lavender").pack()
    ec6 = tk.Entry(sub4, width=5, justify='center')
    ec6.pack(pady=5)
    tk.Button(sub4, text="   Ejecutar   ", command=lambda: cerrPostiva(ec6, log_resultado)).pack(pady=10)

    # AFN Cerradura de Kleene
    tk.Label(sub5, text=" Cerradura de Kleene ", font=("Arial", 11, "bold"), bg="lavender").pack(pady=20)
    tk.Label(sub5, text="Ingrese el numero del AFN:", bg="lavender").pack()
    ec7 = tk.Entry(sub5, width=5, justify='center')
    ec7.pack(pady=5)
    tk.Button(sub5, text="   Ejecutar   ", command=lambda: cerrKleene(ec7, log_resultado)).pack(pady=10)

    # AFN Opcional
    tk.Label(sub6, text=" Opcional ", font=("Arial", 11, "bold"), bg="lavender").pack(pady=20)
    tk.Label(sub6, text="Ingrese el numero del AFN:", bg="lavender").pack()
    ec8 = tk.Entry(sub6, width=5, justify='center')
    ec8.pack(pady=5)
    tk.Button(sub6, text="   Ejecutar   ", command=lambda: opcional(ec8, log_resultado)).pack(pady=10)


    ventana.mainloop()


if __name__ == "__main__":
    main()