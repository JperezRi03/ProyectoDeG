import os
from flask import Flask, render_template, request, flash, redirect, url_for, session, Response, send_file
import pdfkit
##from flask_weasyprint import HTML, render_pdf

import psycopg2

app = Flask('test', template_folder= 'templates')

# Establece la conexión a la base de datos
conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='123',
    host='localhost'
)
# Crea un cursor para ejecutar consultas SQL
cursor = conn.cursor()

## ----------------------------------------------------------------------------- QUERYS -----------------------------------------------------------------------------

# Función para verificar las credenciales de inicio de sesión
def verificar_credenciales(username, password):
    cursor.execute("SELECT usuario, contraseña FROM userlogin WHERE usuario = %s AND contraseña = %s", (username, password,))
    result = cursor.fetchone()
    if result and result[1] == password:
        return True
    return False

def verificar_credencialesMedico(username, password):
    cursor.execute("SELECT id, usuario, contraseña FROM medicoLogin WHERE usuario = %s AND contraseña = %s", (username, password,))
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

def guardar_prescripcion(data):
    medico_id = session.get('medico_id')


    cursor.execute(
        "INSERT INTO prescripciones (id_medico, id_medicamento, nombre_medicamento, nombre_doc, correo_doc, lugar_prescripcion, fecha_prescripcion, nombre_paciente, cedula_paciente, numero_hc, tipo_usuario, dosis_diaria, duracion_tratamiento, cantidad_total_medicamento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (medico_id, 1, data['forma_farmaceutica'], data['nombre_doc'], data['correo_doc'], data['Lugar_Pres'], data['Fecha_Pres'], data['nombre_paciente'], data['cedula_paciente'], data['numero_hc'], data['tipo_usuario'], data['dosis_diaria'], data['duracion_tratamiento'], data['cantidad_total'])
    )
    conn.commit()



## ----------------------------------------------------------------------------- RUTAS -----------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('indexPaciente.html')

@app.route('/paciente')
def paciente_index():
    # Aquí va la lógica para la página del paciente
    return render_template('indexPaciente.html')

@app.route('/administrador')
def administrador_index():
    # Aquí va la lógica para la página del administrador
    return render_template('indexAdministrador.html')

@app.route('/medico')
def medico_index():
    # Aquí va la lógica para la página del médico
    return render_template('indexMédico.html')

@app.route('/farmacia')
def farmacia_index():
    # Aquí va la lógica para la página de la farmacia
    return render_template('indexFarmacia.html')

@app.route('/RegistroBos')
def RegistroBos():
    medicamentos = obtener_medicamentos()   
    ##print(medicamentos)
    return render_template('RegistroBos.html',medicamentos=medicamentos)



## ----------------------------------------------------------------------------- Paciente -----------------------------------------------------------------------------

@app.route('/login', methods=['POST'])
def login():    
    username = request.form['username']
    password = request.form['password']

    if verificar_credenciales(username, password):
        session['nombre_usuario'] = username
        return redirect(url_for('DashboardPaciente'))  # Puedes cambiar esto a una redirección
    else:
        flash('Usuario o contraseña incorrectos.', 'warning')  # 'warning' es la categoría del mensaje
        return redirect(url_for('index'))  # Puedes mostrar un mensaje de error en tu página de inicio de sesión
    

@app.route('/DashboardPaciente')
def DashboardPaciente():
    nombre_usuario = session.get('nombre_usuario')
    return render_template('dashboardPaciente.html', nombre_usuario = nombre_usuario)
    

## ----------------------------------------------------------------------------- MEDICO -----------------------------------------------------------------------------

@app.route('/loginMedico', methods=['POST'])
def loginMedico():
    username = request.form['username']
    password = request.form['password']
    medico_id, authenticated = verificar_credencialesMedico(username, password)

    if authenticated:
        session['medico_id'] = medico_id  # Almacena el ID del médico en la sesión
        session['nombre_usuario'] = username
        return redirect(url_for('DashboardMedico'))
    else:
        flash('Usuario o contraseña incorrectos.', 'warning')
        return redirect(url_for('index'))


@app.route('/DashboardMedico')
def DashboardMedico():
    nombre_usuario = session.get('nombre_usuario')
    return render_template('DashboardMedico.html', nombre_usuario = nombre_usuario)

registros = []
@app.route('/DashboardMedico', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':

        # Captura la información del formulario.
        nombre_doc = request.form['nombre_doc']
        correo_doc = request.form['Correo_doc']
        Lugar_Pres = request.form['Lugar_Pres']
        Fecha_Pres = request.form['Fecha_Pres']
        nombre_paciente = request.form['Nombre_Paciente']
        cedula_paciente = request.form['Cedula_Paciente']
        numero_hc = request.form['numero_HC']
        tipo_usuario = request.form['tipo_usuario']
        forma_farmaceutica = request.form['forma_farmaceutica']
        dosis_diaria = request.form['dosis_diaria']
        duracion_tratamiento = request.form['duracion_tratamiento']
        cantidad_total = request.form['cantidad_total']
        diagnostico = request.form['diagnostico']
        
        # Crear un diccionario con la información.
        registro_info = {
            'nombre_doc': nombre_doc,
            'correo_doc': correo_doc,
            'Lugar_Pres': Lugar_Pres,
            'Fecha_Pres': Fecha_Pres,
            'nombre_paciente': nombre_paciente,
            'cedula_paciente': cedula_paciente,
            'numero_hc': numero_hc,
            'tipo_usuario': tipo_usuario,
            'forma_farmaceutica': forma_farmaceutica,
            'dosis_diaria': dosis_diaria,
            'duracion_tratamiento': duracion_tratamiento,
            'cantidad_total': cantidad_total,
            'diagnostico': diagnostico,
        }

        print(registro_info)

    # Insertar en la tabla prescripciones
        
        # Agregar el registro a la lista.
        registros.append(registro_info)
        guardar_prescripcion(registro_info)
        
        # Redirigir a la página de visualización, por ejemplo.
        return redirect(url_for('ver_registros'))
    
    # Mostrar el formulario en GET request.
    return render_template('RegistroBos.html')

@app.route('/registros')
def ver_registros():
    # Pasar la lista de registros al template.
    return render_template('VerRegistro.html', registros=registros)


## ----------------------------------------------------------------------------- GENERAR_PDF -----------------------------------------------------------------------------
config= pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")


@app.route('/generate_pdf', methods=['GET', 'POST'])
def generate_pdf():
    if request.method == 'POST':
        # Recoger datos del formulario
        data = request.form.to_dict()
        ##print(data)



        nombre_doc = data['nombre_doc']
        correo_doc = data['correo_doc']
        Lugar_Pres = data['Lugar_Pres']
        Fecha_Pres = data['Fecha_Pres']
        nombre_paciente = data['nombre_paciente']
        cedula_paciente = data['cedula_paciente']
        numero_hc = data['numero_hc']
        tipo_usuario = data['tipo_usuario']
        forma_farmaceutica = data['forma_farmaceutica']
        dosis_diaria = data['dosis_diaria']
        duracion_tratamiento = data['duracion_tratamiento']
        cantidad_total = data['cantidad_total']
        diagnostico = data['diagnostico']

        # Crear HTML a partir de la plantilla con los datos
        html = render_template('plantillapdf_Prescripcion.html', data=data)

        # Ruta para el archivo PDF de salida
        pdf_output = "output.pdf"

        # Configuración de pdfkit
        pdfkit.from_string(html, pdf_output, configuration=config)

        # Devolver el PDF al usuario para descargarlo
        return send_file(pdf_output, as_attachment=True)

    return render_template('muestra.html')


## ----------------------------------------------------------------------------- MAIN -----------------------------------------------------------------------------
if __name__ == '__main__':
    app.secret_key = 'Val06Ju'  # Necesitas configurar una clave secreta para los mensajes flash
    app.run(debug = True, host = '127.0.0.1', port = 5000)
