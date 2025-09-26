
# Importar funciones de los módulos
import detector_figuras
from mapeo_lineal import mapeo_lineal, mapeo_lineal_aux
from mapeo_bilineal_mejorado import mapeo_bilineal
from mapeo_cuadratico import mapeo_cuadratico, mapeo_cuadratico_aux
from mapeo_exponencial import mapeo_exponencial, mapeo_exponencial_aux
from mapeo_inverso_mejorado import mapeo_inverso, mapeo_inverso_aux

def main():

    print("=== Menú de mapeos ===")
    print("1. Mapeo Bilineal (Möbius)")
    print("2. Mapeo Lineal")
    print("3. Mapeo Cuadrático")
    print("4. Mapeo Exponencial")
    print("5. Mapeo Inverso")
    opcion = input("Seleccione el tipo de mapeo (1-5): ")


    nombre_archivo = input("Ingrese el nombre del archivo de imagen (ejemplo: textoRecta1.jpg): ")
    imagen = f"ImgPruebas/{nombre_archivo}"

    # Inicializar puntos_base con la figura detectada
    puntos_base = None
    centro_result = None
    radio_result = None
    tipo_base = None
    continuar = True
    while continuar:
        if opcion == '1':
            # Solicitar parámetros del mapeo bilineal
            a = complex(input("Ingrese el valor de 'a': "))
            b = complex(input("Ingrese el valor de 'b': "))
            c = complex(input("Ingrese el valor de 'c': "))
            d = complex(input("Ingrese el valor de 'd': "))
            
            if puntos_base is None:
                punto1, punto2, figura, radio, centro = detector_figuras.detectar_figura_y_texto(imagen)
                print(f'Datos extraídos: punto1={punto1}, punto2={punto2}, figura={figura}, radio={radio}, centro={centro}')

                if figura == 'recta':
                    p1 = convertir_a_complejo(punto1)
                    p2 = convertir_a_complejo(punto2)
                    tipo_base, puntos_base, centro_result, radio_result = mapeo_bilineal('recta', punto1=p1, punto2=p2, a=a, b=b, c=c, d=d)

                elif figura == 'circulo':
                    r = float(radio)
                    c_centro = convertir_a_complejo(centro)
                    tipo_base, puntos_base, centro_result, radio_result = mapeo_bilineal('circulo', centro=c_centro, radio=r, a=a, b=b, c=c, d=d)

                else:
                    print('Figura no reconocida o no detectada.')
                    break
            else:
                # Aplicar mapeo bilineal sobre puntos_base
                print('Aplicando mapeo bilineal sobre el resultado anterior...')
                tipo_base, puntos_base, centro_result, radio_result = mapeo_bilineal(tipo_base, puntos_base, centro_result, radio_result, a=a, b=b, c=c, d=d)

        elif opcion == '2':
            # Solicitar parámetros del mapeo lineal
            A = complex(input("Ingrese el valor de 'A': "))
            B = complex(input("Ingrese el valor de 'B': "))
            
            if puntos_base is None:
                punto1, punto2, figura, radio, centro = detector_figuras.detectar_figura_y_texto(imagen)
                print(f'Datos extraídos: punto1={punto1}, punto2={punto2}, figura={figura}, radio={radio}, centro={centro}')
                
                p1 = convertir_a_complejo(punto1)
                p2 = convertir_a_complejo(punto2)
                c_centro = convertir_a_complejo(centro)
                radio = float(radio)

                if figura == 'recta':
                    puntos_base = mapeo_lineal(punto1=p1, punto2=p2, figura=figura, radio=None, centro=None, A=A, B=B)

                elif figura == 'circulo':
                    puntos_base = mapeo_lineal(None, None, figura, radio, c_centro, A, B)
                   
            else:
                print("Aplicando mapeo lineal sobre el resultado anterior...")
                puntos_base = mapeo_lineal_aux(A, B, puntos_base, centro_result, tipo_base)
            
        elif opcion == '3':
            print("Ejemplo: Mapeo Cuadrático de un punto (2,1)")

            if puntos_base is None:
                punto1, punto2, figura, radio, centro = detector_figuras.detectar_figura_y_texto(imagen)
                print(f'Datos extraídos: punto1={punto1}, punto2={punto2}, figura={figura}, radio={radio}, centro={centro}')
                
                p1 = convertir_a_complejo(punto1)
                p2 = convertir_a_complejo(punto2)
                c_centro = convertir_a_complejo(centro)
                radio = float(radio)

                if figura == 'recta':
                    puntos_base = mapeo_cuadratico(p1, p2, figura, None, None)

                elif figura == 'circulo':
                    puntos_base = mapeo_cuadratico(None, None, figura, radio, c_centro)
                    
            else:
                print("Aplicando mapeo lineal sobre el resultado anterior...")
                # Se necesecitan pasar los números complejos a pares ordenados
                puntos_base = [(p.real, p.imag) for p in puntos_base]
                puntos_base = mapeo_cuadratico_aux(A, B, puntos_base)

        elif opcion == '4':
            print("Ejemplo: Mapeo Exponencial de una recta horizontal (x=1)")

            if puntos_base is None:
                punto1, punto2, figura, radio, centro = detector_figuras.detectar_figura_y_texto(imagen)
                print(f'Datos extraídos: punto1={punto1}, punto2={punto2}, figura={figura}, radio={radio}, centro={centro}')

                p1 = convertir_a_complejo(punto1)
                p2 = convertir_a_complejo(punto2)
                
                if figura == 'recta':
                    puntos_base = mapeo_exponencial(p1, p2)
                else:
                    print("Figura no reconocida o no detectada.")
                    break
                    
            else:
                print("Aplicando mapeo exponencial sobre el resultado anterior...")
                # Se necesecitan pasar los números complejos a pares ordenados
                puntos_base = mapeo_exponencial_aux(puntos_base)

        elif opcion == '5':
            print("Ejemplo: Mapeo Inverso de un círculo de centro (1,0) y radio 1")

            if puntos_base is None:
                punto1, punto2, figura, radio, centro = detector_figuras.detectar_figura_y_texto(imagen)
                print(f'Datos extraídos: punto1={punto1}, punto2={punto2}, figura={figura}, radio={radio}, centro={centro}')

                p1 = convertir_a_complejo(punto1)
                p2 = convertir_a_complejo(punto2)
                c_centro = convertir_a_complejo(centro)
                radio = float(radio)

                if figura == 'recta':
                    tipo_base, puntos_base, centro_result, radio_result = mapeo_inverso(figura, p1, p2, None, None)

                elif figura == 'circulo':
                    tipo_base, puntos_base, centro_result, radio_result = mapeo_inverso(figura, None, None, radio, c_centro)
                    
            else:
                print("Aplicando mapeo lineal sobre el resultado anterior...")
                # Se necesecitan pasar los números complejos a pares ordenados
                tipo_base, puntos_base, centro_result, radio_result = mapeo_inverso_aux(figura, puntos_base, centro_result, radio_result)
        else:
            print("Opción no válida.")
            break

        # Preguntar si desea aplicar otro mapeo
        print("\n¿Desea aplicar otro mapeo sobre el resultado actual?")
        print("1. Mapeo Bilineal (Möbius)")
        print("2. Mapeo Lineal")
        print("3. Mapeo Cuadrático")
        print("4. Mapeo Exponencial")
        print("5. Mapeo Inverso")
        print("0. Salir")
        opcion = input("Seleccione el tipo de mapeo (0 para salir): ")
        if opcion == '0':
            continuar = False

def convertir_a_complejo(punto):
    x, y = punto
    return complex(float(x), float(y))


if __name__ == "__main__":
    main()