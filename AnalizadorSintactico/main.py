import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from .Calculadora import Calculadora
from .ER_AFN import ER_AFN
from AnalizadorLexico.AnalizadorLex import AnalizadorLex
from AnalizadorLexico.AFN import AFN

def imprimir_afn(afn: AFN, log_fun):
    """Imprime el AFN con todos sus detalles en el log."""
    
    # Asignar IDs únicos a los estados si no los tienen
    estados_lista = list(afn.Estados)
    for idx, estado in enumerate(estados_lista):
        if not hasattr(estado, 'IdEdo') or estado.IdEdo is None:
            estado.IdEdo = idx
    
    log_fun(f"   • Estados Totales: {len(afn.Estados)}")
    log_fun(f"   • Estado Inicial: {afn.EdoInicial.IdEdo if afn.EdoInicial else 'None'}")
    
    estados_acep_ids = [e.IdEdo for e in afn.EdosAceptacion if hasattr(e, 'IdEdo')]
    log_fun(f"   • Estados de Aceptación: {estados_acep_ids}")
    
    alfabeto_limpio = sorted([s for s in afn.Alfabeto if s != 'ε'])
    log_fun(f"   • Alfabeto: {alfabeto_limpio}")
    log_fun("")
    
    # Imprimir transiciones
    log_fun("   • Transiciones:")
    
    for estado in sorted(estados_lista, key=lambda x: x.IdEdo):
        token_info = f", Token={estado.Token}" if hasattr(estado, 'Token') and estado.Token != -1 else ""
        acept_info = "✓" if estado.EdoAcept else " "
        
        log_fun(f"Estado {estado.IdEdo} [{acept_info}]{token_info}:")
        
        if not estado.Transiciones:
            log_fun(f"   (sin transiciones)")
        else:
            for trans in estado.Transiciones:
                simb_inf = trans.SimboloInf if trans.SimboloInf else 'ε'
                simb_sup = trans.SimboloSup if trans.SimboloSup else 'ε'
                
                if simb_inf == simb_sup:
                    simbolo = f"'{simb_inf}'"
                else:
                    simbolo = f"[{simb_inf}-{simb_sup}]"
                
                destino = trans.EdoDestino.IdEdo if trans.EdoDestino and hasattr(trans.EdoDestino, 'IdEdo') else '?'
                log_fun(f"   {simbolo} → Estado {destino}")
        
        log_fun("")
    
    log_fun("="*60 + "\n")


def guardar_afn_archivo(afn: AFN, log_fun):
    """Guarda el AFN en un archivo de texto en formato legible."""
    ruta = filedialog.asksaveasfilename(
        defaultextension=".txt",
        initialfile="afn.txt",
        title="Guardar AFN como",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )
    
    if not ruta:
        messagebox.showinfo("Cancelado", "Guardado cancelado por el usuario.")
        log_fun("Operación de guardado cancelada.\n")
        return
    
    try:
        # Asignar IDs a los estados
        estados_lista = list(afn.Estados)
        for idx, estado in enumerate(estados_lista):
            if not hasattr(estado, 'IdEdo') or estado.IdEdo is None:
                estado.IdEdo = idx
        
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write("="*60 + "\n")
            archivo.write("AUTÓMATA FINITO NO DETERMINISTA (AFN)\n")
            archivo.write("="*60 + "\n\n")
            
            archivo.write(f"Estados totales: {len(afn.Estados)}\n")
            archivo.write(f"Estado inicial: {afn.EdoInicial.IdEdo if afn.EdoInicial else 'None'}\n")
            
            estados_acep = [e.IdEdo for e in afn.EdosAceptacion if hasattr(e, 'IdEdo')]
            archivo.write(f"Estados de aceptación: {estados_acep}\n")
            
            alfabeto_limpio = sorted([s for s in afn.Alfabeto if s != 'ε'])
            archivo.write(f"Alfabeto: {alfabeto_limpio}\n\n")
            
            archivo.write("TRANSICIONES:\n")
            archivo.write("-"*60 + "\n")
            
            for estado in sorted(estados_lista, key=lambda x: x.IdEdo):
                token_info = f" [Token={estado.Token}]" if hasattr(estado, 'Token') and estado.Token != -1 else ""
                acept_info = " [ACEPTACIÓN]" if estado.EdoAcept else ""
                
                archivo.write(f"\nEstado {estado.IdEdo}{acept_info}{token_info}:\n")
                
                if not estado.Transiciones:
                    archivo.write("  (sin transiciones)\n")
                else:
                    for trans in estado.Transiciones:
                        simb_inf = trans.SimboloInf if trans.SimboloInf else 'ε'
                        simb_sup = trans.SimboloSup if trans.SimboloSup else 'ε'
                        
                        if simb_inf == simb_sup:
                            simbolo = f"'{simb_inf}'"
                        else:
                            simbolo = f"[{simb_inf}-{simb_sup}]"
                        
                        destino = trans.EdoDestino.IdEdo if trans.EdoDestino and hasattr(trans.EdoDestino, 'IdEdo') else '?'
                        archivo.write(f"  {simbolo} → Estado {destino}\n")
            
            archivo.write("\n" + "="*60 + "\n")
        
        messagebox.showinfo("Éxito", f"AFN guardado correctamente en:\n{ruta}")
        log_fun(f"AFN guardado correctamente en: {ruta}")
        log_fun("==========================\n")
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el AFN:\n{str(e)}")
        log_fun(f"Error al guardar: {e}\n")


def convertir_y_guardar_afd(afn: AFN, log_fun):
    """Convierte el AFN a AFD y lo guarda en formato de tabla."""
    ruta = filedialog.asksaveasfilename(
        defaultextension=".txt",
        initialfile="afd_desde_afn.txt",
        title="Guardar AFD como",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )
    
    if not ruta:
        messagebox.showinfo("Cancelado", "Guardado cancelado por el usuario.")
        log_fun("Operación de guardado cancelada.\n")
        return
    
    try:
        log_fun("Convirtiendo AFN a AFD...")
        
        afd = afn.ConvertirAAFD()
        
        log_fun(f"AFD generado con {afd.NumEdos} estados")
        log_fun("==========================\n")
        
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(" ".join(map(str, range(afd.NumEdos))) + "\n")
            archivo.write(str(afd.EdoInicial) + "\n")
            archivo.write(" ".join(map(str, sorted(afd.EdosAceptacion))) + "\n")
            
            alfabeto_ordenado = sorted(afd.Alfabeto)
            archivo.write(" ".join(alfabeto_ordenado) + "\n")
            
            for edo in afd.EdosAFD:
                if edo is None or edo.id == -1 or edo.id >= afd.NumEdos:
                    continue
                
                fila = []
                for simb in alfabeto_ordenado:
                    idx = ord(simb)
                    destino = edo.transAFD[idx] if idx < len(edo.transAFD) else -1
                    fila.append(str(destino) if destino != -1 else "-")
                
                token = getattr(edo, 'Token', -1)
                fila.append(str(token) if token != -1 else "-")
                
                archivo.write(" ".join(fila) + "\n")
        
        messagebox.showinfo("Éxito", f"AFD guardado correctamente en:\n{ruta}")
        log_fun(f"AFD guardado correctamente en: {ruta}")
        log_fun("==========================\n")
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el AFD:\n{str(e)}")
        log_fun(f"Error al guardar AFD: {e}\n")


def implementarCalculadora(entry, log_fun):
    print("Calculadora\n")
    if entry is None:
        messagebox.showerror("Error!", "No se proporcionó ninguna expresión para analizar.")
        return
    raw = entry.get().strip()
    if not raw:
        messagebox.showerror("Error!", "El campo está vacío.")
        entry.focus_set()
        return
    print(f"Expresión a analizar: {raw}")
    log_fun("\n==========================")
    log_fun(f"Expresión enviada: {raw}")
    raw = "".join(raw.split())
    Tokens = {
        "SUMA": 10, "RESTA": 20, "PROD": 30, "DIV": 40, "EXP": 50,
        "SIN": 60, "COS": 60, "TAN": 60,
        "ASIN": 60, "ACOS": 60, "ATAN": 60,
        "LOG": 60, "LN": 60, "EXP_FN": 60, 
        "PAR_I": 70, "PAR_D": 80,
        "PI": 90,
        "NUM": 100,
    }
    try:
        cal = Calculadora(Tokens, AFD="AnalizadorSintactico/AFD_Calculadora.txt")
        resultado = cal.Evaluar(raw)
        if resultado['exito']:
            print("Expresión válida.")
            log_fun("Análisis completado exitosamente!")
            log_fun("Resultados:")
            log_fun(f"   • Notación Postfija: {' '.join(resultado['postfija'])}")
            log_fun(f"   • Resultado Final: {resultado['resultado']}\n")
            log_fun("==========================")
            messagebox.showinfo(
                "Resultado", 
                f"Expresión: {raw}\n\n"
                f"Notación Postfija: {' '.join(resultado['postfija'])}\n\n"
                f"Resultado: {resultado['resultado']}"
            )
        else:
            print(f"{resultado['error']}\n")
            log_fun("\nError! La expresión contiene errores sintácticos.")
            log_fun("==========================")
            messagebox.showerror("Error de sintaxis", "La expresión contiene errores sintácticos.")
    except FileNotFoundError:
        error_msg = "Error: No se encontró el archivo AFD_Calculadora.txt"
        print(f"\n{error_msg}")
        log_fun(f"\n{error_msg}\n")
        messagebox.showerror("Error de archivo.", error_msg)
    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        print(f"\n{error_msg}")
        log_fun(f"\n{error_msg}\n")
        messagebox.showerror("Error de análisis en la calculadora.", error_msg)
        import traceback; traceback.print_exc()


def implementarExpReg(entry, log_fun):
    """Función principal para procesar expresiones regulares."""
    print("Expresión regular\n")
    if entry is None:
        messagebox.showerror("Error", "No se proporcionó ninguna expresión para analizar.")
        return
    
    raw = entry.get().strip()
    if not raw:
        messagebox.showerror("Error", "El campo está vacío.")
        entry.focus_set()
        return
    
    print(f"Expresión a analizar: {raw}")
    log_fun("\n==========================")
    log_fun(f"Expresión enviada: {raw}")
    
    raw = "".join(raw.split())

    Tokens = {
        "OR": 10, "CONC": 20, "CERR_POS": 30, "CERR_KLEEN": 40, "OPC": 50, 
        "PAR_I": 60, "PAR_D": 70,
        "SIMB": 80, "COR_I": 90, "COR_D": 100, "GUION": 110
    }

    try:
        exp = ER_AFN(raw, Tokens, AFD_P="AnalizadorSintactico/AFD_ExpReg.txt")
        afnR = exp.IniConversion()
        
        if afnR is not None:
            log_fun("\nAFN creado exitosamente!")
            imprimir_afn(afnR, log_fun)
            
            # Preguntar al usuario qué desea hacer
            respuesta = messagebox.askyesnocancel(
                "AFN Generado", 
                "AFN creado exitosamente.\n\n"
                "¿Qué desea hacer?\n\n"
                "• SÍ: Guardar AFN\n"
                "• No: Convertir a AFD y guardar\n"
                "• CANCELAR: No guardar"
            )
            
            if respuesta is True:
                guardar_afn_archivo(afnR, log_fun)
            elif respuesta is False:
                convertir_y_guardar_afd(afnR, log_fun)
            
        else:
            log_fun("\nError: No se pudo generar el AFN")
            messagebox.showerror("Error", "No se pudo generar el AFN.\nVerifique la sintaxis de la expresión.")
            
    except FileNotFoundError:
        error_msg = "Error: No se encontró el archivo AFD_ExpReg.txt"
        print(f"\n{error_msg}")
        log_fun(f"\n{error_msg}\n")
        messagebox.showerror("Error de archivo", error_msg)
    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        print(f"\n{error_msg}")
        log_fun(f"\n{error_msg}\n")
        messagebox.showerror("Error", error_msg)
        import traceback
        traceback.print_exc()


def main():
    ventana = tk.Tk()
    ventana.title("Analizador Sintáctico")
    ventana.geometry("900x500")
    ventana.configure(bg="white")

    style = ttk.Style()
    style.configure("TButton", background="#f8f8f8", relief="flat")
    style.map("TButton", background=[("active", "#e6e6e6")])
    style.configure("TNotebook", background="white")
    style.configure("TFrame", background="white")
    style.configure("TLabelframe", background="white")

    paned_w = ttk.Panedwindow(ventana, orient=tk.HORIZONTAL)
    paned_w.pack(fill="both", expand=True, padx=10, pady=10)

    panel_c = ttk.Frame(paned_w)
    panel_r = ttk.Frame(paned_w)
    paned_w.add(panel_c, weight=3)
    paned_w.add(panel_r, weight=1)

    panel_i = ttk.Frame(panel_c)
    panel_i.pack(fill="x", pady=5)

    tk.Label(panel_r, text="Historial", fg="black", bg="white", font=("Arial", 10, "bold")).pack(pady=5)
    text_r = tk.Text(panel_r, wrap="none", height=20, width=50, bg="#fafafa", relief="flat")
    scrollbar_y = tk.Scrollbar(panel_r, orient="vertical", command=text_r.yview)
    text_r.config(yscrollcommand=scrollbar_y.set)
    scrollbar_x = tk.Scrollbar(panel_r, orient="horizontal", command=text_r.xview)
    text_r.config(xscrollcommand=scrollbar_x.set)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    text_r.pack(fill="both", expand=True, padx=5, pady=5)

    def log_resultado(mensaje):
        text_r.insert(tk.END, mensaje + "\n")
        text_r.see(tk.END)

    notebookP = ttk.Notebook(panel_c)
    notebookP.pack(expand=True, fill="both", padx=10, pady=10)
    pestaña1 = tk.Frame(notebookP, bg="lavender")
    notebookP.add(pestaña1, text="Análisis Sintáctico")

    notebook = ttk.Notebook(pestaña1)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)
    sub1 = tk.Frame(notebook, bg="light blue")
    sub2 = tk.Frame(notebook, bg="light blue")
    sub3 = tk.Frame(notebook, bg="light blue")
    notebook.add(sub1, text="Descenso Recursivo")
    notebook.add(sub2, text="Análisis LL(1)")
    notebook.add(sub3, text="Análisis LR(0)")

    sub1_notebook = ttk.Notebook(sub1)
    sub1_notebook.pack(expand=True, fill="both", padx=5, pady=5)

    calculadora_tab = tk.Frame(sub1_notebook, bg="light blue")
    sub1_notebook.add(calculadora_tab, text="Calculadora")
    tk.Label(calculadora_tab, text="Calculadora", fg="black", bg="light blue", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(calculadora_tab, text="Ingrese una expresión:", bg="light blue").pack()
    exp1 = tk.Entry(calculadora_tab, width=20, justify='center')
    exp1.pack(pady=5)
    tk.Button(calculadora_tab, text="   Ejecutar   ", command=lambda: implementarCalculadora(exp1, log_resultado)).pack(pady=15)

    info_frame = tk.Frame(calculadora_tab, bg="light blue")
    info_frame.pack(pady=10, fill="x")
    operadores_frame = tk.Frame(info_frame, bg="light blue")
    operadores_frame.pack(side="left", padx=20, anchor="n")
    tk.Label(operadores_frame, text="Operadores", bg="light blue", font=("Arial", 10, "bold")).pack(anchor="w")
    tk.Label(operadores_frame, text="+   Suma\n-   Resta\n*   Multiplicación\n/   División\n^   Potencia", bg="light blue", justify="left").pack(anchor="w")
    funciones_frame = tk.Frame(info_frame, bg="light blue")
    funciones_frame.pack(side="left", padx=20, anchor="n")
    tk.Label(funciones_frame, text="Funciones", bg="light blue", font=("Arial", 10, "bold")).pack(anchor="w")
    tk.Label(funciones_frame, text="SIN(x)   Seno\nCOS(x)   Coseno\nTAN(x)   Tangente\nASIN(x)   Arcoseno\nACOS(x)   Arcocoseno\nATAN(x)   Arcotangente\nLOG(x)   Logaritmo base 10\nLN(x)    Logaritmo natural\nEXP(x)   Exponencial\n", bg="light blue", justify="left").pack(anchor="w")

    exp_tab = tk.Frame(sub1_notebook, bg="light blue")
    sub1_notebook.add(exp_tab, text="Expresión Regular a AFN")
    tk.Label(exp_tab, text="Expresión Regular a AFN", fg="black", bg="light blue", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(exp_tab, text="Ingrese una expresión:", bg="light blue").pack()
    exp2 = tk.Entry(exp_tab, width=20, justify='center')
    exp2.pack(pady=5)
    tk.Button(exp_tab, text="   Ejecutar   ", command=lambda: implementarExpReg(exp2, log_resultado)).pack(pady=15)

    tk.Label(sub2, text="Análisis LL(1)", fg="black", bg="light blue", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(sub3, text="Análisis SLR", fg="black", bg="light blue", font=("Arial", 12, "bold")).pack(pady=5)

    ventana.mainloop()

if __name__ == "__main__":
    main()