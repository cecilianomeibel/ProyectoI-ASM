import math
import numpy as np
import matplotlib.pyplot as plt

# ------------------
# FUNCION PRINCIPAL
# ------------------
def mapeo_cuadratico(punto1=None, punto2=None, figura=None, radio=None, centro=None):
    """
    Función que detecta el tipo de figura según los parámetros y:
    - Aplica el mapeo cuadrático
    - Grafico comparativo de la versión original y mapeada

    Parámetros:
    - punto1, punto2: argumentos para una recta
    - figura:  "recta" o "circulo"
    - radio, centro: argumentos para un círculo
    """

    # ------------------
    # CREACION DE LA FIGURA ORIGINAL
    # ------------------
    if figura is None:
        raise ValueError("Debe indicar el tipo de figura")

    # Recta (dos puntos)
    if figura == "recta":
        if punto1 is None or punto2 is None:
            raise ValueError("Debe proporcionar dos puntos para la recta")
        x1, y1 = punto1
        x2, y2 = punto2
        x = np.linspace(x1, x2, 200)
        y = np.linspace(y1, y2, 200)
        figura_original = list(zip(x, y))

    # Círculo
    elif figura == "circulo":
        if radio is None or centro is None:
            raise ValueError("Debe proporcionar radio y centro para el círculo")
        xc, yc = centro
        theta = np.linspace(0, 2*np.pi, 200)
        figura_original = [(radio*math.cos(t)+xc, radio*math.sin(t)+yc) for t in theta]

    else:
        raise ValueError("Tipo de figura no reconocida, debe ser 'recta' o 'circulo'")
    
    return mapeo_cuadratico_aux(figura_original)

# Función auxiliar para el mapeo cuadrático (figura_original es lista de tuplas o pares ordenados)
def mapeo_cuadratico_aux(figura_original):
    # ------------------
    # MAPEADO CUADRATICO
    # ------------------
    figura_mapeada = [obtener_componentes_w(p) for p in figura_original]

    # ------------------
    # GRAFICO COMPARATIVO
    # ------------------
    fig, axs = plt.subplots(1, 2, figsize=(10,5))
    graficar_figura(axs[0], figura_original, color='blue', etiqueta="Original")
    axs[0].set_title("Original")

    graficar_figura(axs[1], figura_mapeada, color='red', etiqueta="Mapeo cuadrático")
    axs[1].set_title("Mapeo cuadrático")

    plt.tight_layout()
    plt.show()

    #transformar figura_mapeada en formato complejo
    figura_mapeada_compleja = [complex(x, y) for x, y in figura_mapeada]

    # retornar la figura mapeada en formato complejo (puntos complejos)
    return figura_mapeada_compleja


# Función interna para el mapeo cuadrático
def obtener_componentes_w(z):
    x, y = z
    u = x**2 - y**2
    v = 2*x*y
    return (u, v)

# Función interna para graficar
def graficar_figura(ax, fig, color="b", etiqueta="", lim=5):
    x, y = zip(*fig)
    ax.plot(x, y, color=color, label=etiqueta)
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.legend()



# ------------------
# EJEMPLOS
# ------------------

#mapeo_cuadratico((-1,0), (1,7.5), "recta", None, None)
#mapeo_cuadratico(None, None, "circulo", 1, (1,0))
