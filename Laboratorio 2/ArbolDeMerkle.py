import hashlib
import random
from anytree import Node, RenderTree

class Nodo:                           # Clase para representar los nodos, contiene el hash y sus hijos izquierdo y derecho
    def __init__(self, hash):
        self.hash = hash
        self.izquierdo = None
        self.derecho = None
         
def calcular_hash(texto):             #Función para calcular el hash de los nodos con SHA 256, sin tener que repetir todo el código cada vez que se calcule un hash.
    return hashlib.sha256(texto.encode()).hexdigest()

def generar_transacciones(N, nombres):         #Esta función permite generar transacciones aleatorias, todas son de pago, por ejemplo: "Ana pago 180". Recibe el número de transacciones y una lista de nombres.
    transacciones= []                          # Lista donde se van a guardar las transacciones
    nodos = []                                 # Lista donde van a estar todos los nodos del árbol
    for i in range(N):
        transaccion = f"{random.choice(nombres)} pago {random.randint(1,1000)}"    # Se genera una transacción escogiendo un nombre aleatorio de la lista y un monto aleatorio entre 1 y 1000
        transacciones.append(transaccion)                                   
        print(i+1, transaccion)                         # Las transacciones se muestran mientras se crean.
        hash_transaccion= calcular_hash(transaccion)    # Se genera el hash de la transacción                
        nodos.append(Nodo(hash_transaccion))            #Se crea un nodo con el hash de la transacción y se agrega a la lista de nodos, donde inicialmente se van a tener solo los nodos de las transacciones.
    return nodos, transacciones                         # Se retorna la lista de los nodos y de las transacciones
                                     
def construir_niveles(nodos):               #Esta función es para construir los niveles del arbol y recibe los nodos con los que hará los niveles
    siguiente_nivel = []
    for i in range(0,len(nodos),2):         # Se recorre la lista de nodos de dos en dos, ya que cada pareja creará un nodo padre

        if i + 1 < len(nodos):              #Se verifica que exista un nodo vecino, para saber cuando se tiene un numero impar de nodos en el nivel
            nodo_actual = nodos[i]          # Nodo actual en el ciclo
            nodo_vecino = nodos[i + 1]      # Nodo que está a su lado
            hash_padre = calcular_hash(nodo_actual.hash +  nodo_vecino.hash)    # Se calcula el hash que forman los dos nodos, quien será su padre
            nodo_padre = Nodo(hash_padre)                                       # Se crea el nodo padre  y se añade a la lista del nivel siguiente.
            nodo_padre.izquierdo = nodo_actual      # Se asignan los hijos del nodo, el de la izquierda será el nodo actual
            nodo_padre.derecho = nodo_vecino        # Su hijo a la derecha será el vecino del nodo actual
            siguiente_nivel.append(nodo_padre)
        else:
            nodo_actual = nodos[i]               # En caso de que el último nodo no tenga otro a su lado, el número de nodos es impar
            nodo_vecino = Nodo(nodo_actual.hash) # El nodo vecino de este será el mismo, por lo que se hace una copia de este
            nodo_padre = Nodo(calcular_hash(nodo_actual.hash +  nodo_vecino.hash))     # Se calcula su padre con el hash del nodo con su duplicado
            nodo_padre.izquierdo = nodo_actual   # Se asignan los hijos izquierdo y derecho, quienes son el nodo y su duplicado    
            nodo_padre.derecho = nodo_vecino
            siguiente_nivel.append(nodo_padre)   # Se agrega al siguiente nivel
    return siguiente_nivel

def construir_arbol(nodos_nivel_actual):         # Se construye el arbol con ayuda de la función de construir_niveles hasta llegar a la raiz y se retorna
    while len(nodos_nivel_actual) > 1:           # Se continua mientras hayan más de un nodo en el nivel, ya que en la raíz solo habrá uno
        nodos_nivel_actual = construir_niveles(nodos_nivel_actual)    # La función construir_niveles devuelve el siguiente nivel, por lo que va subiendo hasta llegar a la raíz
    return nodos_nivel_actual[0]      # Se retorna la raíz quién es la que queda en la variable de nodos_nivel_actual


def convertir_arbol_a_anytree(nodo, padre=None):           # Esta función recibe a la raiz y convierte el árbol en una estructura compatible con la librería anytree para mostrarlo en la terminal, empieza con padre=None porque la raiz no tiene padre
    nodo_a_mostrar = Node(nodo.hash[:8], parent=padre)     # Se convierte a un nodo de AnyTree, el nombre del nodo son los primeros 8 caracteres de su hash y su nodo padre
    if nodo.izquierdo:                                     # Si tiene hijo izquierdo también se convierte, siendo el padre el nodo_a_mostrar y ya no sería None
        convertir_arbol_a_anytree(nodo.izquierdo, nodo_a_mostrar)     
    if nodo.derecho:                                     # Si tiene hijo derecho también se convierte
        convertir_arbol_a_anytree(nodo.derecho, nodo_a_mostrar)
    return nodo_a_mostrar     # Se retorna el nodo convertido a AnyTree

def mostrar_arbol(raiz):                          # Función para mostrar el árbol en la terminal y recibe la raiz del árbol.
    arbol = convertir_arbol_a_anytree(raiz)       # Se convierte el árbol a un AnyTree para que RenderTree pueda mostrarlo, se guarda su raiz.
    for pre, __, nodo in RenderTree(arbol):       # RenderTree recorre todos los nodos y asigna a pre los símbolos de las ramas del respectivo nodo, __ es información sobre el nivel del nodo (la cual no se muestra)
            print(f"{pre}{nodo.name}")            # Se imprime las ramas y el nombre del nodo, que es el hash 


def experimento_uno(nodos, transacciones):            # Función para  mostrar que la raíz cambia al cambiar una transacción, recibe las transacciones y sus nodos
    raiz_original = construir_arbol(nodos)            # Se construye y guarda la raíz con los nodos de las transacciones originales
    print("\nRaíz original:")                         
    print(raiz_original.hash[:8])               
    print("\n La primera transacción será modificada por:")
    transaccion_modificada = "Silvana pago 200000"    # Como no está en la lista de nombres ni en el límite de montos no será igual a las que se pueden generar
    print(transaccion_modificada)
    transacciones[0] = transaccion_modificada         # Para el experimento se modifica la primera transacción de la lista
    nodos[0] = Nodo(calcular_hash(transacciones[0]))  # Se modifica la lista de nodos en la primera posición con el hash de la transacción modificada
    raiz_modificada = construir_arbol(nodos)          # Se vuelve a construir el árbol y guarda la nueva raíz
    print("\nÁrbol modificado")
    mostrar_arbol(raiz_modificada)                    
    print("\nRaíz modificada:")                       # Se muestra tanto la raíz original como la modificada para verificar los cambios visualmente
    print(raiz_modificada.hash[:8])
    if raiz_original != raiz_modificada:              # Igualmente el programa verifica si son diferentes y muestra el resultado
        print("\nLa raíz cambió")

        
def experimento_dos(nodos, transacciones):             # Función para la prueba de inclusión del bloque 3, recibe las transacciones y sus nodos
    raiz_original = construir_arbol(nodos)             # Se construye el árbol original y se guarda su raíz
    transaccion_3_original = transacciones[2]          
    supuesta_transaccion = calcular_hash(input("\nIngrese la transacción 3:"))    # Se pide la transacción 3 que se cree que es la original
    h4 = raiz_original.izquierdo.derecho.derecho.hash                # Para reconstruir el árbol se obtienen los hashes necesarios: h4, h12 y h5555(ya que ese nodo se duplicó)
    h34 = calcular_hash(supuesta_transaccion + h4)                   # Y se calculan los otros hashes (h34, h1234, raiz) que tienen que ver con la transacción 3 ingresada para llegar a la raiz
    h12 = raiz_original.izquierdo.izquierdo.hash                     
    h1234 = calcular_hash(h12 + h34)
    h5555 = raiz_original.derecho.hash
    raiz_obtenida = calcular_hash(h1234 + h5555)                     
    print("\n Resultados:")                                          # Se muestra la raíz original y la obtenida de reconstruir el árbol
    print("\n Raíz original:")
    print(f"\n {raiz_original.hash[:8]}")
    print("\n Raíz obtenida:")
    print(f"\n {raiz_obtenida[:8]}")
    if raiz_original.hash == raiz_obtenida:                          # Se comparan las raíces y si son iguales se muestra que la transacción es válida
        print(f"\nLa transacción 3 es válida")
    else:
        print(f"\nLa transacción 3 no es válida")                   # Si no son iguales, se muestra también el resultado

# EXPERIMENTOS  
N = 5       # Número de transacciones
nombres = ["Ana", "Juan", "Pedro", "Maria", "Carlos"]           # Lista de nombres para escoger aleatoriamente
nodos, transacciones = generar_transacciones(N, nombres)        # Se generan las transacciones y los nodos (hojas) que generan
raiz = construir_arbol(nodos)                                   # Se construye el árbol y se guarda la raíz
print("\nÁrbol original\n")                                     # Se muestra el árbol original y también se muestra la raíz
mostrar_arbol(raiz)
print(f"\n Raíz del arbol:\n{raiz.hash} ")
print("\nEXPERIMENTO UNO: MODIFICAR UN BLOQUE")                 
experimento_uno(nodos.copy(), transacciones.copy())             # Se corre el experimento uno y dos con una copia de los nodos y las transacciones para no modificar directamente los originales
print("\nEXPERIMENTO DOS: PRUEBA DE INCLUSIÓN DEL BLOQUE 3")
experimento_dos(nodos.copy(), transacciones.copy())