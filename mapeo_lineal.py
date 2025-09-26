import numpy as np
import matplotlib.pyplot as plt


#Función principal de de mapeo lineal
def mapeo_lineal(punto1_recta, punto2_recta, figura, radio_circulo, centro_circulo, A_in, B_in):
    # Convertir puntos a números complejos
    punto1_aux = punto1_recta[0]+punto1_recta[1]*1j
    punto2_aux = punto2_recta[0]+punto2_recta[1]*1j
    centro_circulo_aux = centro_circulo[0]+centro_circulo[1]*1j

    # Se generan los puntos de la figura original
    puntos_figura_original = generar_puntos_figura_original(tipo_figura=figura, centro=centro_circulo_aux, radio=radio_circulo, punto1=punto1_aux, punto2=punto2_aux, n_puntos=100)

    # Aplicar transformación
    w_points = mapeo_lineal_aux(A_in, B_in, puntos_figura_original)

    return w_points


# Función para generar puntos de la figura original y aplicar el mapeo lineal
def generar_puntos_figura_original(tipo_figura='circulo', centro=0, radio=1, punto1=-1+0j, punto2=1+0j, n_puntos=100):

    z_points = None
    
    # Generar puntos según el tipo de figura
    if tipo_figura == 'circulo':
        theta = np.linspace(0, 2 * np.pi, n_puntos)
        z_points = centro + radio * np.exp(1j * theta)
    else:
        t = np.linspace(0, 1, n_puntos)
        z_points = punto1 + t * (punto2 - punto1)

    # se retorna los puntos transformados
    return z_points

    
def mapeo_lineal_aux(A, B, z_points):  
    # Aplicar transformación
    w_points = A * z_points + B
    
    titulo_z = 'Figura Original'
    titulo_w = 'Mapeo Lineal'

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    
    # Grafica de los puntos originales
    ax[0].plot(z_points.real, z_points.imag, 'b-', linewidth=2)
    ax[0].axhline(y=0, color='black', linewidth=1)  # Eje X
    ax[0].axvline(x=0, color='black', linewidth=1)  # Eje Y
    ax[0].set_title(titulo_z)
    ax[0].set_xlabel('Parte Real')
    ax[0].set_ylabel('Parte Imaginaria')
    ax[0].grid(True, alpha=0.3)
    ax[0].set_aspect('equal')
    
    # Grafica de los puntos transformados
    ax[1].plot(w_points.real, w_points.imag, 'g-', linewidth=2)
    ax[1].axhline(y=0, color='black', linewidth=1)  # Eje X
    ax[1].axvline(x=0, color='black', linewidth=1)  # Eje Y
    ax[1].set_title(f'Transformado: w = ({A})*z + ({B})')
    ax[1].set_xlabel('Parte Real')
    ax[1].set_ylabel('Parte Imaginaria')
    ax[1].grid(True, alpha=0.3)
    ax[1].set_aspect('equal')
    
    plt.tight_layout()
    plt.show()

    # se retorna los puntos transformados
    return w_points

mapeo_lineal(punto1_recta=(-1,0), punto2_recta=(1,0), figura='circulo', radio_circulo=2, centro_circulo=(0,0), A_in=2+0j, B_in=1+1j)
#mapeo_lineal(punto1_recta=(-2,-2), punto2_recta=(2,2), figura='linea', radio_circulo=0, centro_circulo=(0,0), A_in=2+0j, B_in=2+0j)
#mapeo_lineal(punto1_recta=(-1,0), punto2_recta=(1,0), figura='circulo', radio_circulo=2, centro_circulo=(1,0), A_in=2+0j, B_in=0+0j)