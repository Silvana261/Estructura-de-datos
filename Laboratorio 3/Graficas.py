import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ARCHIVOS_CSV = [
    "datos/e1_insercion.csv",
    "datos/e2_busqueda.csv",
    "datos/e3_listado.csv",
    "datos/e5_rango.csv",
]

CARPETA_SALIDA = "graficas"

# La pendiente se calcula solo con N >= N_MIN_AJUSTE, valor fijado antes de ver los resultados.
# Con N pequeños el tiempo es de microsegundos y lo dominan costos fijos, no el algoritmo.
N_MIN_AJUSTE = 1000

NOMBRES = {"lista": "Lista", "abb": "ABB", "bmas": "B+"}
COLORES = {"lista": "#e73c9a", "abb": "#b012f3", "bmas": "#2ecc9f"}

NOMBRES_EXPERIMENTO = {
    "E1": "Inserción",
    "E2": "Búsqueda por ID",
    "E3": "Listado ascendente",
    "E5": "Búsqueda por rango",
}

NOMBRES_ORDEN = {"aleatorio": "IDs en orden aleatorio", "ordenado": "IDs en orden ascendente"}


def cargar_datos(archivos):
    partes = []
    for archivo in archivos:
        if not os.path.exists(archivo):
            print(f"Aviso: no se encontró '{archivo}', se omite.")
            continue
        partes.append(pd.read_csv(archivo))

    if not partes:
        raise FileNotFoundError("No se encontró ninguno de los CSV. Corre primero los experimentos.")

    df = pd.concat(partes, ignore_index=True)
    df["tiempo_s"] = pd.to_numeric(df["tiempo_s"], errors="coerce")
    df = df.dropna(subset=["tiempo_s"])
    return df


def contar_atipicos(tiempos):
    # Regla de Tukey sobre las repeticiones de un mismo (estructura, orden, N):
    # una repetición se MARCA como atípica si queda fuera de [Q1 - 1.5*IQR, Q3 + 1.5*IQR].
    # Solo se cuentan para reportarlas; NO se descartan.
    q1, q3 = tiempos.quantile(0.25), tiempos.quantile(0.75)
    iqr = q3 - q1
    return int(((tiempos < q1 - 1.5 * iqr) | (tiempos > q3 + 1.5 * iqr)).sum())


def agrupar(df, experimento):
    # Por cada (estructura, orden, N): promedio y desviación estándar de TODAS las repeticiones.
    # Las repeticiones atípicas se conservan; solo se cuenta cuántas hay para reportarlas.
    datos = df[df["experimento"] == experimento]
    filas = []
    marcadas = 0
    for (estr, orden, n), g in datos.groupby(["estructura", "orden", "N"]):
        t = g["tiempo_s"]
        marcadas += contar_atipicos(t)
        filas.append({"estructura": estr, "orden": orden, "N": n,
                      "mean": t.mean(), "std": t.std(), "count": len(t)})
    print(f"{experimento}: {marcadas} de {len(datos)} repeticiones marcadas como atípicas (se conservan)")
    return pd.DataFrame(filas)


def agrupar_altura(df):
    # La altura es una propiedad estructural del árbol, no una medición con ruido.
    datos = df.copy()
    datos["altura"] = pd.to_numeric(datos["altura"], errors="coerce")
    datos = datos.dropna(subset=["altura"])
    if datos.empty:
        return datos
    datos = datos[datos["experimento"] == sorted(datos["experimento"].unique())[0]]
    return (datos.groupby(["estructura", "orden", "N"])["altura"]
            .agg(["mean", "std", "count"]).reset_index())


def calcular_pendiente(N, valores):
    # Pendiente de la regresión log10(N) vs log10(valores), usando solo N >= N_MIN_AJUSTE.
    # Es el exponente k de valores ≈ c * N^k. Se calcula siempre, sin importar la escala del eje Y.
    N = np.asarray(N, dtype=float)
    valores = np.asarray(valores, dtype=float)
    m = (N >= N_MIN_AJUSTE) & (valores > 0)
    if m.sum() < 3:
        return None
    pendiente, _ = np.polyfit(np.log10(N[m]), np.log10(valores[m]), 1)
    return pendiente


def graficar_subplot(ax, resumen, orden, escala_y, ylabel, estructuras):
    datos_orden = resumen[resumen["orden"] == orden]

    for estructura in estructuras:
        d = datos_orden[datos_orden["estructura"] == estructura].sort_values("N")
        if d.empty:
            continue

        pendiente = calcular_pendiente(d["N"], d["mean"])
        etiqueta = NOMBRES.get(estructura, estructura)
        if pendiente is not None:
            etiqueta += f" (pendiente≈{pendiente:.2f})"

        # La banda inferior se limita para que nunca llegue a 0 o negativo (se rompe en escala log).
        std = d["std"].fillna(0)
        inferior = np.maximum(d["mean"] - std, d["mean"] * 0.01)
        superior = d["mean"] + std

        ax.errorbar(
            d["N"], d["mean"], yerr=np.vstack([d["mean"] - inferior, superior - d["mean"]]),
            label=etiqueta, color=COLORES.get(estructura),
            marker="o", markersize=5, capsize=3, linewidth=1.8,
        )
        ax.fill_between(d["N"], inferior, superior, color=COLORES.get(estructura), alpha=0.12)

    ax.set_xscale("log")
    ax.set_yscale(escala_y)
    ax.set_xlabel("Tamaño de la entrada (N)")
    ax.set_ylabel(ylabel)
    ax.set_title(NOMBRES_ORDEN.get(orden, orden))
    ax.legend(title=f"Estructura (pendiente con N ≥ {N_MIN_AJUSTE})")
    ax.grid(True, which="both", linestyle="--", alpha=0.4)

    texto = "Escala eje X: logarítmica\nEscala eje Y: logarítmica"
    ax.text(0.02, 0.98, texto, transform=ax.transAxes, fontsize=8, va="top", ha="left",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8, edgecolor="gray"))


def hacer_figura(resumen, titulo, ylabel, ruta, estructuras):
    ordenes = [o for o in ["aleatorio", "ordenado"] if o in resumen["orden"].unique()]
    escala_y = "log"      # siempre log-log

    fig, axes = plt.subplots(1, len(ordenes), figsize=(7 * len(ordenes), 6), squeeze=False)
    for ax, orden in zip(axes[0], ordenes):
        graficar_subplot(ax, resumen, orden, escala_y, ylabel, estructuras)

    fig.suptitle(titulo, fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    print(f"Guardada: {ruta}")


def main():
    df = cargar_datos(ARCHIVOS_CSV)
    experimentos = sorted(df["experimento"].unique())
    print(f"Experimentos encontrados: {experimentos}")

    for exp in experimentos:
        resumen = agrupar(df, exp)
        if resumen.empty:
            continue
        nombre = NOMBRES_EXPERIMENTO.get(exp, exp)
        hacer_figura(
            resumen,
            f"{exp} — {nombre}\n(promedio de todas las repeticiones; barras y franja = ±1 desviación estándar)",
            "Tiempo (segundos)",
            os.path.join(CARPETA_SALIDA, f"{exp}_{nombre.replace(' ', '_')}.png"),
            ("lista", "abb", "bmas"),
        )

    altura = agrupar_altura(df)
    if not altura.empty:
        hacer_figura(
            altura,
            "Altura del árbol vs N\n(métrica independiente de la máquina; franja = ±1 desviación estándar)",
            "Altura del árbol (niveles)",
            os.path.join(CARPETA_SALIDA, "altura_vs_N.png"),
            ("abb", "bmas"),
        )


if __name__ == "__main__":
    main()