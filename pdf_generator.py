import pdfkit
from flask import render_template, request, send_file

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

# Define otras funciones para generar PDF aquí...
