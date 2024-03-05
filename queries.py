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
    print(result)
    if result and result[2] == password:
        return result[0], True
    return None, False

def verificar_credencialesMedico(username, password):
    cursor.execute("SELECT id, usuario, contraseña FROM medicoLogin WHERE usuario = %s AND contraseña = %s", (username, password,))
    result = cursor.fetchone()
    print(result)
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

def actualizar_prescripcion_con_hash(hash_unico, prescripcion_id):
    cursor.execute(
        "UPDATE prescripciones SET hash_unico = %s WHERE id_prescripcion = %s",
        (hash_unico, prescripcion_id)
    )
    conn.commit()
