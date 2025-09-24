import numpy as np
import matplotlib.pyplot as plt

def mapeo_bilineal(figura, punto1=None, punto2=None, centro=None, radio=None, a=1+0j, b=0+0j, c=0+0j, d=1+0j, n_puntos=400):
    """
    Aplica el mapeo bilineal paso a paso: lineal, inverso, y final extendido.
    Grafica cada paso y retorna los puntos de cada etapa.
    """
    # Paso 1: Mapeo lineal
    if figura == 'recta':
        t = np.linspace(0, 1, n_puntos)
        z_points = punto1 + t * (punto2 - punto1)
        titulo_z = f'Recta: {punto1} a {punto2}'
    elif figura == 'circulo':
        theta = np.linspace(0, 2 * np.pi, n_puntos)
        z_points = centro + radio * np.exp(1j * theta)
        titulo_z = f'Círculo: centro={centro}, radio={radio}'
    else:
        raise ValueError("figura debe ser 'recta' o 'circulo'")

    # Mapeo lineal: w1 = A*z + B
    # Para la forma extendida: A = (bc - ad)/c, B = a/c
    if c == 0:
        raise ValueError("El coeficiente c no puede ser cero en la forma extendida")
    A = c
    B = d
    w1_points = A * z_points + B

    # Paso 2: Mapeo inverso (inversión respecto al origen): w2 = 1/w1
    w2_points = np.zeros_like(w1_points, dtype=complex)
    mask = np.abs(w1_points) > 1e-12
    w2_points[mask] = 1 / w1_points[mask]
    w2_points[~mask] = np.nan  # Para evitar división por cero

    
    # Paso 3: Mapeo final (identidad, ya que la forma extendida termina aquí)
    # Si quisieras aplicar otra transformación, aquí iría
    w_final = (a/c) + ((b*c - a*d)/c) * w2_points
 
    # Graficar cada paso
    fig, axs = plt.subplots(1, 3, figsize=(15, 4))
    axs[0].plot(z_points.real, z_points.imag)
    axs[0].set_title('Figura original\n' + titulo_z)
    axs[0].set_aspect('equal')
    if figura == 'recta':
        axs[0].set_xlim(-5, 5)
        axs[0].set_ylim(-5, 5)
    axs[0].grid()
    axs[1].plot(w1_points.real, w1_points.imag)
    axs[1].set_title('Tras mapeo lineal')
    axs[1].set_aspect('equal')
    if figura == 'recta':
        axs[1].set_xlim(-5, 5)
        axs[1].set_ylim(-5, 5)
    axs[1].grid()
    axs[2].plot(w_final.real, w_final.imag)
    axs[2].set_title('Tras inversión y forma extendida')
    axs[2].set_aspect('equal')
    axs[2].grid()
    plt.tight_layout()
    plt.show()

    return z_points, w1_points, w_final

# Ejemplo de uso:
if __name__ == "__main__":
    # Recta ejemplo
    mapeo_bilineal('recta', punto1=-2+1j, punto2=2+1j, a=2+0j, b=0+1j, c=2+0j, d=0-1j)

    # Círculo ejemplo
    #mapeo_bilineal('circulo', centro=0+0j, radio=2, a=0+0j, b=1+0j, c=1+0j, d=0+0j)


