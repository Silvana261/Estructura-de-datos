class NodoABB:                       # Clase que representa un nodo del árbol ABB
    def __init__(self, estudiante):
        self.estudiante= estudiante  # Cada nodo contiene al dato estudiante completo, no solo una referencia
        self.izquierda = None        # Hijo izquierdo
        self.derecha = None          # Hijo derecho
        
    
class ABB:                             # Esta clase representa el árbol ABB y define las funciones para insertar y buscar estudiantes
    def __init__(self):
        self.raiz = None               # Al crear el árbol, la raíz es None ya que no hay ningún nodo aún.

    def insertarABB(self, estudiante):    # Para insertar se recibe al estudiante
        nuevo = NodoABB(estudiante)    # Se convierte en un NodoABB

        if self.raiz is None:          # Si no existe raíz, este será asignado como la raíz
            self.raiz = nuevo
            return

        nodo_actual = self.raiz             # Si ya hay una raíz del árbol, comenzamos a recorrerlo desde la misma

        while True:                    # Se repite el ciclo hasta encontrar una posición para el nodo
            if estudiante.id < nodo_actual.estudiante.id:     # Si el id es menor al del nodo_actual, se busca en la izquierda de este

                if nodo_actual.izquierda is None:             # Si el actual no tiene hijo por la izquierda
                    nodo_actual.izquierda = nuevo             # Se inserta el nuevo allí
                    return

                nodo_actual = nodo_actual.izquierda           # Si ya estaba ocupado el lugar del hijo izquierdo, bajamos un nivel a la izquierda

            else:                                             # Si el id del nuevo estudiante es mayor o igual al del nodo actual

                if nodo_actual.derecha is None:               # Se verifica si el actual tiene hijo a la derecha
                    nodo_actual.derecha = nuevo               # Si no tiene, se asigna el nuevo como su hijo derecho
                    return

                nodo_actual = nodo_actual.derecha             # Si tiene, entonces se baja un nivel a la derecha para seguir buscando

    def buscarABB(self, id):                    # Para buscar un estudiante, se recibe su id
        est_actual = self.raiz                      # Se empieza a buscar desde la raíz

        while est_actual is not None:               # El ciclo sigue hasta que se quede sin nodos por revisar

            if id == est_actual.estudiante.id:      # Si el id del estudiante actual coincide con el buscado, se retorna el objeto Estudiante
                return est_actual.estudiante        

            if id < est_actual.estudiante.id:       # Si el id es menor al del estudiante actual
                est_actual = est_actual.izquierda   # Buscamos a la izquierda
            else:
                est_actual = est_actual.derecha     # Si es mayor al del estudiante actual, buscamos a la derecha

        return None  # Si no se encuentra se retorna None
    
    def listarEnOrden(self):
        estudiantes_ordenados = []     # Lista donde vamos a guardar los estudiantes ordenados

        pila = []    # Pila para recorrer el árbol
        
        nodo_actual = self.raiz    # Comenzamos desde la raíz

        while nodo_actual is not None or len(pila) > 0:  # Recorremos mientras haya nodos por revisar

            while nodo_actual is not None:      # Bajamos todo lo posible por la izquierda
                pila.append(nodo_actual)        
                nodo_actual = nodo_actual.izquierda

            nodo_actual = pila.pop()     # Sacamos el último nodo guardado

            estudiantes_ordenados.append(nodo_actual.estudiante)     # Agregamos el estudiante a la lista

            nodo_actual = nodo_actual.derecha   # Continuamos por la derecha

        return estudiantes_ordenados   # Retornamos la lista ordenada
    
    def altura(self):
        if self.raiz is None:         # Si la raíz no apunta a nada, el árbol está vacío y la altura es cero
            return 0
        nivel = [self.raiz]           # nivel es una lista que contiene los nodos del nivel actual (empezando con la raíz) que se van a procesar
        altura = 0                    # Inicializar variable altura
        while nivel:                  # Se recorre la lista nivel, mientras aún tenga nodos que analizar
            altura += 1               # Cada vuelta que da el ciclo, significa bajar un nivel, por lo que se aumenta la altura
            siguiente = []
            for nodo in nivel:        # Se recorren los nodos del nivel actual
                if nodo.izquierda is not None:          # Si tiene hijos por la izquiera o derecha, se añaden al siguiente nivel
                    siguiente.append(nodo.izquierda)
                if nodo.derecha is not None:
                    siguiente.append(nodo.derecha)
            nivel = siguiente         # Una vez que todos los hijos del nivel actual están en siguiente, se actualiza como nivel actual
        return altura
    def buscarRango(self, a, b):
        resultado = []
        pila = []
        nodo = self.raiz
        while nodo is not None or len(pila) > 0:
            while nodo is not None:
                pila.append(nodo)
                if nodo.estudiante.id > a:       # Solo se baja a la izquierda si ahí puede haber IDs >= a
                    nodo = nodo.izquierda
                else:
                    nodo = None
            nodo = pila.pop()
            id_actual = nodo.estudiante.id
            if id_actual > b:                    # En recorrido en orden, todo lo que sigue es mayor que b
                break
            if id_actual >= a:
                resultado.append(nodo.estudiante)
            if id_actual < b:                    # Solo se baja a la derecha si ahí puede haber IDs <= b
                nodo = nodo.derecha
            else:
                nodo = None
        return resultado