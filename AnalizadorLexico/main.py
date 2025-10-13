import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from AFN import AFN, EPSILON

# Definimos una lista de los AFN y AFD que se van creando
afns = []
afds = []

# Funciones adicionales necesarias
def guardarArchivo(afd, log_fun):
    num = afd.get().strip()
    afd.delete(0, tk.END)

    if (num is None) or (num > len(afds)):
        log_fun("Error! El numero de AFD indicado no existe.")
        return
    
    afdG = afds[num - 1]
    
    ruta = filedialog.asksaveasfilename(
        defaultextension=".txt",
        initialfile="afd_resultado.txt",
        title="Guardar AFD como",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )

    if not ruta:
        log_fun("Error! Guardado cancelado por el usuario.")
        return

    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write("=== AFD GENERADO ===\n")
            archivo.write(f"Estados: {[edo.id for edo in afd.EdosAFD if edo is not None and edo.id != -1]}\n")
            archivo.write(f"Inicial: {afd.EdoInicial}\n")
            archivo.write(f"Aceptacion: {' '.join(str(e) for e in afd.EdosAceptacion)}\n")
            archivo.write(f"Alfabeto: {sorted(afd.Alfabeto)}\n")

            # Escribir las transiciones
            for edo in afd.EdosAFD:
                if edo is None or edo.id == -1:
                    continue
                transiciones_str = []
                for i, dest in enumerate(edo.transAFD):
                    if dest != -1:
                        transiciones_str.append(f"('{chr(i)}'->{dest})")
                archivo.write(f"Estado {edo.id}: " + ", ".join(transiciones_str) + "\n")
            
        messagebox.showinfo("Felicidades!", f"AFD guardado correctamente en: {ruta}\n")
            
    except Exception as e:
        messagebox.showinfo("Error!", f"No se ha podido guardar el AFD.\n")
        log_fun(f"Error! {e}.")

def actualizarContador(cont_AFN):
    cont_AFN.set(f"Numero total de AFN's: {len(afns)}")

def actualizarContador2(cont_AFD):
    cont_AFD.set(f"Numero total de AFD's: {len(afds)}")

def obtener_indice(entry, log_fun):
    if entry is None:
        log_fun("Error! No se ha detectado ningun Entry.")

    raw = entry.get().strip()
    print(f"OBTENER INDICE : valor obtenido {raw}")
    if raw == "":
        log_fun("Error! El campo esta vacio. Ingrese un numero valido.")
        entry.focus_set()
        return None

    if not raw.isdigit():
        log_fun(f"Error! '{valor}' no es un número valido.")
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
    log_fun("===============\n")

def imprimir_afd(afd, log_fun):
    log_fun("\n=== AFD RESULTANTE ===\n")
    log_fun(f"Estados totales: {afd.NumEdos}")
    log_fun(f"Estado inicial: {afd.EdoInicial}")
    log_fun(f"Estados de aceptación: {afd.EdosAceptacion}")
    log_fun(f"Alfabeto: {sorted(afd.Alfabeto)}\n")

    for edo in afd.EdosAFD:
        if edo is None or edo.id == -1:
            continue
        log_fun(f"Estado {edo.id}:")
        for i, dest in enumerate(edo.transAFD):
            if dest != -1:
                log_fun(f"\tcon '{chr(i)}' -> {dest}")
    log_fun("===============\n")


# Opciones del AFN
def crearBasico1(entry_widget, log_fun, cont_AFN):
    print("Opcion seleccionada de Crear Basico\n")

    caracter = entry_widget.get().strip()
    entry_widget.delete(0, tk.END)
    print(f"Caracter recibido: {caracter}\n")

    if not caracter:
        log_fun("Error! Debes ingresar al menos un caracter para crear un AFN basico")
        return

    if len(caracter) > 1:
        log_fun(f"Error! Se ha detectado mas de un caracter, se tomara solo el primero.\n")
        caracter = caracter[0]
        
    afn1 = AFN()
    afn1.CrearBasicoUno(caracter)
    afns.append(afn1)

    actualizarContador(cont_AFN)

    log_fun(f"AFN Basico 1 creado para el caracter: '{caracter}'")
    imprimir_afn(afn1, log_fun)

    print(f"Numero de AFN's totales {len(afns)}\n")

def crearBasico2(entry_widget1, entry_widget2, log_fun, cont_AFN):
    print("Opcion seleccionada de Crear Basico\n")

    caracter1 = entry_widget1.get().strip()
    caracter2 = entry_widget2.get().strip()
    entry_widget1.detele(0, tk.END)
    entry_widget2.detele(0, tk.END)

    print(f"Caracteres recibidos: {caracter1, caracter2}\n")

    if(not caracter1) and (not caracter2):
        log_fun(f"Error! Debes ingresar al menos un caracter para crear un AFN basico")
        return

    
    if (len(caracter1) > 1) or (len(caracter2) > 1):
        log_fun(f"Error! Se ha detectado mas de un caracter, se tomara solo el primero.\n")
        caracter1 = caracter1[0]
        caracter2 = caracter2[0]
        
    afn1 = AFN()
    afn1.CrearBasicoDos(caracter1, caracter2)
    afns.append(afn1)

    actualizarContador(cont_AFN)

    log_fun(f"AFN Basico 2 creado para los caracteres: '{caracter1} - {caracter2}'")
    imprimir_afn(afn1, log_fun)

    print(f"Numero de AFN's totales {len(afns)}\n")

def unirAFN(afn1, afn2, log_fun, cont_AFN):
    print("Opcion seleccionada unir AFN\n")

    if(len(afns) < 2):
        log_fun("Error! Se necesitan al menos 2 AFN's para realizar esta operacion.")
        return

    num1 = obtener_indice(afn1, log_fun)
    num2 = obtener_indice(afn2, log_fun)
    print(f"Numeros obtenidos: {num1} - {num2}")

    if num1 is None:
        log_fun("Error! Ingrese el número del AFN 1.")
        return

    if num2 is None:
        log_fun("Error! Ingrese el número del AFN 2.")
        return

    if num1 == num2:
        log_fun("Error! No se puede unir un AFN consigo mismo.")
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

def hacerAFD(afn, log_fun, cont_AFD):
    print("Opcion seleccionada convertir a AFD\n")

    num = obtener_indice(afn, log_fun)

    a = afns[num - 1]

    afd = a.ConvertirAAFD()
    afds.append(afd)

    afns.pop(num - 1)
    actualizarContador2(cont_AFD)

    log_fun(f"Se ha creado el AFD a partir del AFN {num}.")


def main():
    # Definición de la ventana principal en Tkinter
    ventana = tk.Tk()
    ventana.title("Analizador Léxico")
    ventana.geometry("900x500")

    # Crear paneles
    paned_w = ttk.PanedWindow(ventana, orient = tk.HORIZONTAL)
    paned_w.pack(fill = "both", expand = True, padx = 10, pady = 10)
    
    panel_c = ttk.Frame(paned_w)
    panel_r = ttk.Frame(paned_w)

    paned_w.add(panel_c, weight = 3)
    paned_w.add(panel_r, weight = 1)

    # Contenedor de pestañas de panel_r
    tk.Label(panel_r, text = "Historial").pack(pady = 5)
    text_r = tk.Text(panel_r, wrap = tk.WORD, height = 20, width = 50)
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

    pestaña1 = tk.Frame(notebookP, bg="white")
    pestaña2 = tk.Frame(notebookP, bg="royalblue")
    pestaña3 = tk.Frame(notebookP, bg="lightblue")

    notebookP.add(pestaña1, text="AFN")
    notebookP.add(pestaña2, text="Convertir a un AFD")
    notebookP.add(pestaña3, text="Descargar")

    # Pestaña 2
    tk.Label(pestaña2, text="Convertir a un AFD").pack(pady=20)
    tk.Label(pestaña2, text="Ingrese el numero del AFN:").pack()
    numAFN = tk.Entry(pestaña2, width=5, justify='center')
    numAFN.pack(pady=5)
    tk.Button(pestaña2, text="Ejecutar", command=lambda: hacerAFD(numAFN, log_resultado)).pack(pady=10)

    # Pestaña 3
    tk.Label(pestaña3, text="Descargar AFD a Txt").pack(pady=20)
    tk.Label(pestaña3, text="Ingrese el numero del AFD:").pack()
    numAFD = tk.Entry(pestaña3, width=5, justify='center')
    numAFD.pack(pady=5)
    tk.Button(pestaña3, text="Ejecutar", command=lambda: guardarArchivo(numAFD, log_resultado)).pack(pady=10)

    # Contador de los AFD's
    cont_AFD = tk.StringVar()
    cont_AFD.set(f"Numero total de AFD's: {len(afds)}")
    tk.Label(pestaña2, textvariable = cont_AFD).pack(side = tk.LEFT, padx = 20)

    # Subpestañas del AFN (Pestaña 1)
    notebookAFN = ttk.Notebook(pestaña1)
    notebookAFN.pack(expand = True, fill = "both", padx = 10, pady = 10)

    sub1 = ttk.Frame(notebookAFN) # Crear basico 1
    sub2 = ttk.Frame(notebookAFN) # Crear basico 2
    sub3 = ttk.Frame(notebookAFN) # Unir
    sub4 = ttk.Frame(notebookAFN) # Concatenar
    sub5 = ttk.Frame(notebookAFN) # Cerradura +
    sub6 = ttk.Frame(notebookAFN) # Cerradura *
    sub7 = ttk.Frame(notebookAFN) # Opcional

    notebookAFN.add(sub1, text="Crear B1")
    notebookAFN.add(sub2, text="Crear B2")
    notebookAFN.add(sub3, text="Unir")
    notebookAFN.add(sub4, text="Concatenar")
    notebookAFN.add(sub5, text="Cerradura +")
    notebookAFN.add(sub6, text="Cerradura *")
    notebookAFN.add(sub7, text="Opcional ?")

    # Contador de los AFN's
    cont_AFN = tk.StringVar()
    cont_AFN.set(f"Numero total de AFN's: {len(afns)}")
    tk.Label(pestaña1, textvariable = cont_AFN).pack(side = tk.LEFT, padx = 20)
    
    # AFN Basico 1
    tk.Label(sub1, text="AFN Basico 1").pack(pady=20)
    tk.Label(sub1, text="Ingrese un caracter:").pack()
    entry_caracter = tk.Entry(sub1, width=5, justify='center')
    entry_caracter.pack(pady=5)
    tk.Button(sub1, text="Ejecutar", command=lambda: crearBasico1(entry_caracter, log_resultado, cont_AFN)).pack(pady=10)

    # AFN Basico 2
    tk.Label(sub2, text="AFN Basico 2").pack(pady=20)
    tk.Label(sub2, text="Ingrese un caracter:").pack()
    entry_caracter1 = tk.Entry(sub2, width=5, justify='center')
    entry_caracter1.pack(pady=5)
    tk.Label(sub2, text="Ingrese otro caracter:").pack()
    entry_caracter2 = tk.Entry(sub2, width=5, justify='center')
    entry_caracter2.pack(pady=5)
    tk.Button(sub2, text="Ejecutar", command=lambda: crearBasico2(entry_caracter1, entry_caracter2, log_resultado, cont_AFN)).pack(pady=10)

    # AFN Unir
    tk.Label(sub3, text="Unir AFN's").pack(pady=20)
    tk.Label(sub3, text="Ingrese el numero del AFN 1:").pack()
    afn1 = tk.Entry(sub3, width=5, justify='center')
    afn1.pack(pady=5)
    tk.Label(sub3, text="Ingrese el numero del AFN 2:").pack()
    afn2 = tk.Entry(sub3, width=5, justify='center')
    afn2.pack(pady=5)
    tk.Button(sub3, text="Ejecutar", command=lambda: unirAFN(afn1, afn2, log_resultado, cont_AFN)).pack(pady=10)

    # AFN Concatenar
    tk.Label(sub4, text="Concatenar AFN's").pack(pady=20)
    tk.Label(sub4, text="Ingrese el numero del AFN 1:").pack()
    afn1 = tk.Entry(sub4, width=5, justify='center')
    afn1.pack(pady=5)
    tk.Label(sub4, text="Ingrese el numero del AFN 2:").pack()
    afn2 = tk.Entry(sub4, width=5, justify='center')
    afn2.pack(pady=5)
    tk.Button(sub4, text="Ejecutar", command=lambda: concatenarAFN(afn1, afn2, log_resultado, cont_AFN)).pack(pady=10)

    # AFN Cerradura Positiva
    tk.Label(sub5, text="Cerradura Positiva").pack(pady=20)
    tk.Label(sub5, text="Ingrese el numero del AFN:").pack()
    afn1 = tk.Entry(sub5, width=5, justify='center')
    afn1.pack(pady=5)
    tk.Button(sub5, text="Ejecutar", command=lambda: cerrPostiva(afn1, log_resultado)).pack(pady=10)

    # AFN Cerradura de Kleene
    tk.Label(sub6, text="Cerradura de Kleene").pack(pady=20)
    tk.Label(sub6, text="Ingrese el numero del AFN:").pack()
    afn1 = tk.Entry(sub6, width=5, justify='center')
    afn1.pack(pady=5)
    tk.Button(sub6, text="Ejecutar", command=lambda: cerrKleene(afn1, log_resultado)).pack(pady=10)

    # AFN Opcional
    tk.Label(sub7, text="Opcional").pack(pady=20)
    tk.Label(sub7, text="Ingrese el numero del AFN:").pack()
    afn1 = tk.Entry(sub7, width=5, justify='center')
    afn1.pack(pady=5)
    tk.Button(sub7, text="Ejecutar", command=lambda: opcional(afn1, log_resultado)).pack(pady=10)


    ventana.mainloop()


if __name__ == "__main__":
    main()