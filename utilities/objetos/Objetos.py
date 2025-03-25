# Esta clase contiene el objeto que se usa en el Archivo GraficasGenerales para almacenar
# las rutas de las pruebas inicial y final

class ResultadoAprendizaje():
    
    RutaInicial = ""
    RutaFinal = ""
    
    def __init__(self):
        self.RutaInicial = ""
        self.RutaFinal = ""
    
    def getRutaInicial(self):
        return self.RutaInicial
    def getRutaFinal(self):
        return self.RutaFinal
    
    def setRutaInicial(self, ruta):
        self.RutaInicial = ruta
    def setRutaFinal(self, ruta):
        self.RutaFinal = ruta
