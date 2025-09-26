import numpy as np
import matplotlib.pyplot as plt

def mapeo_bilineal(figura, punto1=None, punto2=None, centro=None, radio=None, a=1+0j, b=0+0j, c=0+0j, d=0+0j, n_puntos=400):
    """
    Aplica el mapeo bilineal paso a paso: lineal, inverso, y final extendido.
    Grafica cada paso y retorna los puntos de cada etapa.
    """

    # Se generan los puntos de la figura original
    if figura == 'recta':
        t = np.linspace(0, 1, n_puntos)
        z_points = punto1 + t * (punto2 - punto1)
        titulo_z = f'Recta: {punto1} a {punto2}'

    elif figura == 'circulo':
        theta = np.linspace(-2 * np.pi, 2 * np.pi, n_puntos)
        z_points = centro + radio * np.exp(1j * theta)
        titulo_z = f'Círculo: centro={centro}, radio={radio}'

    else:
        raise ValueError("figura debe ser 'recta' o 'circulo'")

    # Paso 1: Mapeo lineal

    # Mapeo lineal: w1 = A*z + B
    # Para la forma extendida: A = (bc - ad)/c, B = a/c
    if c == 0:
        raise ValueError("El coeficiente c no puede ser cero en la forma extendida")
    
    B = 0
    A = c
    if figura == 'recta':
        B = d
    else:
        # escalamiento con centro fijo (cuando se hace un escalamiento no centrado en el origen, el centro del circulo se mueve, por ende se contrarresta)
        B = (centro - A*centro) + d

    # Mapeo lineal
    w1_points = A * z_points + B

    # Paso 2: Mapeo inverso (inversión respecto al origen): w2 = 1/w1
    w2_points = []
    w_final = []

    # Se debe hacer analisis de la figura luego de la tranformacion lineal
    if figura == 'recta':
        w2_points = mapeo_inverso_recta(w1_points)

    else:
        #cuando la figura es un circulo
        centro_circulo = centro + d
        radio_circulo = radio * np.abs(A)
        w2_points = mapeo_inverso_circulo(w1_points, centro_circulo, radio_circulo)


    # Paso 3: Mapeo final (identidad, ya que la forma extendida termina aquí)
    # Si quisieras aplicar otra transformación, aquí iría
    
    w2_points = np.array(w2_points)  # Convertir lista a array de NumPy
    w_final = np.array(w_final)
    w_final = (a/c) + ((b*c - a*d)/c) * w2_points

    # Graficar cada paso
    fig, axs = plt.subplots(1, 3, figsize=(15, 4))
    axs[0].plot(z_points.real, z_points.imag)
    axs[0].axhline(y=0, color='black', linewidth=1)  # Eje X
    axs[0].axvline(x=0, color='black', linewidth=1)  # Eje Y
    axs[0].set_title('Figura original\n' + titulo_z)
    axs[0].set_aspect('equal')
    if figura == 'recta':
        axs[0].set_xlim(-5, 5)
        axs[0].set_ylim(-5, 5)
    axs[0].grid()
    axs[1].plot(w1_points.real, w1_points.imag)
    axs[1].axhline(y=0, color='black', linewidth=1)  # Eje X
    axs[1].axvline(x=0, color='black', linewidth=1)  # Eje Y
    axs[1].set_title('Tras mapeo lineal')
    axs[1].set_aspect('equal')
    if figura == 'recta':
        axs[1].set_xlim(-5, 5)
        axs[1].set_ylim(-5, 5)
    axs[1].grid()
    axs[2].plot(w_final.real, w_final.imag)
    axs[2].axhline(y=0, color='black', linewidth=1)  # Eje X
    axs[2].axvline(x=0, color='black', linewidth=1)  # Eje Y
    axs[2].set_title('Tras inversión y forma extendida')
    axs[2].set_aspect('equal')
    axs[2].set_xlim(-5, 5)
    axs[2].set_ylim(-5, 5)
    axs[2].grid()
    plt.tight_layout()
    plt.show()

    return z_points, w1_points, w_final

# Función para el mapeo inverso de una recta (contempla todos los posibles casos)
def mapeo_inverso_recta(puntos_recta):

    pendiente = 0
    interseccion_eje_img = 0
    puntos_transformación_final = []

    # Se verifica si la pendiente de la recta es infinita (una recta vertical)
    if puntos_recta[-1].real == puntos_recta[0].real:

        #Se obtiene los parámetros del circulo
        centro_circulo = (1/(puntos_recta[0].real*2)) + 0j
        radio_circulo = (1/(puntos_recta[0].real*2))

        # Se obtiene los puntos del circulo
        theta = np.linspace(0, 2 * np.pi, 400)
        z_points_inversa = centro_circulo + radio_circulo * np.exp(1j * theta)

        # Se retornan los puntos del circulo, el mapeo de la recta vertical
        return z_points_inversa
    
    else:
        # Pendiente de la recta
        pendiente = ((puntos_recta)[-1].imag - puntos_recta[0].imag) / ((puntos_recta)[-1].real - puntos_recta[0].real)

    # Se verifica si la recta es horizontal
    if pendiente == 0:
        

        #Se obtiene los parámetros del circulo (se debe invertir el signo de la componente imaginaria del centro del circulo por el mapeo inverso)
        centro_circulo = 0 - (1/(puntos_recta[0].imag*2)) * 1j
        radio_circulo = (1/(puntos_recta[0].imag*2))

        # Se obtiene los puntos del circulo
        theta = np.linspace(0, 2 * np.pi, 400)
        z_points_inversa = centro_circulo + radio_circulo * np.exp(1j * theta)
                
        # Se retornan los puntos del circulo, el mapeo de la recta horizontal
        return z_points_inversa

    else:
        # Se calcula la intersección con el eje imag (cuando real = 0)
        interseccion_eje_img = puntos_recta[0].imag - pendiente * puntos_recta[0].real # la b de y = mx + b

    ################################################################

    # Se verifica si la recta pasa por el origen (es decir b = 0)
    if interseccion_eje_img == 0:
        #La recta pasa por el origen
        #Se le cambia el signo a cada parte real de los puntos
        for punto in puntos_recta:
            nuevo_punto = -punto.real + punto.imag * 1j
            puntos_transformación_final.append(nuevo_punto)
        
        # se retornan los puntos de la recta, el mapeo de una recta que pasa por el origen
        return puntos_transformación_final
    
    else:
        #La recta no pasa por el origen (tiene dos intersecciones con los ejes), se convierte en un circulo que pasa por el origen con intersección en los dos ejes

        # Se halla la intersección con el eje real (cuando imag = 0)
        interseccion_eje_real = -interseccion_eje_img / pendiente  # x = (y-b)/m
        interseccion_eje_real = 1/interseccion_eje_real # se aplica mapeo inverso

        # Donde en la ecuación del circulo (x-h)^2 + (y-k)^2 = r^2:
        #  h = a/2 (a = interseccion_eje_real), k = b/2 (b = interseccion_eje_img)

        # Dado al comportamiento del mapeo inverso, las componentes imaginarias se deben invertir (cambio de signo)
        interseccion_eje_img = -interseccion_eje_img
        interseccion_eje_img = 1/interseccion_eje_img # se aplica mapeo inverso
        
        # Se obtienen los parámetros del circulo
        centro_circulo = (interseccion_eje_real/2) + (interseccion_eje_img/2)*1j
        radio_circulo = np.sqrt((interseccion_eje_real**2 + interseccion_eje_img**2))/2

        # Se obtiene los puntos del circulo
        theta = np.linspace(0, 2 * np.pi, 400)
        z_points_inversa = centro_circulo + radio_circulo * np.exp(1j * theta)

        # se retornan los puntos del circulo, el mapeo de una recta que no pasa por el origen
        return z_points_inversa

# Función para el mapeo inverso de un círculo (contempla todos los posibles casos)
def mapeo_inverso_circulo(puntos_circulo, centro_circulo, radio_circulo):

    interseccion_eje_img = 0

    # Hay que verificar si el circulo está centrado en el origen (si es así, tiende a infinito)
    if centro_circulo == 0:
        print("El círculo está centrado en el origen, tiende a infinito.")
        return None

    # Se verifica si el circulo se encuentra sobre el eje real
    if centro_circulo.imag == 0:
    
        # Se verifica si el circulo pasa por el origen
        verificar_origen = centro_circulo.real - radio_circulo
        if verificar_origen <= 1e-10 and verificar_origen >= -1e-10:
            
            # Se crean puntos a partir del centro del circulo y radio
            interseccion_eje_real = centro_circulo.real + radio_circulo
            interseccion_eje_real = 1/interseccion_eje_real # se invierte la componente real por el mapeo inverso
            punto1 = interseccion_eje_real + 10j
            punto2 = interseccion_eje_real - 10j

            t = np.linspace(0, 1, 400)
            z_points = punto1 + t * (punto2 - punto1)

            return z_points
        
    # Se verifica si el circulo se encuentra sobre el eje imaginario
    elif centro_circulo.real == 0:

        # Se verifica si el circulo pasa por el origen
        verificar_origen = centro_circulo.imag - radio_circulo
        if verificar_origen <= 1e-10 and verificar_origen >= -1e-10:
            
            # Se crean puntos a partir del centro del circulo y radio
            interseccion_eje_img = centro_circulo.imag + radio_circulo
            interseccion_eje_img = -interseccion_eje_img # se le cambia el signo a la componente imaginaria por el mapeo inverso, pues es una linea horizontal a lo que se transformará
            interseccion_eje_img = 1/interseccion_eje_img # se invierte la componente imaginaria por el mapeo inverso
            punto1 = -10 + interseccion_eje_img*1j
            punto2 = 10 + interseccion_eje_img*1j

            t = np.linspace(0, 1, 400)
            z_points = punto1 + t * (punto2 - punto1)

            return z_points
    
    # Se verifica si el circulo pasa por el origen y tiene intersección en ambos ejes
    if ((centro_circulo.real**2 + centro_circulo.imag**2) - radio_circulo**2) <= 1e-10:

        #De la ecuación del círculo (x-h)^2 + (y-k)^2 = r^2
        # h = a/2 (a = interseccion_eje_real), k = b/2 (b = interseccion_eje_img)
        # Por lo tanto: a = h*2, b = k*2  (siempre y cuando el círculo pase por el origen)
        print("Pasa aquí?")

        interseccion_eje_real = centro_circulo.real*2
        interseccion_eje_real = 1/interseccion_eje_real # se invierte la componente real por el mapeo inverso 
        interseccion_eje_img = centro_circulo.imag*2
        interseccion_eje_img = 1/interseccion_eje_img # se invierte la componente imaginaria por el mapeo inverso

        # Debido al mapeo inverso, se invierte la componente imaginaria
        interseccion_eje_img = -interseccion_eje_img

        punto1 = interseccion_eje_real + 0j
        punto2 = 0 + interseccion_eje_img*1j

        t = np.linspace(-5, 5, 400)
        z_points = punto1 + t * (punto2 - punto1)

        return z_points

    else:
        # El círculo no pasa por el origen, se invierten todos sus puntos
        z_points = 1 / puntos_circulo
        return z_points


# Ejemplo de uso:
if __name__ == "__main__":

    #Ejemplo de mapeo bilineal
    mapeo_bilineal('recta', punto1=-2+1j, punto2=2+1j, a=2+0j, b=0+1j, c=2+0j, d=0-1j)

    # Ejemplo recta vertical
    #mapeo_bilineal('recta', punto1=2-2j, punto2=2+4j, a=2+0j, b=0+1j, c=2+0j, d=0-1j)

    # Recta horizontal ejemplo
    #mapeo_bilineal('recta', punto1=-2+1j, punto2=2+1j, a=2+0j, b=0+1j, c=2+0j, d=0-0j)

    # Recta que pasa por el origen
    #mapeo_bilineal('recta', punto1=-10-10j, punto2=10+10j, a=2+0j, b=0+1j, c=2+0j, d=0-0j)

    #Recta que interseca en los dos ejes
    #mapeo_bilineal('recta', punto1=-4-2j, punto2=2+4j, a=2+0j, b=0+1j, c=2+0j, d=0-0j)

    # Círculo centrado sobre el eje real
    #mapeo_bilineal('circulo', centro=2+0j, radio=1, a=0+0j, b=1+0j, c=2+0j, d=0+0j)

    #Círculo centrado sobre el eje imaginario
    #mapeo_bilineal('circulo', centro=0+2j, radio=1, a=0+0j, b=1+0j, c=2+0j, d=0+0j)

    #Círculo que pasa por el origen y tiene intersección en ambos ejes
    #mapeo_bilineal('circulo', centro=1+1j, radio=2**(1/2), a=0+0j, b=1+0j, c=1+0j, d=0+0j)

    # Círculo que no pasa por el origen
    #mapeo_bilineal('circulo', centro=4+4j, radio=2, a=0+0j, b=1+0j, c=1+0j, d=0+0j)

    # Ejemplos de Meibel
    #mapeo_bilineal('recta', punto1=-1+0j, punto2=-1+5j, a=2+0j, b=0+1j, c=1+0j, d=0-0j)

    #mapeo_bilineal('recta', punto1=0+0j, punto2=0.10+0.10j, a=2+0j, b=0+1j, c=1+0j, d=0-0j)
