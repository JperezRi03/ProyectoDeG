from flask import render_template, request, redirect, url_for, session, flash, send_file
import pdfkit
from queries import *

def register_routes(app):

##----------------------------------- PACIENTE -------------------------------------

    @app.route('/')
    def index():
        return render_template('indexPaciente.html')

    @app.route('/paciente')
    def paciente_index():
        return render_template('indexPaciente.html')
    
    @app.route('/DashboardPaciente')
    def DashboardPaciente():
        nombre_usuario = session.get('nombre_usuario')
        ##print(nombre_usuario)
        return render_template('dashboardPaciente.html', nombre_usuario = nombre_usuario)
    
    @app.route('/login', methods=['POST'])
    def login():    
        username = request.form['username']
        password = request.form['password']
        userId, authenticated = verificar_credenciales(username, password)
    
        if authenticated:
            session['userId'] = userId
            session['nombre_usuario'] = username
            return redirect(url_for('DashboardPaciente'))
        else:
            flash('Usuario o contraseña incorrectos.', 'warning')
            return redirect(url_for('index'))
    
    @app.route('/prescripcionesUserLista')
    def prescripcionesUserLista():
        user_id = session.get('userId')
        if user_id:
            prescripciones = obtener_prescripciones_paciente(user_id)
            return render_template('prescripcionesUserLista.html', prescripciones=prescripciones)
        else:
            # Redirigir al médico a la página de inicio de sesión si no ha iniciado sesión
            return redirect(url_for('login'))


##----------------------------------- ADMINISTRADOR -------------------------------------
    @app.route('/administrador')
    def administrador_index():
        return render_template('indexAdministrador.html')
    
##----------------------------------- MEDICO -------------------------------------

    @app.route('/medico')
    def medico_index():
        return render_template('indexMédico.html')
    
    @app.route('/RegistroBos')
    def RegistroBos():
        medicamentos = obtener_medicamentos()   
        pacientes = all_usuarios()
        ##print(pacientes)
        return render_template('RegistroBos.html',medicamentos=medicamentos , pacientes=pacientes)
    
    @app.route('/DashboardMedico')
    def DashboardMedico():
        nombre_usuario = session.get('nombre_usuario')
        return render_template('dashboardMedico.html', nombre_usuario=nombre_usuario)
    
    @app.route('/loginMedico', methods=['POST'])
    def loginMedico():
        username = request.form['username']
        password = request.form['password']
        medico_id, authenticated = verificar_credencialesMedico(username, password)
        ##print(medico_id, "ESTA ES LA ID DEL MEDICO")

        if authenticated:
            session['medico_id'] = medico_id
            session['nombre_usuario'] = username
            return redirect(url_for('DashboardMedico'))
        else:
            flash('Usuario o contraseña incorrectos.', 'warning')
            return redirect(url_for('index'))
        
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

            ##print(registro_info)

            guardar_prescripcion(registro_info)
            
            return redirect(url_for('ver_registros'))
        
        return render_template('RegistroBos.html')

    @app.route('/registros')
    def ver_registros():
        registros = obtener_prescripciones_medico(session.get('medico_id'))
        return render_template('DashboardMedico.html', registros=registros)

    # Define otras rutas y funciones asociadas aquí...
    @app.route('/prescripcionesPacientesLista')
    def prescripcionesPacientesLista():
        medico_id = session.get('medico_id')
        if medico_id:
            prescripciones = obtener_prescripciones_medico(medico_id)
            ##print(prescripciones)
            return render_template('prescripcionesPacientes.html', prescripciones=prescripciones)
        else:
            # Redirigir al médico a la página de inicio de sesión si no ha iniciado sesión
            return redirect(url_for('loginMedico'))
    
##----------------------------------- FARMACIA -------------------------------------

    @app.route('/farmacia')
    def farmacia_index():
        return render_template('indexFarmacia.html')

    @app.route('/loginFarmacia', methods=['POST'])
    def loginFarm():        
        username = request.form['username']
        password = request.form['password']

        if verificar_credencialesFarmacia(username, password):
            session['nombre_usuario'] = username
            return redirect(url_for('DashboardFarmacia'))  # Puedes cambiar esto a una redirección
        else:
            flash('Usuario o contraseña incorrectos.', 'warning')  # 'warning' es la categoría del mensaje
            return redirect(url_for('farmacia'))  # Puedes mostrar un mensaje de error en tu página de inicio de sesión


    @app.route('/DashboardFarmacia')
    def DashboardFarmacia():
        nombre_usuario = session.get('nombre_usuario')
        return render_template('DashboardFarmacia.html', nombre_usuario = nombre_usuario)
    
    
    @app.route('/listaMedicamentos')
    def listaMedicamentos():
        medicamentos = obtener_medicamentos()
        ##print(medicamentos)
        return render_template('stockMedicamentos.html', medicamentos=medicamentos)
        # Redirigir al médico a la página de inicio de sesión si no ha iniciado sesión
    
    @app.route('/AMEMedicamentos')
    def AMEMedicamentos():
        medicamentos = obtener_medicamentos()
        return render_template('stockAMEmedicamentos.html', medicamentos=medicamentos)
        # Redirigir al médico a la página de inicio de sesión si no ha iniciado sesión

    @app.route('/eliminar/<int:medicamento_id>', methods=['GET'])
    def eliminar_medicamento(medicamento_id): 
            eliminar_medicamento_por_id(medicamento_id)
            return redirect('/AMEMedicamentos')
    # Aquí deberías ejecutar la lógica para eliminar el medicamento con el ID proporcionado de la base de datos
    # Después de eliminar el medicamento, redirige al usuario a la página de lista de medicamentos

    @app.route('/editar/<int:medicamento_id>', methods=['POST'])
    def editar_medicamento(medicamento_id):    
        nueva_cantidad = request.form.get('cantidad')
        if nueva_cantidad:
            modificar_medicamento_por_id(nueva_cantidad, medicamento_id)
            return redirect('/AMEMedicamentos')

    @app.route('/agregarMedicamento', methods=['GET'])
    def mostrar_formulario_agregar_medicamento():
        return render_template('agregarMedicamento.html')
    
    @app.route('/agregarMedicamento', methods=['POST'])
    def agregar_medicamento():
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        # Aquí tu lógica para insertar el nuevo medicamento en la base de datos
        # Por ejemplo:
        cursor.execute("INSERT INTO medicamentos_stock (n_medicamento, cantidad) VALUES (%s, %s)", (nombre, cantidad))
        conn.commit()
        return redirect('/AMEMedicamentos')


        
    
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
            pdf_output = "Prescripcion.pdf"

            # Configuración de pdfkit
            pdfkit.from_string(html, pdf_output, configuration=config)

            # Devolver el PDF al usuario para descargarlo
            return send_file(pdf_output, as_attachment=True)

        return render_template('muestra.html')
