import cv2
import numpy as np
import easyocr
import re

IMG_PATH = 'textoCirculo6.jpeg'

# Cargar imagen
img = cv2.imread(IMG_PATH)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blur, 50, 150)

# Detectar figura principal (solo una por imagen)
figura = None

# Detectar recta
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)
if lines is not None and len(lines) > 0:
    figura = 'recta'

# Si no es recta, buscar círculo
if figura is None:
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50, param1=50, param2=30, minRadius=10, maxRadius=0)
    if circles is not None and len(circles[0]) > 0:
        figura = 'circulo'

if figura:
    print(f'Figura detectada: {figura}')
else:
    print('No se detectó ninguna figura')

# OCR para extraer texto
lector = easyocr.Reader(['es'])
resultado = lector.readtext(IMG_PATH)
texto_completo = ' '.join([texto for (_, texto, _) in resultado])

print(f'Texto detectado por OCR: "{texto_completo}"')
# Extraer datos del texto según la figura
if figura == 'recta':
    # Normalizar texto para corregir errores comunes de OCR
    texto_norm = texto_completo.replace('l', '1').replace('I', '1')
    texto_norm = texto_norm.replace('O', '0').replace('o', '0')
    texto_norm = texto_norm.replace('|', '1')
    texto_norm = texto_norm.replace('.', ',').replace(';', ',').replace(':', ',')
    # Buscar dos puntos con separadores flexibles y números negativos
    puntos = re.findall(r'\(\s*(-?\d+)\s*[,;\s]+\s*(-?\d+)\s*\)', texto_norm)
    if len(puntos) >= 2:
        (x1, y1), (x2, y2) = puntos[0], puntos[1]
        print(f'Punto inicial: ({x1},{y1})')
        print(f'Punto final: ({x2},{y2})')
    else:
        print('No se encontraron dos puntos en el texto.')
elif figura == 'circulo':
    # Normalizar texto para corregir errores comunes de OCR
    texto_norm = texto_completo.replace('l', '1').replace('I', '1')
    texto_norm = texto_norm.replace('O', '0').replace('o', '0')
    texto_norm = texto_norm.replace('|', '1')
    texto_norm = texto_norm.replace('.', ',').replace(';', ',').replace(':', ',').replace('=', ':')
    # Corregir errores de OCR: 'K', 'k', 'Y', 'y' por 'r', y 'z' por '=' o ':'
    texto_norm = re.sub(r'([KkYy])', 'r', texto_norm)
    texto_norm = texto_norm.replace('z', ':')
    # Buscar todos los radios y centros posibles
    radios = re.findall(r'r\s*[:=,\s]+\s*(\d+)', texto_norm, re.IGNORECASE)
    centros = re.findall(r'\(\s*(-?\d+)\s*[,;\s]+\s*(-?\d+)\s*\)', texto_norm)
    if radios:
        print(f'Radio: {radios[0]}')
    else:
        print('No se encontró radio en el texto.')
    if centros:
        x, y = centros[0]
        print(f'Centro: ({x},{y})')
    else:
        print('No se encontró centro en el texto.')
