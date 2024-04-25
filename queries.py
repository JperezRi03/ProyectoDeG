import psycopg2
from flask import session

# Establece la conexión a la base de datos
conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='123',
    host='localhost'
)
cursor = conn.cursor()

# Funciones para consultar la base de datos
# Función para verificar las credenciales de inicio de sesión
def verificar_credenciales(username, password):
    cursor.execute("SELECT id, usuario, contraseña FROM userlogin WHERE usuario = %s AND contraseña = %s", (username, password,))
    result = cursor.fetchone()
    if result and result[2] == password:
        return result[0], True
    return None, False

def verificar_credencialesMedico(username, password):
    cursor.execute("SELECT id, usuario, contraseña FROM medicoLogin WHERE usuario = %s AND contraseña = %s", (username, password,))
    result = cursor.fetchone()
    if result and result[2] == password:
        return result[0], True  # Devuelve el ID y True si las credenciales son correctas
    return None, False

def verificar_credencialesFarmacia(username, password):
    cursor.execute("SELECT id, usuario, contraseña FROM farmalogin WHERE usuario = %s AND contraseña = %s", (username, password,))
    result = cursor.fetchone()
    if result and result[2] == password:
        return result[0], True  # Devuelve el ID y True si las credenciales son correctas
    return None, False

def obtener_medicamentos():
    # Consulta SQL que devuelve todos los medicamentos en la BD
    cursor.execute("SELECT * FROM medicamentos_Stock")
    data = cursor.fetchall()
    # Devuelve una lista de tuplas
    return data

def all_usuarios():
    # Consulta SQL que devuelve todos los medicamentos en la BD
    cursor.execute("select * from userLogin")
    data = cursor.fetchall()
    # Devuelve una lista de tuplas
    return data



def guardar_prescripcion(data):
    medico_id = session.get('medico_id')
    cantidad_total = data['cantidad_total']
    cursor.execute(
            "INSERT INTO prescripciones (id_medico, id_medicamento, id_user , nombre_medicamento, nombre_doc, correo_doc, lugar_prescripcion, fecha_prescripcion, nombre_paciente, cedula_paciente, numero_hc, tipo_usuario, dosis_diaria, duracion_tratamiento, cantidad_total_medicamento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (medico_id, 1, 1, data['forma_farmaceutica'], data['nombre_doc'], data['correo_doc'], data['Lugar_Pres'], data['Fecha_Pres'], data['nombre_paciente'], data['cedula_paciente'], data['numero_hc'], data['tipo_usuario'], data['dosis_diaria'], data['duracion_tratamiento'], cantidad_total)
        )
        
        # Actualizar el stock del medicamento
    cursor.execute(
            "UPDATE medicamentos_stock SET cantidad = CAST(Cantidad AS INT) - %s WHERE id_medicamento = 1",
            (cantidad_total,)  # Se pasa como una tupla de un solo elemento
        )
    
    conn.commit()

def obtener_prescripciones_medico(medico_id):
    cursor.execute(
        "SELECT * FROM prescripciones WHERE id_medico = %s",
        (medico_id,)
    )
    prescripciones = cursor.fetchall()
    return prescripciones

def obtener_prescripciones_paciente(nombre_usuario):
    cursor.execute(
        "SELECT * FROM prescripciones WHERE id_user = %s",
        (nombre_usuario,)
    )
    prescripciones = cursor.fetchall()
    return prescripciones

def eliminar_medicamento_por_id(medicamento_id):
    try:
        with conn:
            cursor.execute(
                "DELETE FROM medicamentos_stock WHERE id_medicamento=%s",
                (str(medicamento_id),)
            )
        return True
    except Exception as e:
        print("Error al intentar eliminar el medicamento: ", str(e))
        return False

def modificar_medicamento_por_id( nueva_cantidad, medicamento_id):
     cursor.execute(
                "update medicamentos_stock set cantidad = %s WHERE id_medicamento = %s",
                ( nueva_cantidad, medicamento_id)
            )
     conn.commit()

def actualizar_prescripcion_con_txid(txid_nft, hash_unico, prescripcion_id):
    cursor.execute(
        "UPDATE prescripciones SET txid_nft = %s, hash_unico = %s WHERE id_prescripcion = %s",
        (txid_nft, hash_unico, prescripcion_id)
    )
    conn.commit()

def existe_nft_prescripcion(prescripcion_id):
    # Esta función debe consultar la base de datos y verificar si ya existe un txid_nft para la prescripción
    cursor.execute("SELECT txid_nft FROM prescripciones WHERE id_prescripcion = %s", (prescripcion_id,))
    resultado = cursor.fetchone()
    return resultado is not None and resultado[0] is not None

def actualizar_prescripcion_con_qr_url(qr_url, prescripcion_id):
    try:
        # Asegúrate de tener una conexión abierta a la base de datos (conn) y un cursor disponible
        cursor.execute(
            "UPDATE prescripciones SET qr_url = %s WHERE id_prescripcion = %s",
            (qr_url, prescripcion_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar la URL del QR:", e)
        return False

def obtener_qr_url_por_txid(txid):
    cursor.execute("SELECT qr_url FROM prescripciones WHERE txid_nft = %s", (txid,))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None

def obtener_prescripcion_por_txid(txid):
    try:
        cursor.execute("SELECT * FROM prescripciones WHERE txid_nft = %s", (txid,))
        resultado = cursor.fetchone()
        if resultado:
            # Construye un diccionario con los datos de la prescripción
            prescripcion = {
                'id_prescripcion': resultado[0],
                'id_medico': resultado[1],
                'id_medicamento': resultado[2],
                'id_user': resultado[3],
                'nombre_medicamento': resultado[4],
                'nombre_doc': resultado[5],
                'correo_doc': resultado[6],
                'lugar_prescripcion': resultado[7],
                'fecha_prescripcion': resultado[8],
                'nombre_paciente': resultado[9],
                'cedula_paciente': resultado[10],
                'numero_hc': resultado[11],
                'tipo_usuario': resultado[12],
                'dosis_diaria': resultado[13],
                'duracion_tratamiento': resultado[14],
                'cantidad_total_medicamento': resultado[15],
                'hash_unico': resultado[16],
                'usado': resultado[17],
                'txid_nft': resultado[18],
                'qr_url': resultado[19]
            }
            return prescripcion
        else:
            return None
    except Exception as e:
        print("Error al obtener la prescripción por txid:", str(e))
        return None

