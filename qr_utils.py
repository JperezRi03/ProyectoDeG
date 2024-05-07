from pyzbar.pyzbar import decode
from PIL import Image
import io

##--------------------------- Medidor de Tiempos ---------------------------
import time

def cronometrar_funcion(func):
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        print(f"Tiempo de ejecución de '{func.__name__}': {fin - inicio} segundos")
        return resultado
    return wrapper
##--------------------------- Medidor de Tiempos ---------------------------

@cronometrar_funcion
def decodificar_imagen_qr(imagen):
    # Decodifica la imagen QR y devuelve los datos
    qr_code_image = Image.open(io.BytesIO(imagen.read()))
    qr_result = decode(qr_code_image)
    if qr_result:
        qr_data = qr_result[0].data.decode()
        return qr_data
    return None


