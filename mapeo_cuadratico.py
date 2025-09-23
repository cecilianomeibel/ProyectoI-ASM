import math
import matplotlib.pyplot as plt

# ------------------
# MAPEO CUADRÁTICO
# ------------------
def mapeo_cuadratico(z, modo='cartesiano'):
    """
    Realiza el mapeo cuadrático: z -> z^2
    Parámetros:
        z: punto en coordenadas cartesianas (x, y) o polares (r, theta)
        modo: 'cartesiano' o 'polar'
    Retorna:
        Tupla (u, v) del punto transformado
    """
    if modo == 'cartesiano':
        x, y = z
        # Fórmulas del mapeo cuadrático en cartesianas: (x + iy)^2 = u + iv
        u = x**2 - y**2
        v = 2 * x * y
        return (u, v)
    elif modo == 'polar':
        r, theta = z
        # Fórmulas en coordenadas polares: r^2 e^(i 2θ)
        rho = r**2
        phi = 2 * theta
        # Convertir de polar a cartesianas para graficar
        u = rho * math.cos(phi)
        v = rho * math.sin(phi)
        return (u, v)
    else:
        raise ValueError("El modo debe ser 'cartesiano' o 'polar'")

# =======================
# FUNCIONES DE GRAFICACIÓN
# =======================
def graficar_punto(ax, punto, color="b", etiqueta="", lim=5):
    """
    Grafica un solo punto en un eje dado.
    Parámetros:
        ax: objeto matplotlib Axes
        punto: tupla (x, y)
        color: color del punto
        etiqueta: leyenda del punto
        lim: límite de los ejes
    """
    x, y = punto
    ax.plot(x, y, 'o', color=color, label=etiqueta)
    ax.axhline(0, color='gray', lw=0.5)  # eje horizontal
    ax.axvline(0, color='gray', lw=0.5)  # eje vertical
    ax.set_aspect('equal', adjustable='box')  # ejes con la misma escala
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.legend()

def mostrar_grafico_comparativo(z, w, titulo_izq="Original", titulo_der="Mapeo cuadrático"):
    """
    Muestra un gráfico comparativo entre el punto original  y el resultado del 
    mapeo cuadrático. También imprime los valores en consola.
    """
    print(f"{titulo_izq}: {z}")
    print(f"{titulo_der}: {w}\n")
    
    fig, axs = plt.subplots(1, 2, figsize=(8,4))
    
    # Gráfico del punto original
    graficar_punto(axs[0], z, color='blue', etiqueta=titulo_izq)
    axs[0].set_title(titulo_izq)
    
    # Gráfico del punto transformado
    graficar_punto(axs[1], w, color='red', etiqueta=titulo_der)
    axs[1].set_title(titulo_der)
    
    plt.tight_layout()
    plt.show()


