# Clase que representa un Nodo del QuadTree

class Nodo:
    def __init__(self, coordenada_x, coordenada_y, longitud_horizontal, longitud_vertical, capacidad_nodo = 1):      # En cada cuadrante solo podrá haber un punto
        self.coordenada_x = coordenada_x                       # Cada Nodo tiene una cordenada en X y en Y                   
        self.coordenada_y = coordenada_y
        self.longitud_horizontal = longitud_horizontal       # Contienen también tiene las dimensiones o medidas del cuadrante
        self.longitud_vertical = longitud_vertical           # donde están ubicados
        self.punto = None          # En punto se guarda la tupla, que es el valor de la coordenada de los puntos de entrega
        self.hijos = None          # En hijos se guarda los nodos a los que apuntará en caso de ser nodo padre, pero si es una hoja, esta variable sigue None
        self.es_hoja = True        # Será False si deja de ser una hoja. Empieza en True, porque al crear un Nodo siempre empieza como hoja
      
                                
    def verificar_si_contiene_punto(self, coordenada_x_punto, coordenada_y_punto): # Función para verificar si un punto (x,y) cae dentro de las dimensiones del Nodo
    
        dentro_rango_en_x = self.coordenada_x <= coordenada_x_punto < self.coordenada_x + self.longitud_horizontal     # Se valida si está dentro del rango en el eje X del Nodo
                                                                                                                           # La coordenada X del punto debe ser mayor o igual a la del inicio (coordenada X del nodo) y menor que la del inicio + la longitud
        dentro_rango_en_y = self.coordenada_y <= coordenada_y_punto < self.coordenada_y + self.longitud_vertical       # Se valida si está dentro el rango en el eje Y del Nodo
                                                                                                                           # La coordenada Y del punto debe ser mayor o igual que la del inicio del Nodo y menor que la del inicio + la longitud
        return dentro_rango_en_x and dentro_rango_en_y  # Si se cumplen las dos, se retorna True
    
    
    def subdividir_nodo(self):   # Esta función divide el Nodo en cuatro cuadrantes hijos
        
        mitad_horizontal = self.longitud_horizontal / 2     # Calcula la mitad del ancho del nodo actual. 
        mitad_vertical =  self.longitud_vertical / 2        # Calcula la mitad de la altura del nodo actual.
        
        hijo_Noroeste = Nodo(self.coordenada_x, self.coordenada_y + mitad_vertical, mitad_horizontal, mitad_vertical)                     # Crea el hijo noroeste: comienza en la izquierda y en la mitad superior
        hijo_Noreste = Nodo(self.coordenada_x + mitad_horizontal, self.coordenada_y + mitad_vertical, mitad_horizontal, mitad_vertical )  # Crea el hijo noreste: comienza en la mitad horizontal y en la mitad superior
        hijo_Suroeste = Nodo(self.coordenada_x, self.coordenada_y, mitad_horizontal, mitad_vertical)                                      # Crea el hijo suroeste: comienza en la esquina inferior izquierda del nodo actual
        hijo_Sureste = Nodo(self.coordenada_x + mitad_horizontal, self.coordenada_y, mitad_horizontal, mitad_vertical)                    # Crea el hijo sureste: comienza en la mitad horizontal y en la parte inferior
        
        self.hijos = [hijo_Noreste, hijo_Noroeste, hijo_Sureste, hijo_Suroeste]
        self.es_hoja = False    # Ahora que se dividió este Nodo deja de ser una hoja, ahora apunta a los Nodos hijos
    
    
    def indice_hijo(self, coordenada_x_punto, coordenada_y_punto):       # Determina cuál de los cuatro hijos contiene las coordenadas del punto.
        
        centro_en_x = self.coordenada_x + self.longitud_horizontal / 2   # Se calcula la coordenada horizontal y vertical del centro del nodo.
        centro_en_y = self.coordenada_y + self.longitud_vertical / 2
        
        derecha = coordenada_x_punto >= centro_en_x     # Es True si el punto está en la mitad derecha o justo en el centro horizontal.
        arriba = coordenada_y_punto >= centro_en_y      # Es True si el punto está en la mitad superior o justo en el centro vertical.

        
        if derecha and arriba:    # Si el punto está arriba  a la derecha, corresponde al hijo_Noreste
            return 0     # Devuelve el índice 0, correspondiente al hijo_Noreste
        
        elif not derecha and arriba:   # Si el punto está arriba a la izquierda, corresponde al hijo_Noroeste
            return 1     # Devuelve el índice 1, correspondiente al hijo_Noroeste
        
        elif derecha and not arriba:   # Si está abajo a la derecha, corresponde al hijo_Sureste
            return 2     # Devuelve el índice 2, correspondiente al hijo_Sureste
        
        elif not derecha and not arriba:     # Si el punto está abajo a la izquierda, corresponde al hijo_Suroeste
            return 3     # Devuelve el índice 3, correspondiente al hijo_Suroeste


    def insertar_punto(self, coordenada_x_punto, coordenada_y_punto):      # Inserta un punto en el nodo actual o en alguno de sus hijos
        
        if not self.verificar_si_contiene_punto(coordenada_x_punto, coordenada_y_punto) :        # Comprueba si el punto está dentro de los límites del nodo actual
            return False   # Si no cumple, se retorna False ya que el punto no se puede insertar en el rango
        
        if self.es_hoja :   # Comprueba si el nodo actual es una hoja, para poder almacenar el punto
            if self.punto is None:    # También se comprueba si hay un punto ya alamcenado
                self.punto = (coordenada_x_punto, coordenada_y_punto)  # Si está vacio, entonces se inserta y se retorna True porque ya se insertó
                return True
            
            if self.punto == (coordenada_x_punto, coordenada_y_punto) : # Si ya habia un punto, se verifica si el que se va a insertar no es el mismo al ya insertado
                return False            

            punto_antiguo = self.punto     # Guarda el punto que ya estaba almacenado.
            self.punto = None              # Y se vacía el punto del Nodo para poder distribuirlos en sus próximos hijos
            self.subdividir_nodo()         # Se divide el Nodo y deja de ser una hoja, ahora tiene 4 cuadrantes (hijos)
            
            coordenada_x_punto_antiguo, coordenada_y_punto_antiguo = punto_antiguo   # Se sacan las coordenadas del punto antiguo
            
            indice_punto_antiguo = self.indice_hijo(coordenada_x_punto_antiguo, coordenada_y_punto_antiguo)     # Se calcula el índice donde se tiene que insertar en alguno de los hijos del Nodo
            
            self.hijos[indice_punto_antiguo].insertar_punto(coordenada_x_punto_antiguo, coordenada_y_punto_antiguo)    # Se inserta en el Nodo hijo correspondiente al índice del punto antiguo, llamando recursivamente la función
            
        indice_punto_nuevo = self.indice_hijo(coordenada_x_punto, coordenada_y_punto)   # Cuando se resuelve la inserción del punto antiguo, se calcula el índice del hijo al que pertenece el nuevo punto.
        return self.hijos[indice_punto_nuevo].insertar_punto(coordenada_x_punto, coordenada_y_punto)   # Inserta el nuevo punto en ese hijo y se devuelve el resultado de la función


    def verificar_si_se_cruza(self, x_min, y_min, x_max, y_max):    # Función auxiliar para verificar si el cuadrado con las dimensiones del rango buscado se cruza con el del Nodo que se está analizando
         
        se_cruza_en_x = self.coordenada_x < x_max and x_min < self.coordenada_x + self.longitud_horizontal   # El tramo de la consulta en X es [x_min, x_max), entonces se verifica: inicio del nodo < fin de la consulta y inicio de la consulta < fin del nodo
        
        se_cruza_en_y = self.coordenada_y < y_max and y_min < self.coordenada_y + self.longitud_vertical   # # El tramo de la consulta en Y es [y_min, y_max), entonces se hace la misma verificación anterior pero en el eje Y
        
        return se_cruza_en_x and se_cruza_en_y      # En caso de que las dos verificaciones se cumplan, se retorna True. Si al menos una no cumple, False.
    
    def consultar_rango(self, x_min, y_min, x_max, y_max, puntos_encontrados = None):   # Función para encontrar los puntos dentro de un rango, o sea los puntos dentro de un cuadrado
                                                                                        # puntos_encontrados se inicializa None, para que cada consulta nueva que no reciba la lista, la cree de nuevo 
        if puntos_encontrados is None:   # Si es una nueva consulta será None
           puntos_encontrados = []       # Se crea la lista donde se guardará el resultado de la consulta
        
        if self.verificar_si_se_cruza(x_min,y_min, x_max, y_max):   # Se verifica que el rango buscado se cruce con el del Nodo actual
            
            if self.es_hoja :        # Si se cruzan, se revisa si el Nodo actual es una hoja
                if self.punto is not None :  # Y si también tiene un punto almacenado, se revisa
                    coordenada_x_punto, coordenada_y_punto = self.punto
                    if x_min <= coordenada_x_punto < x_max and y_min <= coordenada_y_punto < y_max :    # Si las coordenadas del punto están en el rango buscado
                        puntos_encontrados.append(self.punto)    # Se agrega a la lista de encontrados
            else:
                for hijo in self.hijos:        # Si no es una hoja, se revisa el rango buscado en cada uno de sus hijos
                    hijo.consultar_rango(x_min, y_min, x_max, y_max, puntos_encontrados)     # Se llama la función recursivamente, esta vez con la lista de puntos_encontrados de la misma consulta (ya no se le asigna None)
                              
        else:   # Si no se cruzan
            return puntos_encontrados    # se descarta el cuadrante y se devuelve la lista tal y como está.
        
        return puntos_encontrados        # Al finalizar, se retornan todos los puntos encontrados dentro del rango
    
    
    def consultar_en_radio(self, centro_x, centro_y, radio):   # Función para buscar puntos a un radio de un punto específico (centro_x, centro_y), o sea los puntos dentro de este círculo
        
        # Se calculan las coordenadas del cuadrante mínimo que contiene al círculo que se forma con el radio ingresado
        x_min = centro_x - radio     
        x_max = centro_x + radio
        y_min = centro_y - radio
        y_max = centro_y + radio
        
        puntos_candidatos =self.consultar_rango(x_min, y_min, x_max, y_max)   # Los puntos candidatos serán los que estén dentro del cuadrante formado por las coordenadas anteriores
                                                                              # Ya que pueden haber puntos dentro, que no pertenezcan al círculo
        puntos_resultantes = []  # Se inicializa la lista donde se dejarán los puntos correctos
        
        for coordenada_x_punto, coordenada_y_punto in puntos_candidatos:   # Se recorren los puntos de la lista de los candidatos
            distancia = ((coordenada_x_punto - centro_x)**2 + (coordenada_y_punto - centro_y)**2)**(1/2)   # Se calcula la distancia entre el punto y el centro del círculo, con la distancia euclidiana

            if distancia <= radio:  # La distancia entre los puntos y el centro deben ser menor o igual a la del radio para estar dentro
                puntos_resultantes.append((coordenada_x_punto, coordenada_y_punto))   # Los que cumplan, se agregan a la lista
        
        return puntos_resultantes   # Al final se retorna la lista con los puntos al rededor del ingresado en ese radio específico
