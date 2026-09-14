import hashlib
import random
from anytree import Node, RenderTree

class Nodo:                           # Clase para representar los nodos, contiene el hash, y sus hijos izquierdo y derecho
    def __init__(self, hash):
        self.hash = hash
        self.izquierdo = None
        self.derecho = None
         
def calcular_hash(texto):             #Función para calcular el hash de los nodos, sin tener que repetir todo el código cada vez.
    return hashlib.sha256(texto.encode()).hexdigest()


def generar_transacciones(N, nombres):         #Esta función permite generar transacciones aleatorias, todas son de pago, por ejemplo: "Ana pago 180"
    transacciones= []                          # Lista donde se van a guardar las transacciones
    nodos = []
    for i in range(N):
        transaccion = f"{random.choice(nombres)} pago {random.randint(1,1000)}"    # Se genera una transacción escogiendo un nombre aleatorio y un monto aleatorio entre 1 y 1000
        transacciones.append(transaccion)
        print(i+1, transaccion)
        hash_transaccion= calcular_hash(transaccion)    # Se genera el hash de la transacción                
        nodos.append(Nodo(hash_transaccion))            #Se crea un nodo con el hash de la transacción y se agrega a una lista de nodos, donde inicialmente se van a tener solo los nodos de las transacciones
    return nodos, transacciones
                                     
def construir_niveles(nodos):               #Esta función es para construir los niveles del arbol  
    siguiente_nivel = []
    for i in range(0,len(nodos),2):         # Se recorre la lista de nodos de dos en dos

        if i + 1 < len(nodos):              #Se verifica que exista un nodo vecino, para saber cuando se tiene un numero impar de nodos en el nivel
            nodo_actual = nodos[i]          # Nodo actual en el ciclo
            nodo_vecino = nodos[i + 1]      # Nodo que está a su lado
            hash_padre = calcular_hash(nodo_actual.hash +  nodo_vecino.hash)    # Se calcula el hash que forman los dos nodos continuos, quien será su padre
            nodo_padre = Nodo(hash_padre)                                       # Se crea el nodo padre  y se añade a la lista del nivel siguiente.
            nodo_padre.izquierdo = nodo_actual
            nodo_padre.derecho = nodo_vecino
            siguiente_nivel.append(nodo_padre)
        else:
            nodo_actual = nodos[i]               # En caso de que el último nodo no tenga otro a su lado, el número de nodos es impar
            nodo_vecino = Nodo(nodo_actual.hash) # El nodo vecino de este sería el mismo
            nodo_padre = Nodo(calcular_hash(nodo_actual.hash +  nodo_vecino.hash))     # Se calcula su padre con el hash del nodo con el mismo
            nodo_padre.izquierdo = nodo_actual          
            nodo_padre.derecho = nodo_vecino
            siguiente_nivel.append(nodo_padre)
    return siguiente_nivel

def construir_arbol(nodos_nivel_actual):          # Se construye el arbol con la función de construir nivel hasta llegar a la raiz y se retorna
    while len(nodos_nivel_actual) > 1:
        nodos_nivel_actual = construir_niveles(nodos_nivel_actual)
    return nodos_nivel_actual[0]

def convertir_arbol_a_anytree(nodo, padre=None):         # Se convierte el árbol en una estructura de anytree para mostrarlo en la terminal, empieza con None porque la raiz no tiene padre
    nodo_anytree = Node(nodo.hash[:8], parent=padre)     # Se convierte a un nodo de AnyTree y solo se muestran los primeros 8 caracteres de cada nodo
    if nodo.izquierdo:                                   # Si tiene hijo izquierdo también se convierte siendo el padre el nodo_anytree y ya no sería None
        convertir_arbol_a_anytree(nodo.izquierdo, nodo_anytree)     
    if nodo.derecho:                                     # Si tiene hijo derecho también se convierte
        convertir_arbol_a_anytree(nodo.derecho, nodo_anytree)
    return nodo_anytree 

def mostrar_arbol(raiz):
    arbol = convertir_arbol_a_anytree(raiz)
    for pre, __, nodo in RenderTree(arbol):
            print(f"{pre}{nodo.name}")
 
    
def experimento_uno(nodos, transacciones):            # Función para el experimento uno, que se trata de mostrar que la raíz cambia al cambiar una transacción
    raiz_original = construir_arbol(nodos)            # Se construye y guarda la raíz con los nodos de las transacciones originales
    print("\nRaíz original:")                         
    print(raiz_original.hash[:8])               
    print("\nTransacción modificada:")
    transaccion_modificada = "Silvana pago 200000"    # Como no está en la lista de nombres ni en el límite de montos no será igual a las que se pueden generar
    print(transaccion_modificada)
    transacciones[0] = transaccion_modificada         # Para el experimento se modifica la primera transacción
    nodos[0] = Nodo(calcular_hash(transacciones[0]))  # Se modifica la lista de nodos en la primera posición con el hash de la transacción modificada
    raiz_modificada = construir_arbol(nodos)          # Se vuelve a construir el árbol y guarda la nueva raíz
    print("\nÁrbol modificado")
    mostrar_arbol(raiz_modificada)                    
    print("\nRaíz modificada:")                       # Se muestra tanto la raíz original como la modificada para verificar los cambios visualmente
    print(raiz_modificada.hash[:8])
    if raiz_original != raiz_modificada:              # Igualmente el programa verifica si son diferentes y muestra el resultado
        print("\nLa raíz cambió")

        
def experimento_dos(nodos, transacciones):
    raiz_original = construir_arbol(nodos)
    transaccion_3_original = transacciones[2]
    supuesta_transaccion = calcular_hash(input("\nIngrese la transacción 3:"))
    h4 = raiz_original.izquierdo.derecho.derecho.hash
    h34 = calcular_hash(supuesta_transaccion + h4)
    h12 = raiz_original.izquierdo.izquierdo.hash
    h1234 = calcular_hash(h12 + h34)
    h5555 = raiz_original.derecho.hash
    raiz_obtenida = calcular_hash(h1234 + h5555)
    print("\n Resultados:")
    print("\n Raíz original:")
    print(f"\n {raiz_original.hash[:8]}")
    print("\n Raíz obtenida:")
    print(f"\n {raiz_obtenida[:8]}")
    if raiz_original.hash == raiz_obtenida:
        print(f"\nLa transacción 3 es válida")
    else:
        print(f"\nLa transacción 3 no es válida")
    
N = 5
nombres = ["Ana", "Juan", "Pedro", "Maria", "Carlos"]
nodos, transacciones = generar_transacciones(N, nombres)
raiz = construir_arbol(nodos)
print("\nÁrbol original\n")
mostrar_arbol(raiz)
print("Escoge el experimento:")
while True:
    opcion = input("\n1. Modificar un bloque\n2. Verificar el bloque 3\n3. Salir\n")
    if opcion == "1":
        experimento_uno(nodos.copy(), transacciones.copy())
    elif opcion == "2":
        experimento_dos(nodos.copy(), transacciones.copy())
    elif opcion == "3":
        break
    else:
        print("Opción no válida")