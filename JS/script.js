document.addEventListener("DOMContentLoaded", function () {
    const infoPersonal = localStorage.getItem("Info_personal");
    const Historia_medico = localStorage.getItem("Historia_medico");
    const Info_Contacto = localStorage.getItem("Info_Contacto");
    const Diagnosticos = localStorage.getItem("Diagnosticos");
    const Tratamientos = localStorage.getItem("Tratamientos");
    const Medicos = localStorage.getItem("Medicos");
    const Medicamentos = localStorage.getItem("Medicamentos");
    const Datos_v = localStorage.getItem("Datos_v");
    const Datos_ss = localStorage.getItem("Datos_ss");

        // Accede al elemento y establece el contenido
        console.log(document.getElementById("Info_personalP").value = infoPersonal);
        console.log(document.getElementById("Historia_medicoP").value = Historia_medico);
        console.log(document.getElementById("Info_ContactoP").value = Info_Contacto);
        console.log(document.getElementById("DiagnosticosP").value = Diagnosticos);
        console.log(document.getElementById("TratamientosP").value = Tratamientos);
        console.log(document.getElementById("MedicosP").value = Medicos);
        console.log(document.getElementById("MedicamentosP").value = Medicamentos);
        console.log(document.getElementById("Datos_vP").value = Datos_v);
        console.log(document.getElementById("Datos_ssP").value = Datos_ss);

});