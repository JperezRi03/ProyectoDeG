function validarEmail(email) {
    const re = /^[^@]+@\w+(\.\w+)+\w$/;
    return re.test(email);
}

// Función para validar la cédula
function validarCedula(cedula) {
    const re = /^\d{6}$/;
    return re.test(cedula);
}

// Agrega eventos de escucha para validar en tiempo real
document.getElementById('Correo_doc').addEventListener('input', function() {
    var email = this.value;
    if (!validarEmail(email)) {
        this.setCustomValidity('Por favor ingresa un correo electrónico válido.');
    } else {
        this.setCustomValidity('');
    }
});

document.getElementById('Cedula_Paciente').addEventListener('input', function() {
    var cedula = this.value;
    if (!validarCedula(cedula)) {
        this.setCustomValidity('La cédula debe tener 8 dígitos.');
    } else {
        this.setCustomValidity('');
    }
});
function showError(input, message) {
    const container = input.parentElement; // Encuentra el contenedor del input
    input.classList.add('input-error'); // Añade la clase de error al input
    let error = container.querySelector('.error-message'); // Busca si ya existe un mensaje de error
    if (!error) {
        error = document.createElement('div'); // Crea un nuevo elemento div para el mensaje
        error.className = 'error-message'; // Añade la clase al div
        container.appendChild(error); // Añade el mensaje de error al DOM
    }
    error.innerText = message; // Establece el texto del mensaje de error
}

function clearError(input) {
    const container = input.parentElement;
    input.classList.remove('input-error'); // Elimina la clase de error
    let error = container.querySelector('.error-message');
    if (error) {
        container.removeChild(error); // Elimina el mensaje de error del DOM
    }
}

document.getElementById('Correo_doc').addEventListener('input', function() {
    if (!validarEmail(this.value)) {
        showError(this, 'Por favor ingresa un correo electrónico válido.');
    } else {
        clearError(this);
        this.setCustomValidity('');
    }
});

document.getElementById('Cedula_Paciente').addEventListener('input', function() {
    if (!validarCedula(this.value)) {
        showError(this, 'La cédula debe tener 6 dígitos.');
    } else {
        clearError(this);
        this.setCustomValidity('');
    }
});

function validarNumeroHC(numero) {
    const re = /^\d+$/; // Expresión regular que acepta solo números
    return re.test(numero);
}

document.getElementById('numero_HC').addEventListener('input', function() {
    if (!validarNumeroHC(this.value)) {
        showError(this, 'El N° de Historia Clínica debe contener solo números.');
    } else {
        clearError(this);
        this.setCustomValidity('');
    }
});

document.getElementById('dataForm').addEventListener('submit', function(event) {
console.log('Intentando enviar formulario');
if (!this.checkValidity()) {
    console.log('Formulario no válido');
    event.preventDefault();
    event.stopPropagation();
} else {
    console.log('Formulario válido, enviando...');
}
    }, false);