import requests
import json
import hashlib


def multichain_request(method, params=[]):
    
    url = "http://127.0.0.1:5788" #Puerto RPC
    headers = {'content-type': 'application/json'}
    auth = ( 'multichainrpc' , 'AVMW5ryb7x7kgt4GnKqEkHLB1syqY5Hd2jtZC3Bptvz7' ) 

    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": 0,
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    print(response.status_code)
    try:
        return response.json()
    except ValueError:
        print("No se pudo decodificar la respuesta JSON.")
        return None

def generar_identificador_unico(data_string):
    return hashlib.sha256(data_string.encode()).hexdigest()

def generar_y_almacenar_nft(hash_unico, url_descarga):
    direccion_from = "1TpazdQRapnPVy6ANJjBiQPjNBGFPSJsQ1CiHR"
    
    # Generamos un identificador único para este NFT
    identificador_unico = generar_identificador_unico(f"{hash_unico}{url_descarga}")
    nombre_unico_activo = f"nft_{identificador_unico}"
    print(nombre_unico_activo)
    
    # Asegurándonos de que 'nft_data' es un diccionario con la estructura correcta.
    nft_data = {"json": {"hash": hash_unico, "url_descarga": url_descarga}}

    # Emitiendo más cantidad del activo existente 'qr_nfts'.
    params = [
        direccion_from,
        nombre_unico_activo,  # Nombre único para el nuevo activo
        1,  # Cantidad a emitir
        1,  # Unidades
        0,  # Cantidad de la moneda nativa
        nft_data  # Datos detallados como un diccionario
    ]
    
    respuesta = multichain_request('issue', params)
    print("Respuesta de la emisión del NFT:", respuesta)
    return respuesta