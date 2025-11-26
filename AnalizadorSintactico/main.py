import tkinter as tk
from tkinter import ttk, messagebox

from .Calculadora import Calculadora
from AnalizadorLexico.AnalizadorLex import AnalizadorLex

def implementarCalculadora(entry, log_fun):
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

    raw = raw.replace(" ", "").replace("\t", "").replace("\n", "")

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
            log_fun(f"   • Notación Postfija: {' '.join(resultado['postfija'])}\n")
            log_fun(f"   • Resultado Final: {resultado['resultado']}\n")
            log_fun("==========================")
            
            # Mostrar resultado en un messagebox también
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
        messagebox.showerror("Error de archivo", error_msg)
        
    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        print(f"\n{error_msg}")
        log_fun(f"\n{error_msg}\n")
        messagebox.showerror("Error de análisis", error_msg)
        import traceback
        traceback.print_exc()


def main():
    # Definición de la ventana principal en Tkinter
    ventana = tk.Tk()
    ventana.title("Analizador Sintáctico")
    ventana.geometry("900x500")
    ventana.configure(bg = "white")

    style = ttk.Style()
    style.configure("TButton", background = "#f8f8f8", relief = "flat")
    style.map("TButton", background=[("active", "#e6e6e6")])
    style.configure("TNotebook", background="white")
    style.configure("TFrame", background="white")
    style.configure("TLabelframe", background="white")

    # Crear paneles
    paned_w = ttk.Panedwindow(ventana, orient = tk.HORIZONTAL)
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
    pestaña2 = tk.Frame(notebookP, bg = "light blue")

    notebookP.add(pestaña1, text="AFN's")
    notebookP.add(pestaña2, text="Análisis Sintáctico")

    # Pestaña 2
    notebook = ttk.Notebook(pestaña2)
    notebook.pack(expand=True, fill="both", padx = 10, pady = 10)

    sub1 = tk.Frame(notebook, bg = "light blue") # Descenso recursivo - Calculadora y Gramática de Gramáticas
    sub2 = tk.Frame(notebook, bg = "light blue") # Análisis LL(1)
    sub3 = tk.Frame(notebook, bg = "light blue") # Análisis SLR
    sub4 = tk.Frame(notebook, bg = "light blue") # Análisis LR Canónico

    # Subpestañas de Análisis Sintáctico
    notebook.add(sub1, text="Descenso Recursivo")
    notebook.add(sub2, text="Análisis LL(1)")
    notebook.add(sub3, text="Análisis SLR")
    notebook.add(sub4, text="Análisis LR Canónico")

    # Subpestaña 1 - Descenso Recursivo
    sub1_notebook = ttk.Notebook(sub1)
    sub1_notebook.pack(expand=True, fill="both", padx=5, pady=5)

    # Subpestaña "Calculadora"
    calculadora_tab = tk.Frame(sub1_notebook, bg="light blue")
    sub1_notebook.add(calculadora_tab, text="Calculadora")
    tk.Label(calculadora_tab, text="Calculadora", fg="black", bg="light blue", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(calculadora_tab, text="Ingrese una expresión:", bg="light blue").pack()
    exp1 = tk.Entry(calculadora_tab, width=20, justify='center')
    exp1.pack(pady=5)
    tk.Button(sub1, text="   Ejecutar   ", command=lambda: implementarCalculadora(exp1, log_resultado)).pack(pady=15)

    # Subpestaña "Gramática de Gramáticas"
    gramatica_tab = tk.Frame(sub1_notebook, bg="light blue")
    sub1_notebook.add(gramatica_tab, text="Gramática de Gramáticas")

    tk.Label(gramatica_tab, text="Gramática de Gramáticas", fg="black", bg="light blue", font=("Arial", 12, "bold")).pack(pady=5)

    # Subpestaña 2 - Análisis LL(1)
    tk.Label(sub2, text="Análisis LL(1)", fg="black", bg="light blue", font=("Arial", 12, "bold")).pack(pady=5)
    
    # Subpestaña 3 - Análisis SLR
    tk.Label(sub3, text="Análisis SLR", fg="black", bg="light blue", font=("Arial", 12, "bold")).pack(pady=5)

    # Subpestaña 4 - Análisis LR Canónico
    tk.Label(sub4, text="Análisis LR Canónico", fg="black", bg="light blue", font=("Arial", 12, "bold")).pack(pady=5)

    ventana.mainloop()

if __name__ == "__main__":
    main()