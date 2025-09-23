import numpy as np
import matplotlib.pyplot as plt


# Función simple para uso rápido sin interfaz gráfica
def mapeo_lineal(A, B, tipo_figura='circulo', centro=0, radio=1, punto1=-1+0j, punto2=1+0j, n_puntos=100):
    
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    
    # Generar puntos según el tipo de figura
    if tipo_figura == 'circulo':
        theta = np.linspace(0, 2 * np.pi, n_puntos)
        z_points = centro + radio * np.exp(1j * theta)
        titulo_z = f'Círculo: centro={centro}, radio={radio}'
    else:
        t = np.linspace(0, 1, n_puntos)
        z_points = punto1 + t * (punto2 - punto1)
        titulo_z = f'Línea: P1={punto1}, P2={punto2}'
    
    # Aplicar transformación
    w_points = A * z_points + B
    
    # Graficar
    ax[0].plot(z_points.real, z_points.imag, 'b-', linewidth=2)
    ax[0].set_title(titulo_z)
    ax[0].set_xlabel('Parte Real')
    ax[0].set_ylabel('Parte Imaginaria')
    ax[0].grid(True, alpha=0.3)
    ax[0].set_aspect('equal')
    
    ax[1].plot(w_points.real, w_points.imag, 'g-', linewidth=2)
    ax[1].set_title(f'Transformado: w = ({A})*z + ({B})')
    ax[1].set_xlabel('Parte Real')
    ax[1].set_ylabel('Parte Imaginaria')
    ax[1].grid(True, alpha=0.3)
    ax[1].set_aspect('equal')
    
    plt.tight_layout()
    plt.show()
