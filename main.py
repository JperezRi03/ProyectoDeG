import os
from flask import Flask, render_template, request, flash, redirect, url_for, session, Response
from flask_weasyprint import HTML, render_pdf

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
    cursor.execute("SELECT usuario, contraseña FROM medicoLogin WHERE usuario = %s AND contraseña = %s", (username, password,))
    result = cursor.fetchone()
    if result and result[1] == password:
        return True
    return False




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
    # Aquí va la lógica para la página de la farmacia
    return render_template('RegistroBos.html')



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

    if verificar_credencialesMedico(username, password):
        session['nombre_usuario'] = username
        return redirect(url_for('DashboardMedico'))  # Puedes cambiar esto a una redirección
    else:
        flash('Usuario o contraseña incorrectos.', 'warning')  # 'warning' es la categoría del mensaje
        return redirect(url_for('index'))  # Puedes mostrar un mensaje de error en tu página de inicio de sesión

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
            'diagnostico': diagnostico
        }

    # Insertar en la tabla prescripciones
        
        # Agregar el registro a la lista.
        registros.append(registro_info)
        
        # Redirigir a la página de visualización, por ejemplo.
        return redirect(url_for('ver_registros'))
    
    # Mostrar el formulario en GET request.
    return render_template('RegistroBos.html')

@app.route('/registros')
def ver_registros():
    # Pasar la lista de registros al template.
    return render_template('VerRegistro.html', registros=registros)


## ----------------------------------------------------------------------------- GENERAR_PDF -----------------------------------------------------------------------------

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():


    nombre_doc = request.form['nombre_doc']
    # Recoge los datos del formulario
    data = {
        'nombre_doc': nombre_doc,
        ##'Fecha_Pres': request.form.get('Fecha_Pres', ''),
        ##'entidad': request.form.get('entidad', ''),
        # ... más datos del formulario ...
    }
    
    # Renderiza tu plantilla HTML con los datos
    rendered_html = render_template('plantillapdf_Prescripcion.html', **data)
    
    # Convierte el HTML renderizado en un PDF y envíalo como respuesta
    return render_pdf(HTML(string=rendered_html))

## ----------------------------------------------------------------------------- MAIN -----------------------------------------------------------------------------
if __name__ == '__main__':
    app.secret_key = 'Val06Ju'  # Necesitas configurar una clave secreta para los mensajes flash
    app.run(debug = True, host = '127.0.0.1', port = 5000)
