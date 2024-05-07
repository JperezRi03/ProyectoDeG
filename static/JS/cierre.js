var tiempoInactividad = 3 * 60 * 1000; // 3 minutos
var tiempoAviso = 1 * 60 * 1000; // 1 minuto antes del cierre
var timer;

function resetTimer() {
    clearTimeout(timer);
    timer = setTimeout(function() {
        $('#sessionTimeoutModal').modal('show'); // Muestra el modal para extender la sesión
        // Después del aviso, espera 1 minuto antes de cerrar la sesión
        setTimeout(logout, tiempoAviso);
    }, tiempoInactividad - tiempoAviso);
}

function logout() {
    window.location.href = '/paciente'; // Asegúrate de modificar con la URL correcta de logout
}

window.onload = resetTimer;
document.onmousemove = resetTimer;
document.onkeypress = resetTimer;
