const passwordInput = document.getElementById('password');
const seepassword = document.getElementById('seepassword');

seepassword.addEventListener('change', function () {
    if (this.checked) {
        passwordInput.type = 'text'; // Si el checkbox está marcado, muestra la contraseña
    } else {
        passwordInput.type = 'password'; // Si el checkbox no está marcado, oculta la contraseña
    }
});
