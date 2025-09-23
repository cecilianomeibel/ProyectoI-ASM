import easyocr

# Crear el lector de OCR en español
lector = easyocr.Reader(['es'])

# Analizar la imagen
resultado = lector.readtext("textoCirculoMami.jpg")

# Guardar texto y mostrar
for (bbox, texto, conf) in resultado:
    print(texto)
