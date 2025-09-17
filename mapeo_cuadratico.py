import math

def mapeo_cuadratico(z, modo='cartesiano'):
    """
    Mapeo cuadrático w = z^2.
    
    Argumentos:
    - z: tupla de coordenadas
        - modo='cartesiano': z = (x, y)
        - modo='polar': z = (r, theta)
    
    Retorna:
    - w: tupla de coordenadas en el mismo modo
        - cartesiano: (u, v)
        - polar: (rho, phi)
    """
    if modo == 'cartesiano':
        x, y = z
        u = x**2 - y**2
        v = 2 * x * y
        return (u, v)
    
    elif modo == 'polar':
        r, theta = z
        rho = r**2
        phi = 2 * theta
        return (rho, phi)
    
    else:
        raise ValueError("El modo debe ser 'cartesiano' o 'polar'")

# --- Ejemplos de uso ---


# Coordenadas cartesianas
#z en coordenadas cartesianas es: z = x + iy
z_cart = (2, 1)
w_cart = mapeo_cuadratico((2, 1), modo='cartesiano')
print(f"Entrada cartesiana {z_cart} -> Salida {w_cart}")

# Coordenadas polares
# z en coordenadas polares es: z = re^(iθ)
z_polar = (2, math.pi/4)
w_polar = mapeo_cuadratico(z_polar, modo='polar')
print(f"Entrada polar {z_polar} -> Salida {w_polar}")
