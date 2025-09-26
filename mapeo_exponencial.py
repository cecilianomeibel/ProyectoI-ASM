# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt


def mapeo_exponencial(punto1_recta, punto2_recta):

    x = None
    y = None

    #Se verifican los puntos dados para determinar si es una recta vertical o horizontal, de lo contrario no se puede hacer el mapeo
    if punto1_recta[0] == punto2_recta[0]:  # Recta vertical (x = constante)
        x = punto1_recta[0]
        y = None
    elif punto1_recta[1] == punto2_recta[1]:  # Recta horizontal (y = constante)
        x = None
        y = punto1_recta[1]
    else:
        raise ValueError("Los puntos dados no forman una recta vertical u horizontal, intente de nuevo.")

    # Se obtiene los puntos de la figura original
    figura_original = generar_puntos_figura_original(x=x, y=y, num_puntos=1000)

    # Se realiza el mapeo exponencial
    w_points = mapeo_exponencial_aux(figura_original)

    return w_points


def generar_puntos_figura_original(x=None, y=None, num_puntos=1000):
    
    z_original = None

    if x is None and y is None:
        raise ValueError("Al menos uno de x o y debe tener un valor")
    
    # Caso 1: x = None, y = constante (ángulo fijo)
    # Genera una recta vertical en el plano z que se mapea a una recta desde el origen
    if x is None:
        # Se genera una recta
        theta = y  # Ángulo en radianes
        
        # Generar puntos a lo largo de la recta vertical x + iy donde y es constante
        x_vals = np.linspace(0, 5, num_puntos)  # Valores de x desde -5 a 5
        
        # Puntos originales en el plano complejo
        z_original = x_vals + 1j * theta
        
    # Caso 2: y = None, x = constante (radio fijo)  
    # Genera una recta horizontal en el plano z que se mapea a un círculo
    elif y is None:
        # Se genera un círculo
        
        # Generar puntos a lo largo de la recta horizontal x + iy donde x es constante
        y_vals = np.linspace(0, 2*np.pi, num_puntos)  # Ángulos de 0 a 2π
        x_val = x          # x constante (radio fijo)
        
        # Puntos originales en el plano complejo
        z_original = x_val + 1j * y_vals
        
    # Caso 3: Ambos x e y tienen valores (punto único)
    else:
        z_original = np.array([x + 1j * y])
    

    return z_original


def mapeo_exponencial_aux(z_original=None):
    # Se realiza el mapeo exponencial: e^(x + iy) = e^x * (cos(y) + i*sin(y))
    w_mapeado = np.exp(z_original)
    visualizar_mapeo(z_original, w_mapeado)

    return w_mapeado


def visualizar_mapeo(z_original, w_mapeado, titulo="Mapeo Exponencial"):
    """
    Visualiza el mapeo exponencial en dos gráficas separadas
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plano original (z)
    ax1.plot(z_original.real, z_original.imag, 'b-', linewidth=2, label='Curva original')
    ax1.set_xlabel('Re(z)')
    ax1.set_ylabel('Im(z)')
    ax1.set_title('Plano Original (z)')
    ax1.grid(True, alpha=0.3)
    ax1.axis('equal')
    ax1.legend()
    
    # Plano mapeado (w)
    ax2.plot(w_mapeado.real, w_mapeado.imag, 'r-', linewidth=2, label='Curva mapeada')
    ax2.set_xlabel('Re(w)')
    ax2.set_ylabel('Im(w)')
    ax2.set_title('Plano Mapeado (w = e^z)')
    ax2.grid(True, alpha=0.3)
    ax2.axis('equal')
    ax2.legend()
    
    plt.suptitle(titulo, fontsize=16)
    plt.tight_layout()
    plt.show()


#mapeo_exponencial(punto1_recta=(2,0), punto2_recta=(2,4), figura='linea', radio_circulo=0, centro_circulo=(0,0), A_in=1+0j, B_in=0+0j)
