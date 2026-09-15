### Laboratorio 2

**Árbol de Merkle** utilizando hashes SHA-256.

El programa permite:

* Generar transacciones aleatorias y calcular su hash.
* Construir el árbol por niveles a través de la clase nodo.
* Manejar cantidades impares de nodos duplicando el último nodo.
* Mostrar gráficamente el árbol en la terminal utilizando `AnyTree`.
* Obtener y mostrar la raíz del árbol.
<img width="1136" height="591" alt="image" src="https://github.com/user-attachments/assets/32b3e25c-a189-446d-a657-ffd772a33ac9" />


#### Experimento 1: Modificar un bloque

Se modifica una de las transacciones originales y se vuelve a construir el árbol. Se comparan las raíces para demostrar que al cambiar una transacción también cambia la raíz del Árbol de Merkle.
<img width="720" height="632" alt="image" src="https://github.com/user-attachments/assets/7d8566cd-73ba-4ae3-8f06-4518dc37af52" />


#### Experimento 2: Prueba de inclusión del bloque 3

Se solicita una posible transacción para el bloque 3 y, mediante los hashes necesarios, se reconstruye la ruta hasta la raíz. Finalmente, se compara la raíz obtenida con la raíz original para determinar si la transacción pertenece al árbol.
* Caso válido:
<img width="668" height="497" alt="image" src="https://github.com/user-attachments/assets/e2757318-9159-46fe-99af-53af84c0a75a" />

* Caso inválido:
<img width="781" height="500" alt="image" src="https://github.com/user-attachments/assets/1a30d18c-c107-4b07-bf82-92dba6bb0a81" />



## Uso de Inteligencia Artificial

Se utilizó Inteligencia Artificial como herramienta de apoyo durante el desarrollo del laboratorio para encontrar librerías y para:

* Comprender y descubrir el uso de `random.choice()` para seleccionar aleatoriamente un nombre de una lista.
* Comprender la implementación de la librería **AnyTree** y el uso de `RenderTree` para mostrar el Árbol de Merkle gráficamente en la terminal.
* Comprender cómo utilizar funciones recursivas para recorrer y convertir los nodos del árbol a la estructura de **AnyTree y RenderTree **.
* Identificar y solucionar errores durante el desarrollo del programa, utilizando la IA como apoyo para localizar de manera más rápida posibles problemas en el código y comprender cómo corregirlos.
