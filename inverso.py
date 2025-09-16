import cmath

def circ_por_tres(p1, p2, p3):
    """ Devuelve centro y radio del círculo que pasa por tres puntos """
    (x1,y1),(x2,y2),(x3,y3) = (p1.real,p1.imag),(p2.real,p2.imag),(p3.real,p3.imag)
    A = 2*(x2-x1)
    B = 2*(y2-y1)
    C = x2**2 + y2**2 - x1**2 - y1**2
    D = 2*(x3-x1)
    E = 2*(y3-y1)
    F = x3**2 + y3**2 - x1**2 - y1**2
    denom = A*E - B*D
    if denom == 0:
        return None
    cx = (C*E - B*F)/denom
    cy = (A*F - C*D)/denom
    r = ((x1-cx)**2 + (y1-cy)**2)**0.5
    return (cx, cy), r

def recta_por_dos(p1, p2):
    """ Devuelve la recta en forma general Ax + By + C = 0 a partir de dos puntos """
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:  # recta vertical
        A, B, C = 1, 0, -x1
    elif y1 == y2:  # recta horizontal
        A, B, C = 0, 1, -y1
    else:
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m*x1
        A, B, C = -m, 1, -b
    return (A, B, C)

def inverso(tipo, *args):
    """
    Aplica la inversión w = 1/z a un círculo o recta.
    
    Argumentos:
    - ("circulo", centro, radio)   con centro = (x,y)
    - ("linea", p1, p2)            con dos puntos de la recta
    
    Retorna:
    - ("circulo", (cx,cy), r)
    - ("linea", ((x1,y1),(x2,y2)))
    """
    if tipo == "circulo":
        centro, radio = args
        a, b = centro
        r = radio
        d2 = a*a + b*b  # distancia al origen al cuadrado

        # Círculo que pasa por el origen → línea vertical/horizontal
        if abs(d2 - r*r) < 1e-12:  
            # Línea vertical: x = a/2
            x_line = a / 2
            return ("linea", ((x_line, 0), (x_line, 1)))  # segundo punto cualquiera distinto
        else:
            # Círculo que no pasa por el origen → inversión directa
            cx = -a / (d2 - r*r)
            cy = -b / (d2 - r*r)
            r_new = r / abs(d2 - r*r)
            return ("circulo", (cx, cy), r_new)

    elif tipo == "linea":
        p1, p2 = args
        x1, y1 = p1
        x2, y2 = p2

        # Línea que pasa por el origen → sigue siendo línea tras la inversión
        if (x1==0 and y1==0) or (x2==0 and y2==0):
            p_no_origen = (x2, y2) if (x1==0 and y1==0) else (x1, y1)
            x, y = p_no_origen
            # Aplicamos inversión de un solo punto
            w = (x/(x**2 + y**2), y/(x**2 + y**2))
            return ("linea", ((0,0), w))
        else:
            # Línea que no pasa por el origen → círculo que pasa por el origen
            z1 = complex(*p1)
            z2 = complex(*p2)
            z3 = 0+0j
            return ("circulo", *circ_por_tres(z1, z2, z3))
    else:
        raise ValueError("El tipo debe ser 'circulo' o 'linea'")

def info_recta_puntos(p1, p2):
    """ Devuelve info legible de la recta a partir de dos puntos """
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:
        return f"x = {x1}"
    elif y1 == y2:
        return f"y = {y1}"
    else:
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m*x1
        return f"y = {m}x + {b}"


# Ejemplos
print(inverso("circulo", (1,0),1)) # Círculo que pasa por el origen → Línea que no pasa por el origen

print(inverso("circulo", (0,10), 2)) # Círculo que no pasa por el origen → Círculo que no pasa por el origen

print(inverso("linea", (0.5,0), (0.5,0.5))) # Línea que no pasa por el origen → Círculo que pasa por el origen

print(inverso("linea", (0,0),(2,3))) # Línea que pasa por el origen → Línea que pasa por el origen
