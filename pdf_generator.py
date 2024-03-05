import pdfkit
import os
import qrcode

from flask import render_template, request, send_file, url_for, redirect

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
        prescripcion_id = data['id_prescripcion']

        # Crear HTML a partir de la plantilla con los datos
        html = render_template('plantillapdf_Prescripcion.html', data=data)

        # Ruta para el archivo PDF de salida
        pdf_output = f"static/prescripcionesPDF/{prescripcion_id}.pdf"
        
        # Generar el código QR
        qr_output = f"static/qr/{prescripcion_id}.png"
        url_descarga = url_for('descargar_pdf', prescripcion_id=prescripcion_id, _external=True)
        qr = qrcode.make(url_descarga)
        qr.save(qr_output)
        return redirect(url_descarga)

        # Configuración de pdfkit
        pdfkit.from_string(html, pdf_output, configuration=config)

        # Devolver el PDF al usuario para descargarlo
        return send_file(pdf_output, as_attachment=True)

    return render_template('muestra.html')

@app.route('/descargar_pdf/<prescripcion_id>')
def descargar_pdf(prescripcion_id):
    path_al_pdf = f"static/prescripciones/{prescripcion_id}.pdf"
    return send_file(path_al_pdf, as_attachment=True)

# Define otras funciones para generar PDF aquí...
