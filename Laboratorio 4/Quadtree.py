# Clase que representa un Nodo del QuadTree

class Nodo:
    def __init__(self, coordenada_x, coordenada_y, longitud_horizontal, longitud_vertical, capacidad_nodo = 1):      # En cada cuadrante solo podrá haber un nodo
        self.coordenada_x = coordenada_x                       # Cada Nodo tiene una cordenada en X y en Y                   
        self.coordenada_y = coordenada_y
        self.longitud_horizontal = longitud_horizontal       # Contienen también tiene las dimensiones o medidas del cuadrante
        self.longitud_vertical = longitud_vertical           # donde están ubicados
        self.punto = None          # En punto se guarda la tupla, que es el valor de la coordenada de los puntos de entrega
        self.hijos = None          # En hijos se guarda los nodos a los que apuntará en caso de ser nodo padre, pero si es una hoja, esta variable sigue None
        self.es_hoja = True        # Será False si deja de ser una hoja. Empieza en True, porque al crear un Nodo siempre empieza como hoja
                                
    def verficar_si_contiene_punto(self, coordenada_x_punto, coordenada_y_punto): # Función para verificar si el punto cae dentro de las dimensiones del Nodo
        # En esta variable booleana calcula si 
        dentro_rango_en_x = self.coordenada_x <= self.coordenada_x_punto < self.cordenada_x + self.longitud_horizontal
        dentro_rango_en_y = self.coordenada_y <= self.coordenada_y_punto < self.cordenada_y + self.longitud_horizontal
        return dentro_rango_en_x and dentro_rango_en_y
    
    def subdividir_nodo(self):
        
        mitad_horizontal = self.longitud_horizontal / 2
        mitad_vertical =  self.longitud_vertical / 2
        
        hijo_Noreste = Nodo(self.coordenada_x, self.coordenada_y + mitad_vertical, mitad_horizontal, mitad_vertical)
        hijo_Noroeste = Nodo(self.coordenada_x + mitad_horizontal, self.coordenada_y + mitad_vertical, mitad_horizontal, mitad_vertical )
        hijo_Sureste = Nodo(self.coordenada_x, self.coordenada_y, mitad_horizontal, mitad_vertical)
        hijo_Suroeste = Nodo(self.coordenada_x + mitad_horizontal, self.coordenada_y, mitad_horizontal, mitad_vertical)
        
        self.hijos = [hijo_Noreste, hijo_Noroeste, hijo_Sureste, hijo_Suroeste]
        self.es_hoja = False
    
    def indice_hijo(self, coordenada_x_punto, coordenada_y_punto):
        
        centro_en_x = self.coordenada_x + self.longitud_horizontal / 2
        centro_en_y = self.coordenada_y + self.longitud_vertical / 2
        
        derecha = coordenada_x_punto >= centro_en_x
        arriba = coordenada_y_punto >= centro_en_y
        
        if not derecha and arriba:
            return 0
        elif derecha and arriba:
            return 1 
        elif not derecha and not arriba:
            return 2
        elif derecha and not arriba:
            return 3

    def insertar_punto(self, coordenada_x_punto, coordenada_y_punto):
        
        if not self.verficar_si_contiene_punto(coordenada_x_punto, coordenada_y_punto):
            return False
        
        if self.es_hoja:
            if self.punto is None:
                self.punto = (coordenada_x_punto, coordenada_y_punto)
                return True
            if self.punto == (coordenada_x_punto, coordenada_y_punto):
                return False            

            punto_actual = self.punto
            self.punto = None
            self.subdividir_nodo()
            
            coordenada_x_punto_actual, coordenada_y_punto_actual = punto_actual
            indice_punto_actual = self.indice_hijo(coordenada_x_punto_actual, coordenada_y_punto_actual)
            self.hijos[indice_punto_actual].insertar_punto(coordenada_x_punto_actual, coordenada_y_punto_actual)
            
        indice_punto_nuevo = self.indice_hijo(coordenada_x_punto, coordenada_y_punto)
        return self.hijos[indice_punto_nuevo].insertar_punto(coordenada_x_punto, coordenada_y_punto)