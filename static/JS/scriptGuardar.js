// Página de ingreso de datos
document.getElementById("guardar-btn").addEventListener("click", function () {
    // Guardar los datos ingresados
    const Info_personal = document.getElementById("Info_personal").value;
    const Historia_medico = document.getElementById("Historia_medico").value;
    const Info_Contacto = document.getElementById("Info_Contacto").value;
    const Diagnosticos = document.getElementById("Diagnosticos").value;
    const Tratamientos = document.getElementById("Tratamientos").value;
    const Medicos = document.getElementById("Medicos").value;
    const Medicamentos = document.getElementById("Medicamentos").value;
    const Datos_v = document.getElementById("Datos_v").value;
    const Datos_ss = document.getElementById("Datos_ss").value;
    // Guardar los datos en el LocalStorage

    localStorage.setItem("Info_personal", Info_personal);
    localStorage.setItem("Historia_medico", Historia_medico);
    localStorage.setItem("Info_Contacto", Info_Contacto);
    localStorage.setItem("Diagnosticos", Diagnosticos);
    localStorage.setItem("Tratamientos", Tratamientos);
    localStorage.setItem("Medicos", Medicos);
    localStorage.setItem("Medicamentos", Medicamentos);
    localStorage.setItem("Datos_v", Datos_v);
    localStorage.setItem("Datos_ss", Datos_ss);

    // Redirigir a la página de previsualización
    window.location.href = "preview.html";
});
