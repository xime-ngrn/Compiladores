import Estado
import Transicion

class AFN:
    def __init__(self):
        self.Estados = set()          
        self.EdoInicial = None      
        self.Alfabeto = set()        
        self.EdosAceptacion = set()  

    def CrearBasico(self, c):
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
    
    def CrearBasico(self, c1, c2):
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