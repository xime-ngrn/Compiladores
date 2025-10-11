from Estado import Estado
from Transicion import Transicion
from AFD import AFD
from ElemSj import ElemSj
from collections import deque

EPSILON = 'ε'

class AFN:
    def __init__(self):
        self.Estados = set()          
        self.EdoInicial = None      
        self.Alfabeto = set()        
        self.EdosAceptacion = set()  

    def CrearBasicoUno(self, c):
        e1 = Estado()
        e2 = Estado()
        self.Estados.add(e1)
        self.Estados.add(e2) 
        self.EdoInicial = e1
        e1.Transiciones.add(Transicion(c,e2))
        e2.EdoAcept = True
        self.Alfabeto.add(c)
        self.EdosAceptacion.add(e2)

        return self
    
    def CrearBasicoDos(self, c1, c2):
        e1 = Estado()
        e2 = Estado()
        self.Estados.add(e1)
        self.Estados.add(e2) 
        self.EdoInicial = e1
        e1.Transiciones.add(Transicion(c1, c2,e2))
        e2.EdoAcept = True
        self.EdosAceptacion.add(e2)

        for i in range(ord(c1), ord(c2) + 1):
            simbolo = chr(i)
            self.Alfabeto.add(simbolo)

        return self
    
    def UnirAFN(self, F2):
        e1 = Estado()  
        e2 = Estado()  

        e1.Transiciones.add(Transicion(EPSILON, self.EdoInicial))
        e1.Transiciones.add(Transicion(EPSILON, F2.EdoInicial))

        e1.Transiciones.add(Transicion(EPSILON, e2))

        for e in self.EdosAceptacion:
            e.Transiciones.add(Transicion(EPSILON, e2))
            e.EdoAcept = False
        for e in F2.EdosAceptacion:
            e.Transiciones.add(Transicion(EPSILON, e2))
            e.EdoAcept = False

        e2.EdoAcept = True

        self.EdoInicial = e1
        self.Estados.update(F2.Estados)
        self.Estados.add(e1)
        self.Estados.add(e2)
        self.EdosAceptacion.clear()
        self.EdosAceptacion.add(e2)
        self.Alfabeto.update(F2.Alfabeto)

        return self


    
    def ConcatenarAFN(self, F2):
        for e in self.EdosAceptacion:
            for t in F2.EdoInicial.Transiciones:
                e.Transiciones.add(t)
            e.EdoAcept = False

        self.EdosAceptacion.clear()
        self.EdosAceptacion.update(F2.EdosAceptacion)
        self.Alfabeto.update(F2.Alfabeto)
        #F2.Estados.discard(F2.EdoInicial)
        self.Estados.update(F2.Estados)

        return self
    
    def CerraduraPositiva(self):
        e1 = Estado()
        e2 = Estado()

        for e in self.EdosAceptacion:
            e.Transiciones.add(Transicion(c_inf=EPSILON, c_sup=EPSILON, edoDestino=self.EdoInicial))
            e.Transiciones.add(Transicion(c_inf=EPSILON, c_sup=EPSILON, edoDestino=e2))
            e.EdoAcept = False
        
        e1.Transiciones.add(Transicion(c_inf=EPSILON, c_sup=EPSILON, edoDestino=self.EdoInicial))
        e1.Transiciones.add(Transicion(c_inf=EPSILON, c_sup=EPSILON, edoDestino=e2))
        self.EdoInicial = e1
        self.EdosAceptacion.clear()
        self.EdosAceptacion.add(e2)
        self.Estados.add(e1)
        self.Estados.add(e2)

        return self
    
    def CerraduraKleene(self):
        e1 = Estado()
        e2 = Estado()

        e1.Transiciones.add(Transicion(c_inf=EPSILON, c_sup=EPSILON, edoDestino=self.EdoInicial))
        e1.Transiciones.add(Transicion(c_inf=EPSILON, c_sup=EPSILON, edoDestino=e2))

        for e in self.EdosAceptacion:
            e.Transiciones.add(Transicion(c_inf=EPSILON, c_sup=EPSILON, edoDestino=self.EdoInicial))  
            e.Transiciones.add(Transicion(c_inf=EPSILON, c_sup=EPSILON, edoDestino=e2))               
            e.EdoAcept = False

        e2.EdoAcept = True

        self.EdoInicial = e1
        self.Estados.add(e1)
        self.Estados.add(e2)
        self.EdosAceptacion.clear()
        self.EdosAceptacion.add(e2)

        return self
    
    def Opcional(self):
        e1 = Estado()
        e2 = Estado()

        e1.Transiciones.add(Transicion(c_inf=EPSILON, c_sup=EPSILON, edoDestino=self.EdoInicial))
        e1.Transiciones.add(Transicion(c_inf=EPSILON, c_sup=EPSILON, edoDestino=e2))

        for e in self.EdosAceptacion:
            e.Transiciones.add(Transicion(c_inf=EPSILON, c_sup=EPSILON, edoDestino=e2))
            e.EdoAcept = False

        e2.EdoAcept = True

        self.EdoInicial = e1
        self.Estados.add(e1)
        self.Estados.add(e2)
        self.EdosAceptacion.clear()
        self.EdosAceptacion.add(e2)

        return self
    
    def CerraduraEpsilonUno(self, e):
        c = set()
        p = [e]
        while p:
            e2 = p.pop()
            if e2 is None:
                continue
            if e2 not in c:
                c.add(e2)
                for t in e2.Transiciones:
                    if t.SimboloInf == EPSILON and t.EdoDestino is not None:
                        p.append(t.EdoDestino)
        return c
    
    def CerraduraEpsilonDos(self, c):
        r = set()

        for e in c:
            r.update(self.CerraduraEpsilonUno(e))

        return r
    
    def MoverUno(self, e, c):
        r = set()
        for t in e.Transiciones:
            if t.SimboloInf is not None and t.SimboloSup is not None:
                if t.SimboloInf <= c <= t.SimboloSup:
                    r.add(t.EdoDestino)
        return r


    def MoverDos(self, e, c):
        r = set()
        for e1 in e:
            for t in e1.Transiciones:
                if t.SimboloInf is not None and t.SimboloSup is not None:
                    if t.SimboloInf <= c <= t.SimboloSup:
                        r.add(t.EdoDestino)
        return r
    
    def IrA(self, e, c):
        return self.CerraduraEpsilonDos(self.MoverDos(e, c))
    
    def Buscar(self, C, conjunto_s):
        for i, Sj in enumerate(C):
            if Sj.s == conjunto_s:
                return i
        return -1

    def ConvertirAAFD(self):
        afd = AFD()
        C = []
        Q = deque()
        NumElemSj = 0

        # Crear el conjunto S0 con la cerradura epsilon del estado inicial
        Sj0 = ElemSj()
        Sj0.s = self.CerraduraEpsilonUno(self.EdoInicial)
        Sj0.id = NumElemSj
        NumElemSj += 1

        C.append(Sj0)
        Q.append(Sj0)

        while Q:
            SjAct = Q.popleft()
            for c in sorted(self.Alfabeto):  # ← alfabeto ordenado
                if c == EPSILON:  # ← saltar epsilon
                    continue
                nuevo_conjunto = self.IrA(SjAct.s, c)
                if not nuevo_conjunto:
                    continue

                NumEdo = self.Buscar(C, nuevo_conjunto)
                if NumEdo == -1:
                    # Nuevo conjunto de estados
                    SjAux = ElemSj()
                    SjAux.s = nuevo_conjunto
                    SjAux.id = NumElemSj
                    NumElemSj += 1
                    C.append(SjAux)
                    Q.append(SjAux)
                    afd.AgregarTransicion(SjAct.id, SjAux.id, c)
                else:
                    afd.AgregarTransicion(SjAct.id, C[NumEdo].id, c)

        # Determinar estados de aceptación
        for Sj in C:
            for e in Sj.s:
                if e.EdoAcept:
                    afd.EdosAceptacion.add(Sj.id)
                    break

        afd.EdoInicial = 0
        afd.Alfabeto = {c for c in self.Alfabeto if c != EPSILON}
        afd.NumEdos = len(afd.EdosAFD)

        # Asignar ids consistentes
        for i, edo in enumerate(afd.EdosAFD):
            edo.id = i

        return afd