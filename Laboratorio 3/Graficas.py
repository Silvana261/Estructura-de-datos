import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# ----------------------------------------------------------------------
# CONFIGURACIÓN: ajusta esto a tus archivos reales
# ----------------------------------------------------------------------
# Tu script 'run_experimentos' guarda un CSV POR EXPERIMENTO dentro de 'datos/'.
# Aquí se listan todos para que este script los lea y los junte en uno solo.
# Si corriste con PRUEBA = True, cambia los nombres para que terminen en "_prueba.csv".
ARCHIVOS_CSV = [
    "datos/e1_insercion.csv",
    "datos/e2_busqueda.csv",
    "datos/e3_listado.csv",
    "datos/e5_rango.csv",
]

CARPETA_SALIDA = "graficas"         # Carpeta donde se guardan las imágenes

# Nombres bonitos para la leyenda y colores fijos (así son consistentes en todas las gráficas)
NOMBRES = {"lista": "Lista", "abb": "ABB", "bmas": "B+"}
COLORES = {"lista": "#e73c9a", "abb": "#b012f3", "bmas": "#2ecc9f"}

# Nombres descriptivos para cada código de experimento (agrega aquí los que uses)
NOMBRES_EXPERIMENTO = {
    "E1": "Inserción",
    "E2": "Búsqueda por ID",
    "E3": "Listado ascendente",
    "E5": "Búsqueda por rango",
}
 
# OJO: debe coincidir exactamente con los valores de ORDENES en tu script de experimentos
NOMBRES_ORDEN = {"aleatorio": "IDs en orden aleatorio", "ordenado": "IDs en orden ascendente"}
 
 
def cargar_datos(archivos):
    # Lee cada CSV (puede que no todos existan si aún no corriste todos los experimentos)
    # y los junta en un solo DataFrame, ya que todos comparten las columnas que usamos aquí
    # (experimento, estructura, orden, N, rep, tiempo_s, altura), aunque E5 tenga columnas
    # adicionales (Q, K) que simplemente no usamos para graficar.
    partes = []
    for archivo in archivos:
        if not os.path.exists(archivo):
            print(f"Aviso: no se encontró '{archivo}', se omite.")
            continue
        partes.append(pd.read_csv(archivo))
 
    if not partes:
        raise FileNotFoundError(
            "No se encontró ninguno de los archivos listados en ARCHIVOS_CSV. "
            "Revisa que ya hayas corrido tu script de experimentos y que los nombres coincidan."
        )
 
    df = pd.concat(partes, ignore_index=True)
    df["tiempo_s"] = pd.to_numeric(df["tiempo_s"], errors="coerce")
    df = df.dropna(subset=["tiempo_s"])
    return df
 
 
def agrupar(df, experimento):
    # Por cada (estructura, orden, N) hay varias repeticiones; sacamos promedio y desviación.
    datos = df[df["experimento"] == experimento]
    resumen = (
        datos.groupby(["estructura", "orden", "N"])["tiempo_s"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )
    return resumen
 
 
def decidir_escala(valores):
    # Si los valores abarcan varios órdenes de magnitud, conviene escala logarítmica.
    # Si no, una escala lineal se lee mejor. Esto se decide automáticamente por experimento.
    valores = valores[valores > 0]
    if len(valores) < 2:
        return "linear"
    razon = valores.max() / valores.min()
    return "log" if razon > 50 else "linear"
 
 
def graficar_subplot(ax, resumen, orden, escala_y):
    datos_orden = resumen[resumen["orden"] == orden]
 
    for estructura in ["lista", "abb", "bmas"]:
        datos_estr = datos_orden[datos_orden["estructura"] == estructura].sort_values("N")
        if datos_estr.empty:
            continue
 
        # errorbar con yerr=std dibuja la barra de desviación estándar sobre cada punto
        ax.errorbar(
            datos_estr["N"],
            datos_estr["mean"],
            yerr=datos_estr["std"],
            label=NOMBRES.get(estructura, estructura),
            color=COLORES.get(estructura),
            marker="o",
            markersize=5,
            capsize=3,
            linewidth=1.8,
        )
 
        # Además de la barra de error, una franja sombreada ±1 desviación estándar,
        # para que la dispersión se note también como "ancho de banda" y no solo como línea vertical.
        ax.fill_between(
            datos_estr["N"],
            datos_estr["mean"] - datos_estr["std"],
            datos_estr["mean"] + datos_estr["std"],
            color=COLORES.get(estructura),
            alpha=0.12,
        )
 
    ax.set_xscale("log")               # el eje N casi siempre conviene en log (abarca 10 a 20000)
    ax.set_yscale(escala_y)
 
    ax.set_xlabel("Tamaño de la entrada (N)")
    ax.set_ylabel("Tiempo (segundos)")
    ax.set_title(NOMBRES_ORDEN.get(orden, orden))
    ax.legend(title="Estructura")
    ax.grid(True, which="both", linestyle="--", alpha=0.4)
 
    # Anotación explícita de la escala usada en cada eje (pedido del profesor)
    texto_escala = f"Escala eje X: logarítmica\nEscala eje Y: {'logarítmica' if escala_y == 'log' else 'lineal'}"
    ax.text(
        0.02, 0.98, texto_escala,
        transform=ax.transAxes, fontsize=8, va="top", ha="left",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8, edgecolor="gray"),
    )
 
 
def graficar_experimento(df, experimento, carpeta_salida):
    resumen = agrupar(df, experimento)
    if resumen.empty:
        return
 
    ordenes_presentes = [o for o in ["aleatorio", "ordenado"] if o in resumen["orden"].unique()]
    if not ordenes_presentes:
        ordenes_presentes = list(resumen["orden"].unique())
 
    # Una sola escala Y para las dos gráficas del mismo experimento, así son comparables entre sí
    escala_y = decidir_escala(resumen["mean"].values)
 
    fig, axes = plt.subplots(1, len(ordenes_presentes), figsize=(7 * len(ordenes_presentes), 6), squeeze=False)
    axes = axes[0]
 
    for ax, orden in zip(axes, ordenes_presentes):
        graficar_subplot(ax, resumen, orden, escala_y)
 
    titulo = NOMBRES_EXPERIMENTO.get(experimento, experimento)
    fig.suptitle(f"{experimento} — {titulo}\n(la franja sombreada y las barras muestran ±1 desviación estándar)",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.92])
 
    os.makedirs(carpeta_salida, exist_ok=True)
    ruta = os.path.join(carpeta_salida, f"{experimento}_{titulo.replace(' ', '_')}.png")
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    print(f"Guardada: {ruta}")
 
 
def graficar_altura(df, carpeta_salida):
    # La altura es una métrica INDEPENDIENTE DE LA MÁQUINA (a diferencia del tiempo),
    # así que vale la pena graficarla aparte: muestra el efecto estructural puro
    # (ABB degenerando con IDs en orden vs B+ manteniéndose balanceado) sin el ruido
    # de hardware que sí afecta a los tiempos.
 
    datos = df.copy()
    datos["altura"] = pd.to_numeric(datos["altura"], errors="coerce")   # "" (de la Lista) se vuelve NaN
    datos = datos.dropna(subset=["altura"])
 
    if datos.empty:
        print("No hay datos de altura para graficar (revisa que ABB y B+ tengan la columna 'altura' llena).")
        return
 
    # La altura no depende de qué experimento la midió (E1, E2, E3...), es una propiedad
    # del árbol ya construido. Usamos el primer experimento disponible que tenga esta columna.
    experimento_usado = sorted(datos["experimento"].unique())[0]
    datos = datos[datos["experimento"] == experimento_usado]
 
    resumen = (
        datos.groupby(["estructura", "orden", "N"])["altura"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )
 
    ordenes_presentes = [o for o in ["aleatorio", "ordenado"] if o in resumen["orden"].unique()]
    if not ordenes_presentes:
        ordenes_presentes = list(resumen["orden"].unique())
 
    escala_y = decidir_escala(resumen["mean"].values)
 
    fig, axes = plt.subplots(1, len(ordenes_presentes), figsize=(7 * len(ordenes_presentes), 6), squeeze=False)
    axes = axes[0]
 
    for ax, orden in zip(axes, ordenes_presentes):
        datos_orden = resumen[resumen["orden"] == orden]
 
        for estructura in ["abb", "bmas"]:        # la Lista no tiene altura, se omite a propósito
            datos_estr = datos_orden[datos_orden["estructura"] == estructura].sort_values("N")
            if datos_estr.empty:
                continue
 
            ax.errorbar(
                datos_estr["N"], datos_estr["mean"], yerr=datos_estr["std"],
                label=NOMBRES.get(estructura, estructura), color=COLORES.get(estructura),
                marker="o", markersize=5, capsize=3, linewidth=1.8,
            )
            ax.fill_between(
                datos_estr["N"], datos_estr["mean"] - datos_estr["std"], datos_estr["mean"] + datos_estr["std"],
                color=COLORES.get(estructura), alpha=0.12,
            )
 
        ax.set_xscale("log")
        ax.set_yscale(escala_y)
        ax.set_xlabel("Tamaño de la entrada (N)")
        ax.set_ylabel("Altura del árbol (niveles)")
        ax.set_title(NOMBRES_ORDEN.get(orden, orden))
        ax.legend(title="Estructura")
        ax.grid(True, which="both", linestyle="--", alpha=0.4)
 
        texto_escala = f"Escala eje X: logarítmica\nEscala eje Y: {'logarítmica' if escala_y == 'log' else 'lineal'}"
        ax.text(0.02, 0.98, texto_escala, transform=ax.transAxes, fontsize=8, va="top", ha="left",
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.8, edgecolor="gray"))
 
    fig.suptitle(
        f"Altura del árbol vs N  (datos de {experimento_usado})\n"
        "(métrica independiente de la máquina; la franja sombreada muestra ±1 desviación estándar)",
        fontsize=12,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.92])
 
    os.makedirs(carpeta_salida, exist_ok=True)
    ruta = os.path.join(carpeta_salida, "altura_vs_N.png")
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    print(f"Guardada: {ruta}")
 
 
def main():
    df = cargar_datos(ARCHIVOS_CSV)
 
    experimentos_presentes = sorted(df["experimento"].unique())
    print(f"Experimentos encontrados en el CSV: {experimentos_presentes}")
 
    for experimento in experimentos_presentes:
        graficar_experimento(df, experimento, CARPETA_SALIDA)
 
    graficar_altura(df, CARPETA_SALIDA)
 
 
if __name__ == "__main__":
    main()
 