## Laboratorio 2

**Árbol de Merkle** utilizando hashes SHA-256.

El programa permite:

* **Generar transacciones aleatorias:** se generan `N` transacciones seleccionando aleatoriamente un nombre de una lista y una cantidad entre 1 y 1000. Todas tienen el formato `"(nombre) pago (cantidad)"`, por ejemplo: `"Ana pago 180"`. A cada transacción se le calcula su hash SHA-256, que representa las hojas iniciales del árbol.
* **Construir el árbol por niveles:** se agrupan los nodos de dos en dos y se calcula el hash de la concatenación de sus hashes para crear el nodo padre. Este proceso se repite hasta obtener un único nodo, que corresponde a la raíz.
* **Manejar cantidades impares de nodos:** cuando un nivel tiene una cantidad impar de nodos, se duplica el último nodo para poder formar su nodo padre.
* **Representar los nodos:** cada nodo almacena su hash y tiene referencias a su hijo izquierdo y derecho mediante la clase `Nodo`.
* **Mostrar el árbol en la terminal:** se convierte la estructura del árbol a `AnyTree` y se utiliza `RenderTree` para mostrar visualmente las relaciones entre padres e hijos. Para facilitar la lectura, se muestran únicamente los primeros 8 caracteres de cada hash.
* **Obtener la raíz:** después de construir todos los niveles, se obtiene el único nodo restante como raíz y se muestra su hash completo.

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
* Comprender cómo utilizar funciones recursivas para recorrer y convertir los nodos del árbol a la estructura de AnyTree y RenderTree.
* Identificar y solucionar errores durante el desarrollo del programa, utilizando la IA como apoyo para localizar de manera más rápida posibles problemas en el código y comprender cómo corregirlos.
