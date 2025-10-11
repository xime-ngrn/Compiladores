"""
from AFN import AFN, EPSILON

def imprimir_afn(afn):
    print("\n=== AFN ===")
    print(f"Estados totales: {len(afn.Estados)}")
    print(f"Estado inicial: {afn.EdoInicial.IdEdo}")
    print(f"Estados de aceptación: {[e.IdEdo for e in afn.EdosAceptacion]}")
    print(f"Alfabeto: {sorted(afn.Alfabeto)}")
    for e in sorted(afn.Estados, key=lambda x: x.IdEdo):
        print(f" Estado {e.IdEdo} (Acept: {e.EdoAcept}):")
        for t in e.Transiciones:
            si = t.SimboloInf
            ss = t.SimboloSup
            dest = t.EdoDestino.IdEdo if t.EdoDestino is not None else None
            print(f"   -> {si!r}-{ss!r} -> {dest}")
    print("============\n")

def imprimir_afd(afd):
    print("\n=== AFD RESULTANTE ===")
    print(f"Estados totales: {afd.NumEdos}")
    print(f"Estado inicial: {afd.EdoInicial}")
    print(f"Estados de aceptación: {afd.EdosAceptacion}")
    print(f"Alfabeto: {sorted(afd.Alfabeto)}\n")

    for edo in afd.EdosAFD:
        if edo is None or edo.id == -1:
            continue
        print(f"Estado {edo.id}:")
        for i, dest in enumerate(edo.transAFD):
            if dest != -1:
                print(f"   con '{chr(i)}' -> {dest}")
    print("======================\n")

def main():
    # Crear AFN para 'a'
    afn1 = AFN()
    afn1.CrearBasicoUno('a')

    # Crear AFN para 'b'
    afn2 = AFN()
    afn2.CrearBasicoUno('b')

    # Unir: afn1 = afn1 | afn2
    afn1.UnirAFN(afn2)
    print("AFN creado para la expresión: a|b")
    imprimir_afn(afn1)

    # Aplicar opcional (equivale a (a|b)? )
    afn1.Opcional()
    print("Se aplicó el operador opcional (a|b)?")
    imprimir_afn(afn1)

    # Convertir a AFD
    afd = afn1.ConvertirAAFD()
    print("Conversión AFN -> AFD completada")
    imprimir_afd(afd)


if __name__ == "__main__":
    main()

"""