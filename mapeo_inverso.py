import numpy as np
import matplotlib.pyplot as plt

# -------------------
# FUNCION PRINCIPAL 
# -------------------

def mapeo_inverso(punto1, punto2, figura, radio, centro):
    """
    Calcula el mapeo inverso de un círculo o línea respecto al origen
    y muestra automáticamente el gráfico comparativo.
    """

    # Preparar datos de entrada
    if figura == "circulo":
        entrada = (figura, centro, radio)
        args = (centro, radio)
    elif figura == "recta":
        entrada = (figura, punto1, punto2)
        args = (punto1, punto2)
    else:
        raise ValueError("figura debe ser 'circulo' o 'recta'")

    # Calcular mapeo inverso
    salida = mapeo_inverso_aux(figura, args)

    # Graficar automáticamente
    mostrar_grafico_comparativo(entrada, salida)

    # Retornar solo la salida por si se quiere usar
    return salida


# =======================
# FUNCIONES AUXILIARES
# =======================

def mapeo_inverso_aux(figura, args):
    """
    Función auxiliar para mapeo inverso.
    """

    if figura == "circulo":
        # Desempaquetar centro y radio
        centro, radio = args
        a, b = centro
        r = radio
        d2 = a*a + b*b  # Distancia al cuadrado desde el origen hasta el centro

        # Caso especial: el círculo pasa por el origen → se mapea a línea
        if abs(d2 - r*r) < 1e-12:
            # La imagen es una recta: todos los puntos w tales que |w - (a+ib)| = |w|
            x_recta = 2*a  # Ecuación de la recta: x = a/2
                # Caso especial: centro en eje X → recta vertical
            return ("recta", ((x_recta, -10), (x_recta, 10)))

        else:
            # Cálculo general para círculo que no pasa por el origen
            cx = -a / (d2 - r*r)
            cy = -b / (d2 - r*r)
            r_new = r / abs(d2 - r*r)
            return ("circulo", (float(cx), float(cy)), float(r_new))

    elif figura == "recta":
        # Desempaquetar los dos puntos de la línea
        p1, p2 = args
        x1, y1 = p1
        x2, y2 = p2

        # Si uno de los puntos está en el origen → la línea se mapea a otra línea
        if (x1 == 0 and y1 == 0) or (x2 == 0 and y2 == 0):
            p_no_origen = (x2, y2) if (x1 == 0 and y1 == 0) else (x1, y1)
            x, y = p_no_origen
            # Aplicar inversión respecto al origen
            w = (x/(x**2 + y**2), y/(x**2 + y**2))
            return ("recta", ((0, 0), w))
        else:
            # Caso general: la línea no pasa por el origen → se mapea a círculo que pasa por el origen
            q1 = invertir_punto(p1)
            q2 = invertir_punto(p2)
            q3 = (0, 0)
            return ("circulo", *circ_por_tres((0, 0), q1, q2))
    else:
        raise ValueError("El figura debe ser 'circulo' o 'recta'")


def invertir_punto(p):
    """
    Invierte un punto respecto al origen: P -> P/|P|^2
    """
    x, y = p
    den = x**2 + y**2
    return (x/den, y/den)


def circ_por_tres(p1, p2, p3):
    """
    Calcula el círculo que pasa por tres puntos distintos.
    Retorna el centro y radio.
    """
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    # Sistema de ecuaciones para el centro del círculo
    A = 2 * (x2 - x1)
    B = 2 * (y2 - y1)
    C = x2**2 + y2**2 - x1**2 - y1**2
    D = 2 * (x3 - x1)
    E = 2 * (y3 - y1)
    F = x3**2 + y3**2 - x1**2 - y1**2

    denom = A * E - B * D
    if abs(denom) < 1e-12:
        raise ValueError("Los tres puntos son colineales, no definen un círculo.")

    cx = (C * E - B * F) / denom
    cy = (A * F - C * D) / denom
    r = np.hypot(x1 - cx, y1 - cy)  # Radio como distancia desde centro a un punto

    return (float(cx), float(cy)), float(r)


# ------------
# GRAFICACIÓN
# ------------

def graficar_objeto(figura, *args, color="b", etiqueta=""):
    """
    Dibuja un círculo o línea en la gráfica usando matplotlib.
    """
    if figura == "circulo":
        # Ajuste para argumentos
        if len(args) == 1 and isinstance(args[0], tuple) and len(args[0]) == 2 and isinstance(args[0][1], (float, np.floating)):
            centro, radio = args[0]
        else:
            centro, radio = args
        cx, cy = centro
        circ = plt.Circle((cx, cy), radio, color=color, fill=False, label=etiqueta)
        plt.gca().add_patch(circ)
        plt.plot(cx, cy, "o", color=color)

    elif figura == "recta":
        if len(args) == 1:
            (x1, y1), (x2, y2) = args[0]
        else:
            (x1, y1), (x2, y2) = args

        if x1 == x2:
            plt.axvline(x1, color=color, label=etiqueta)
        else:
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m*x1
            xs = np.linspace(-5, 5, 400)
            ys = m*xs + b
            plt.plot(xs, ys, color=color, label=etiqueta)


def mostrar_grafico_comparativo(entrada, salida):
    """
    Muestra una comparación gráfica de la figura original y su mapeo inverso.
    """
    fig, axs = plt.subplots(1, 2, figsize=(6, 4))

    # Entrada
    axs[0].axhline(0, color="gray", lw=0.5)
    axs[0].axvline(0, color="gray", lw=0.5)
    plt.sca(axs[0])
    graficar_objeto(*entrada, color="blue")
    axs[0].set_aspect('equal', adjustable='box')
    axs[0].set_title("Original")

    # Salida
    axs[1].axhline(0, color="gray", lw=0.5)
    axs[1].axvline(0, color="gray", lw=0.5)
    plt.sca(axs[1])
    graficar_objeto(*salida, color="red")
    axs[1].set_aspect('equal', adjustable='box')
    axs[1].set_title("Mapeo inverso")

    # Ajustar límites para que se vea la recta
    axs[1].set_xlim(-1, 6)
    axs[1].set_ylim(-1, 6)

    plt.show()


# Pruebas 
#mapeo_inverso(None, None, "circulo", 0.5, (0.5, 0))
#mapeo_inverso(None, None, "circulo", 1, (1, 0))
#mapeo_inverso(None, None, "circulo", 2, (2, 0))
#mapeo_inverso((-1,0), (-1,5), "recta", None, None)
