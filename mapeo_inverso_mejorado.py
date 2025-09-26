import numpy as np
import matplotlib.pyplot as plt

def mapeo_inverso(figura, punto1=None, punto2=None, centro=None, radio=None, n_puntos=400):

    figura_original = generar_puntos_figura_original(figura, punto1, punto2, centro, radio, n_puntos=n_puntos)

    figura_result, w_points, centro_result, radio_result = mapeo_inverso_aux(figura, figura_original, centro=centro, radio=radio)

    return figura_result, w_points, centro_result, radio_result


def generar_puntos_figura_original(figura, punto1=None, punto2=None, centro=None, radio=None,n_puntos=400):

    z_points = None

    # Se generan los puntos de la figura original
    if figura == 'recta':
        t = np.linspace(0, 1, n_puntos)
        z_points = punto1 + t * (punto2 - punto1)

    else:  #cuando la figura es un circulo
        theta = np.linspace(-2 * np.pi, 2 * np.pi, n_puntos)
        z_points = centro + radio * np.exp(1j * theta)

    return z_points

def mapeo_inverso_aux(figura, z_points, centro=None, radio=None):

    w1_points = None
    figura_result = None
    centro_result = None
    radio_result = None

    # Se realiza el mapeo inverso
    if figura == 'recta':
        figura_result, w1_points, centro_result, radio_result = mapeo_inverso_recta(z_points)

    else:
        #cuando la figura es un circulo
        centro_circulo = centro
        radio_circulo = radio
        figura_result, w1_points, centro_result, radio_result = mapeo_inverso_circulo(z_points, centro_circulo, radio_circulo)
    
    # Convertir a array de NumPy para asegurar que tenga atributos .real e .imag
    w1_points = np.array(w1_points)

    # Graficar cada paso
    fig, axs = plt.subplots(1, 2, figsize=(15, 4))
    axs[0].plot(z_points.real, z_points.imag)
    axs[0].axhline(y=0, color='black', linewidth=1)  # Eje X
    axs[0].axvline(x=0, color='black', linewidth=1)  # Eje Y
    axs[0].set_title('Figura original\n')
    axs[0].set_aspect('equal')
    if figura == 'recta':
        axs[0].set_xlim(-5, 5)
        axs[0].set_ylim(-5, 5)
    axs[0].grid()
    axs[1].plot(w1_points.real, w1_points.imag)
    axs[1].axhline(y=0, color='black', linewidth=1)  # Eje X
    axs[1].axvline(x=0, color='black', linewidth=1)  # Eje Y
    axs[1].set_title('Mapeo de inversión')
    axs[1].set_aspect('equal')
    if figura == 'recta':
        axs[1].set_xlim(-5, 5)
        axs[1].set_ylim(-5, 5)
    axs[1].grid()
    
    plt.tight_layout()
    plt.show()

    return figura_result, w1_points, centro_result, radio_result


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
        return 'circulo', z_points_inversa, centro_circulo, radio_circulo
    
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
        return 'circulo', z_points_inversa, centro_circulo, radio_circulo

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
        return 'recta', puntos_transformación_final, 0+0j, 0.0
    
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
        return 'circulo', z_points_inversa, centro_circulo, radio_circulo

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

            return 'recta', z_points, 0+0j, 0.0
        
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

            return 'recta', z_points, 0+0j, 0.0
    
    # Se verifica si el circulo pasa por el origen y tiene intersección en ambos ejes
    if ((centro_circulo.real**2 + centro_circulo.imag**2) - radio_circulo**2) <= 1e-10:

        #De la ecuación del círculo (x-h)^2 + (y-k)^2 = r^2
        # h = a/2 (a = interseccion_eje_real), k = b/2 (b = interseccion_eje_img)
        # Por lo tanto: a = h*2, b = k*2  (siempre y cuando el círculo pase por el origen)

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

        return 'recta', z_points, 0+0j, 0.0

    else:
        # El círculo no pasa por el origen, se invierten todos sus puntos
        z_points = 1/puntos_circulo
        centro_circulo_result = centro_circulo.conjugate() / (np.abs(centro_circulo)**2 - radio_circulo**2)
        radio_circulo_result = radio_circulo / abs(np.abs(centro_circulo)**2 - radio_circulo**2)
        # Se retornan los puntos del circulo, el mapeo del circulo que no pasa por el origen
        return 'circulo', z_points, centro_circulo_result, radio_circulo_result


# Ejemplo de uso:
#if __name__ == "__main__":

    # Ejemplo recta vertical
    #mapeo_inverso('recta', punto1=2-2j, punto2=2+4j)

    # Recta horizontal ejemplo
    #mapeo_inverso('recta', punto1=-2+1j, punto2=2+1j)

    # Recta que pasa por el origen
    #mapeo_inverso('recta', punto1=-10-10j, punto2=10+10j)

    #Recta que interseca en los dos ejes
    #mapeo_inverso('recta', punto1=-4-2j, punto2=2+4j)

    # Círculo centrado sobre el eje real
    #mapeo_inverso('circulo', centro=2+0j, radio=1)

    #Círculo centrado sobre el eje imaginario
    #mapeo_inverso('circulo', centro=0+2j, radio=1)

    #Círculo que pasa por el origen y tiene intersección en ambos ejes
    #mapeo_inverso('circulo', centro=1+1j, radio=2**(1/2))

    # Círculo que no pasa por el origen
    #figura_result, w_points, centro_result, radio_result = mapeo_inverso('circulo', centro=4+4j, radio=2)
    #print(f'Figura resultante: {figura_result}')
    #print(f'Centro resultante: {centro_result}, Radio resultante: {radio_result}')

    # Ejemplos de Meibel
    #mapeo_inverso('recta', punto1=-1+0j, punto2=-1+5j, a=2+0j, b=0+1j, c=1+0j, d=0-0j)

    #mapeo_inverso('recta', punto1=0+0j, punto2=0.10+0.10j, a=2+0j, b=0+1j, c=1+0j, d=0-0j)