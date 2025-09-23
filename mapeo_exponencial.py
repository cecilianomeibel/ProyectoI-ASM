# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

def mapeo_exponencial(x=None, y=None, num_puntos=1000):
    
    if x is None and y is None:
        raise ValueError("Al menos uno de x o y debe tener un valor")
    
    # Caso 1: x = None, y = constante (ángulo fijo)
    # Genera una recta vertical en el plano z que se mapea a una recta desde el origen
    if x is None:
        theta = y  # Ángulo en radianes
        print(f"Generando recta infinita con angulo theta = {theta:.4f} radianes ({np.degrees(theta):.2f} grados)")
        
        # Generar puntos a lo largo de la recta vertical x + iy donde y es constante
        x_vals = np.linspace(0, 5, num_puntos)  # Valores de x desde -5 a 5
        y_vals = np.full_like(x_vals, theta)     # y constante (ángulo fijo)
        
        # Puntos originales en el plano complejo
        z_original = x_vals + 1j * y_vals
        
        # Mapeo exponencial: e^(x + iy) = e^x * (cos(y) + i*sin(y))
        w_mapeado = np.exp(z_original)
        
    # Caso 2: y = None, x = constante (radio fijo)  
    # Genera una recta horizontal en el plano z que se mapea a un círculo
    elif y is None:
        print(f"Generando circulo de radio e^{x:.4f} = {np.exp(x):.4f}")
        
        # Generar puntos a lo largo de la recta horizontal x + iy donde x es constante
        y_vals = np.linspace(0, 2*np.pi, num_puntos)  # Ángulos de 0 a 2π
        x_val = x          # x constante (radio fijo)
        
        # Puntos originales en el plano complejo
        z_original = x_val + 1j * y_vals
        
        # Mapeo exponencial: e^(x + iy) = e^x * (cos(y) + i*sin(y))
        w_mapeado = np.exp(z_original)
        
    # Caso 3: Ambos x e y tienen valores (punto único)
    else:
        print(f"Mapeando punto único z = {x} + {y}i")
        z_original = np.array([x + 1j * y])
        w_mapeado = np.exp(z_original)
    
    return z_original, w_mapeado

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

# Función principal para probar diferentes casos
def main():
    print("=== MAPEO EXPONENCIAL DE NUMEROS COMPLEJOS ===\n")
    
    # Ejemplo 1: Recta infinita con ángulo pi/4
    print("1. Recta infinita con angulo pi/4:")
    z1, w1 = mapeo_exponencial(x=None, y=np.pi)
    visualizar_mapeo(z1, w1, "Recta infinita -> Recta desde origen")
    
    # Ejemplo 2: Círculo de radio e^1
    print("\n2. Circulo de radio e^1:")
    z2, w2 = mapeo_exponencial(x=1, y=None)
    visualizar_mapeo(z2, w2, "Recta horizontal -> Circulo")
    
    # Ejemplo 3: Círculo de radio e^0 = 1
    print("\n3. Circulo de radio e^0 = 1:")
    z3, w3 = mapeo_exponencial(x=0, y=None)
    visualizar_mapeo(z3, w3, "Recta horizontal (x=0) -> Circulo unitario")
    
    # Ejemplo 4: Recta con ángulo pi/2
    print("\n4. Recta infinita con angulo pi/2:")
    z4, w4 = mapeo_exponencial(x=None, y=np.pi/2)
    visualizar_mapeo(z4, w4, "Recta infinita (theta=pi/2) -> Recta vertical")

if __name__ == "__main__":
    main()
