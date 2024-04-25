from flask import render_template, request, redirect, url_for, session, flash, send_file, jsonify
import pdfkit
import os
import qrcode
import secrets
import hashlib
from werkzeug.utils import secure_filename
from queries import *
from BlockChain import *
from qr_utils import *


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
            print(prescripciones)
            return render_template('prescripcionesUserLista.html', prescripciones=prescripciones)
        else:
            # Redirigir al médico a la página de inicio de sesión si no ha iniciado sesión
            return redirect(url_for('login'))
        
    @app.route('/mostrar_qr/<txid>')
    def mostrar_qr(txid):
        print("TXID received:", txid)  # Esto te mostrará el TXID recibido
        qr_url = obtener_qr_url_por_txid(txid)
        if qr_url:
            return send_file(qr_url, mimetype='image/png')
        else:
            flash('No se pudo encontrar el código QR.', 'error')
            return redirect(url_for('index'))



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
        cursor.execute("INSERT INTO medicamentos_stock (n_medicamento, cantidad) VALUES (%s, %s)", (nombre, cantidad))
        conn.commit()
        return redirect('/AMEMedicamentos')
    
    @app.route('/verificar_prescripcion', methods=['POST'])
    def verificar_prescripcion():
        txid = request.form['txid']
        prescripcion = obtener_prescripcion_por_txid(txid)
        if prescripcion and not prescripcion['usado']:
            return jsonify({'success': True, 'prescripcion': prescripcion})
        else:
            return jsonify({'success': False, 'error': 'Prescripción no válida o ya utilizada'})
    

    ## ----------------------------------------------------------------------------- GENERAR_PDF -----------------------------------------------------------------------------

    config= pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

    def generar_token_unico():
    # Genera un token seguro único
        return secrets.token_urlsafe(16)

    def generar_hash(prescripcion_id, token):
    # Genera un hash único basado en el ID de la prescripción y el token
        cadena = f"{prescripcion_id}{token}"
        return hashlib.sha256(cadena.encode()).hexdigest()

    @app.route('/generate_pdf', methods=['GET', 'POST'])
    def generate_pdf():
        if request.method == 'POST':            
            data = request.form.to_dict()
            prescripcion_id = data['id_prescripcion']

            # Verificar si ya existe un NFT para esta prescripción
            if existe_nft_prescripcion(prescripcion_id):
                return jsonify({'success': False, 'error': 'NFT ya creado para esta prescripción'})

            # Crear HTML a partir de la plantilla con los datos
            html = render_template('plantillapdf_Prescripcion.html', data=data)
            token = generar_token_unico()
            hash_unico = generar_hash(prescripcion_id, token)
            pdf_output = f"static/Styles/prescripcionesPDF/{hash_unico}.pdf"
            qr_output = f"static/Styles/qr/{hash_unico}.png"
            url_descarga = url_for('descargar_pdf', hash_unico=hash_unico, _external=True)
            qr = qrcode.make(url_descarga)
            qr.save(qr_output)
            pdfkit.from_string(html, pdf_output, configuration=config)

            # Crear NFT y obtener respuesta
            respuesta_blockchain, nombre_unico_activo = generar_y_almacenar_nft(hash_unico, url_descarga)
            print(respuesta_blockchain)

            if respuesta_blockchain and (respuesta_blockchain.get('error') is None):
                txid_nft = respuesta_blockchain['result']

                direccion_medico = "16CKbjwLWwwuVY99wFm71cDHxTM6xCpJgTijwd"  # Reemplazar con la dirección real del médico
                direccion_paciente = "1Hmx2WyQNCo4CyQsjJvwttzHv5DckpPRJCMVq5"  # Dirección del paciente  # DireccionDelPaciente

                transferir_activo(direccion_medico, direccion_paciente, nombre_unico_activo, 1)

                actualizar_prescripcion_con_txid(txid_nft, hash_unico, prescripcion_id)
                actualizar_prescripcion_con_qr_url(qr_output, prescripcion_id)

                return jsonify({'success': True, 'txid': txid_nft})
            else:
                return jsonify({'success': False, 'error': respuesta_blockchain.get('error', 'Error desconocido')})

    @app.route('/descargar_pdf/<hash_unico>')
    def descargar_pdf(hash_unico):
        print(hash_unico)
        # Verificar en la base de datos si el hash ya ha sido utilizado
        cursor.execute("SELECT usado FROM prescripciones WHERE hash_unico = %s", (hash_unico,))
        resultado = cursor.fetchone()
        
        if resultado is None:
            # Si no existe un registro con ese hash, es probablemente un enlace inválido
            return jsonify({'error': 'El enlace es inválido o ha ocurrido un error.'}), 404
        
        usado = resultado[0]
        if usado:
            # Si el hash ya fue utilizado, redirigir a una página de error o mensaje
            return jsonify({'error': 'Este enlace ya ha sido utilizado.'}), 400
        else:
            # Devolver información para la descarga sin marcar como usado
            return jsonify({'message': 'El PDF está listo para ser descargado.', 'url': url_for('realizar_descarga', hash_unico=hash_unico, _external=True)})

    @app.route('/realizar_descarga/<hash_unico>')
    def realizar_descarga(hash_unico):
        # Primero verifica si el hash ya ha sido utilizado
        cursor.execute("SELECT usado FROM prescripciones WHERE hash_unico = %s", (hash_unico,))
        resultado = cursor.fetchone()
        if resultado is None:
            # Si el resultado es None, significa que no se encontró el hash, podría ser un error o enlace inválido
            return jsonify({'error': 'El enlace es inválido o ha ocurrido un error.'}), 404
        elif resultado[0]:  # Comprobar si el valor de "usado" es True
            # Si el hash ya fue utilizado, envía una respuesta de error
            return jsonify({'error': 'Este enlace ya ha sido utilizado.'}), 403
        else:
            # Si no ha sido usado, marcarlo como usado y permitir la descarga
            
            cursor.execute("UPDATE prescripciones SET usado = TRUE WHERE hash_unico = %s", (hash_unico,))
            conn.commit()
            path_al_pdf = f"static/Styles/prescripcionesPDF/{hash_unico}.pdf"
            
            if os.path.exists(path_al_pdf):
                return send_file(path_al_pdf, as_attachment=True)
            else:
                return jsonify({'error': 'El archivo PDF solicitado no existe.'}), 404


        
## ----------------------------------------------------------------------------- QR LOGICS -----------------------------------------------------------------------------

    UPLOAD_FOLDER = 'static\Styles\qr'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/procesar_qr', methods=['POST'])
    def procesar_qr():
        if 'qrImage' not in request.files:
            return jsonify({'success': False, 'error': 'No se proporcionó ninguna imagen.'})

        file = request.files['qrImage']
        if file and allowed_file(file.filename):
            qr_data = decodificar_imagen_qr(file)
            if qr_data:
                # Procesamiento adicional con qr_data si es necesario
                return jsonify({'success': True, 'data': qr_data})
            else:
                return jsonify({'success': False, 'error': 'No se pudo decodificar el código QR.'})
        
        return jsonify({'success': False, 'error': 'Archivo no permitido o no proporcionado.'})

    


## GENERAR UN NFT CON LOS DATOS, COGER LOS DATOS GENERAR UN NFT 

## Una aplicación web para la interacción con los usuarios, y una API REST para consumir los recursos de la plataforma de interoperabilidad. red Blockchain bajo la
## plataforma Multichain, la cual contine un API JSON-RPC que recibe datos
## transaccionales desde la plataforma de control y los transfiere entre los nodos de la cadena



