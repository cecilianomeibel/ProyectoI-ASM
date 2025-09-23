
# Importar funciones de los módulos
from mapeo_lineal import mapeo_lineal
from mapeo_bilineal import mapeo_bilineal, valida_imagen
from mapeo_cuadratico import mapeo_cuadratico, mostrar_grafico_comparativo as mostrar_grafico_cuadratico
from mapeo_exponencial import mapeo_exponencial, visualizar_mapeo
from mapeo_inverso import mapeo_inverso, mostrar_grafico_comparativo as mostrar_grafico_inverso

def main():
    print("\n=== Ejemplo 1: Mapeo Lineal de un círculo ===")
    mapeo_lineal(A=2+0j, B=1+1j, tipo_figura='circulo', centro=0, radio=2)

    print("\n=== Ejemplo 2: Círculo bajo mapeo bilineal general ===")
    print("Transformación: w = (2z+1)/(z+1), círculo de centro (1,0) y radio 1.")
    Z, W, zs, pasa, tipo_resultado = mapeo_bilineal(2, 1, 1, 1, 'circulo', centro=1+0j, radio=1.0)
    print("  Resultado obtenido:")
    valida_imagen(W, tipo_resultado)

    print("\n=== Ejemplo 3: Mapeo Cuadrático de un punto (2,1) ===")
    z = (2, 1)
    w = mapeo_cuadratico(z, modo='cartesiano')
    mostrar_grafico_cuadratico(z, w, titulo_izq="Original (2,1)", titulo_der="Mapeo cuadrático")

    print("\n=== Ejemplo 4: Mapeo Inverso de un círculo de centro (1,0) y radio 1 ===")
    entrada = ("circulo", (1,0), 1)
    salida = mapeo_inverso("circulo", (1,0), 1)
    mostrar_grafico_inverso(entrada, salida)

    print("\n=== Ejemplo 5: Mapeo Exponencial de una recta horizontal (x=1) ===")
    z2, w2 = mapeo_exponencial(x=1, y=None)
    visualizar_mapeo(z2, w2, "Recta horizontal (x=1) -> Círculo de radio e^1")

if __name__ == "__main__":
    main()