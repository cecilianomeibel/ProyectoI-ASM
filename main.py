
# Importar funciones de los módulos
import detector_figuras
from mapeo_lineal import mapeo_lineal
from mapeo_bilineal import mapeo_bilineal
#from mapeo_cuadratico import mapeo_cuadratico, mostrar_grafico_comparativo as mostrar_grafico_cuadratico
from mapeo_exponencial import mapeo_exponencial, visualizar_mapeo
from mapeo_inverso import mapeo_inverso, mostrar_grafico_comparativo as mostrar_grafico_inverso

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
    tipo_base = None
    continuar = True
    while continuar:
        if opcion == '1':
            if puntos_base is None:
                punto1, punto2, figura, radio, centro = detector_figuras.detectar_figura_y_texto(imagen)
                print(f'Datos extraídos: punto1={punto1}, punto2={punto2}, figura={figura}, radio={radio}, centro={centro}')
                if figura == 'recta':
                    x1, y1 = punto1
                    x2, y2 = punto2
                    p1 = complex(float(x1), float(y1))
                    p2 = complex(float(x2), float(y2))
                    _, _, puntos_base = mapeo_bilineal('recta', punto1=p1, punto2=p2, a=0+0j, b=1+0j, c=1+0j, d=0+0j)
                    tipo_base = 'recta'
                elif figura == 'circulo':
                    r = float(radio)
                    x, y = centro
                    c = complex(float(x), float(y))
                    _, _, puntos_base = mapeo_bilineal('circulo', centro=c, radio=r, a=0+0j, b=1+0j, c=1+0j, d=0+0j)
                    tipo_base = 'circulo'
                else:
                    print('Figura no reconocida o no detectada.')
                    break
            else:
                # Aplicar mapeo bilineal sobre puntos_base
                print('Aplicando mapeo bilineal sobre el resultado anterior...')
                # Por simplicidad, asumimos que el usuario quiere usar los mismos parámetros
                _, _, puntos_base = mapeo_bilineal(tipo_base, punto1=puntos_base[0], punto2=puntos_base[-1], a=0+0j, b=1+0j, c=1+0j, d=0+0j)
        elif opcion == '2':
            print("Ejemplo: Mapeo Lineal de un círculo (A=2+0j, B=1+1j, centro=0, radio=2)")
            # Aquí deberías adaptar para aceptar puntos_base si no es None
            #mapeo_lineal(A=2+0j, B=1+1j, tipo_figura='circulo', centro=0, radio=2)
            puntos_base = None
        elif opcion == '3':
            print("Ejemplo: Mapeo Cuadrático de un punto (2,1)")
            #z = (2, 1)
            #w = mapeo_cuadratico(z, modo='cartesiano')
            #mostrar_grafico_cuadratico(z, w, titulo_izq="Original (2,1)", titulo_der="Mapeo cuadrático")
            puntos_base = None
        elif opcion == '4':
            print("Ejemplo: Mapeo Exponencial de una recta horizontal (x=1)")
            #z2, w2 = mapeo_exponencial(x=1, y=None)
            #visualizar_mapeo(z2, w2, "Recta horizontal (x=1) -> Círculo de radio e^1")
            puntos_base = None
        elif opcion == '5':
            print("Ejemplo: Mapeo Inverso de un círculo de centro (1,0) y radio 1")
            #entrada = ("circulo", (1,0), 1)
            #salida = mapeo_inverso("circulo", (1,0), 1)
            #mostrar_grafico_inverso(entrada, salida)
            puntos_base = None
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
if __name__ == "__main__":
    main()