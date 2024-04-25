const loginButton = document.getElementById('login-button');
const userTypeRadios = document.querySelectorAll('input[name="user-type"]');
const selectedUserType = document.getElementById('selected-user-type');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');

loginButton.addEventListener('click', () => {
    // Aquí puedes agregar la lógica para iniciar sesión
    alert('Iniciar sesión como ' + getSelectedUserType());
});

userTypeRadios.forEach(radio => {
    radio.addEventListener('change', () => {
        selectedUserType.innerText = radio.value.charAt(0).toUpperCase();
    });
});

function getSelectedUserType() {
    for (const radio of userTypeRadios) {
        if (radio.checked) {
            return radio.value;
        }
    }
}
