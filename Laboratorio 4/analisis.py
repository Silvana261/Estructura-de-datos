import random
# Funciones para generar los puntos

def generar_puntos_uniformes(cantidad, ancho_ciudad, largo_ciudad ): # Función para generar los puntos (x,y) de manera aleatoria en una ciudad con ciertas dimensiones
    puntos = []   # Lista donde se almacenarán los puntos
    
    for i in range(cantidad):  # Se hace un ciclo para generar la cantidad de puntos que se quiera 
        x = random.uniform(0, ancho_ciudad)   # Se genera la coordenada x, como un número entre 0 y el ancho máximo de la ciudad
        y = random.unidorm(0, largo_ciudad)   # Se genera la coordenada y, como un número aleatorio entre 0 y el largo máximo de la ciudad
        puntos.append((x,y))    # Se agrega la tupla a la lista
    return puntos # se retorna la lista con todo los puntos de entrega

def generar_puntos_realistas(cantidad, ancho_ciudad, largo_ciudad, dispersion_barrio ):    # Genera los puntos de manera más realista en una ciudad (unos más agrupados que otros)
                                                                                           # Gran parte de los puntos se concentran alrededor de las coordenadas de unos barrio predefinidos
                                                                                           # Y el resto de manera uniforme por la ciudad
    
    barrios = [(5000, 5000), (14000, 6000), (10000, 15000), (16000, 16000)]  # Coordenadas del centro de unos barrios artificiales, que serían como los lugares principales
    puntos = []   # Se inicializa la lista donde se almacenarán los puntos
    
    while len(puntos) < cantidad:  # Se hace un ciclo que se repite hasta alcanzar la cantidad de puntos deseados
        
        if random.random() < 0.8:  # Cada punto tiene 80% de probabilidad de caer en uno de los barrios
            centro_x, centro_y = random.choice(barrios)     # Se escoge un barrio aleatoriamente
            x = random.gauss(centro_x,dispersion_barrio)    # Se genera la coordenada x aleatoriamente utilizando distribución gaussiana
            y = random.gauss(centro_y, dispersion_barrio)   # Igualmente, la coordenada y con dispersión gaussiana
        else:   # Y el 20% de los datos se generan aleatoriamente por toda la ciudad
            x = random.uniform(0, ancho_ciudad)
            y = random.uniform(0, largo_ciudad)
            
        if 0 <= x < ancho_ciudad and 0 <= y < largo_ciudad:   # Se valida que el punto caiga dentro de los límites de la ciudad 
            puntos.append((x,y))   # Si está bien, se agrega a la lista
    return puntos
