import requests
import json
import hashlib


def multichain_request(method, params=[]):
    
    url = "http://127.0.0.1:6724" #Puerto RPC
    ##url = "http://localHost:6724"  # Test para no Mandar activos
    headers = {'content-type': 'application/json'}
    auth = ( 'multichainrpc' , 'FFTxtf4cHjpRaxFp9Qi7983sM8VSwUgLCBy1n1B53vwU' ) 

    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": 0,
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    try:
        return response.json()
    except ValueError:
        print("No se pudo decodificar la respuesta JSON.")
        return None

def generar_identificador_unico(data_string):
    # Usamos solo los primeros 10 caracteres del hash SHA256 para mantener el nombre del activo corto.
    return hashlib.sha256(data_string.encode()).hexdigest()[:10]


def generar_y_almacenar_nft(hash_unico, url_descarga):
    direccion_from = "16CKbjwLWwwuVY99wFm71cDHxTM6xCpJgTijwd"
    
    # Generamos un identificador único para este NFT
    identificador_unico = generar_identificador_unico(f"{hash_unico}{url_descarga}")
    nombre_unico_activo = f"nft_{identificador_unico}"
    print("Nombre Activo Blockchain : ", nombre_unico_activo)
    
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
    return respuesta, nombre_unico_activo

# Función para transferir un activo
def transferir_activo(from_address, to_address, asset_name, cantidad):
    # El nombre del activo y la cantidad ahora se pasan directamente sin usar un diccionario.
    params = [from_address, to_address, asset_name, cantidad, 0]  # Añade la cantidad directamente
    respuesta = multichain_request('sendassetfrom', params)
    print("Se transfirio asi:", respuesta)
    return respuesta

##def hacer_intransferible(asset_name, direccion_paciente):
    direccion_farmacia = "1S9QPcdS81BTVgvh6NFGh1PtCx8NACHvD4nLpi"
    params = [asset_name, {"restrict": {"send": False}}]
    respuesta = multichain_request('updatefrom', params)
    return 
    
##def quemar_activos(nft_id, cantidad, from_address, burn_address):
    # Asegúrate de que la cantidad se pasa como un número, no como un diccionario
    params = [from_address, burn_address, nft_id, cantidad]
    respuesta = multichain_request('sendassetfrom', params)
    return respuesta

##def hacer_intransferible(asset_name, from_address):
    # asset_name es el nombre del activo que deseas hacer intransferible
    params = [from_address, asset_name, {"update": {"send": False}}]
    respuesta = multichain_request('updatefrom', params)
    print("Respuesta de hacer intransferible:", respuesta)
    return respuesta

##def quemar_nft(asset_name):
    direccion_farmacia = "1S9QPcdS81BTVgvh6NFGh1PtCx8NACHvD4nLpi" 
    params = [direccion_farmacia, asset_name, {"send": False}]  # Desactivar la capacidad de enviar el activo
    respuesta = multichain_request('updatefrom', params)
    print("SE QUEMO ASI :", respuesta)
    return respuesta

