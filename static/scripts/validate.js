function validate(){
    // is_true = (validate_email() && validate_password());
    var fields = ['email', 'password', 'repeat_password', 'name', 'last_name', 'city', 'zip_code', 'street', 'house_number', 'flat_number']
    if (document.getElementById(fields[3])) {
        document.getElementById('error_testowy').innerHTML = 'jest'
    }
    // return is_true;
    return false;
}

// walidacja e-maila
var emailField = document.getElementById('email');

function validate_email(){
    if (emailField.value == ""){
        document.getElementById('email_field_error').innerHTML = "Pole wymagane!"

    }
    else if (emailField.value == "xyz"){
        document.getElementById('email_field_error').innerHTML = "Nieprawidłowy e-mail!"
    }
    else {
        document.getElementById('email_field_error').innerHTML = ""
        return true;
    }
    return false;
}
emailField.addEventListener('blur', validate_email);

// walidacja hasła
var passwordField = document.getElementById('password');
var passwordRepeatField = document.getElementById('repeat_password');

function validatePassword(){
    passwordField.addEventListener('blur', validatePassword);
    if (passwordField.value == "" || passwordRepeatField == "") {
        document.getElementById('pw_field_error').innerHTML = "Oba pola wymagane!"
        return false;
    }
    if (passwordField.value != passwordRepeatField.value) {
        document.getElementById('pw_field_error').innerHTML = "Hasła nie są identyczne!"
        return false;
    }
    document.getElementById('pw_field_error').innerHTML = ""
    return true;
}
passwordRepeatField.addEventListener('blur', validatePassword);


// var nameField = document.getElementById('name');
// var lastNameField = document.getElementById('last_name');
// var cityField = document.getElementById('city');
// var zipCodeField = document.getElementById('zip_code');
// var streetField = document.getElementById('street');
// var houseNumberField = document.getElementById('house_number');
// var flatNumberField = document.getElementById('flat_number');
