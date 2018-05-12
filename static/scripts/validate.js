function validate(){
    var fields = {email: validateEmail,
                  repeat_password: validatePassword,
                  zip_code: validateZipCode
              }
    var func_return = true;
    for (i in Object.keys(fields)){
        if (document.getElementById(Object.keys(fields)[i])){
            if (fields[Object.keys(fields)[i]]() == false){
                func_return = false;
            }
        }
    }
    return func_return;
}


// walidacja e-maila
var emailField = document.getElementById('email');
if (emailField) {
    function validateEmail(){
        if (emailField.value == ""){
            document.getElementById('email_field_error').innerHTML = "Pole wymagane!"
        }
        else {
            var emailPattern = /\b[a-z0-9-_.]*@[a-z0-9-_.]*\.[a-z0-9-_.]*\b/
            if (emailPattern.test(emailField.value)){
                // do sprawdzenia preventDefault() podobno zatrzyma zwracanie undefined ;)
                if (this.id == 'email'){
                    checkEmailInDB('email', 'email', '/ajax_email');
                }
                document.getElementById('email_field_error').innerHTML = ""
                return true;
            }
            else {
                document.getElementById('email_field_error').innerHTML = "Niepoprawny adres e-mail!"
            }
        }
        document.getElementById('email_field_succes').innerHTML = ""
        return false;
    }
    emailField.addEventListener('blur', validateEmail);
}


// walidacja hasła
var passwordField = document.getElementById('password');
var passwordRepeatField = document.getElementById('repeat_password');
if (passwordField && passwordRepeatField){
    function validatePassword(){
        if (this.id == 'repeat_password'){
            passwordField.addEventListener('blur', validatePassword);
        }
        if (passwordField.value == "" || passwordRepeatField == ""){
            document.getElementById('pw_field_error').innerHTML = "Oba pola wymagane!"
            return false;
        }
        if (passwordField.value != passwordRepeatField.value){
            document.getElementById('pw_field_error').innerHTML = "Hasła nie są identyczne!"
            return false;
        }
        document.getElementById('pw_field_error').innerHTML = ""
        return true;
    }
    passwordRepeatField.addEventListener('blur', validatePassword);
}


// walidacja kodu pocztowego
var zipCodeField = document.getElementById('zip_code');
if (zipCodeField){
    function validateZipCode(){
        if (zipCodeField.value == ""){
            document.getElementById('zip_code_field_error').innerHTML = ""
            return true;
        }
        var zipCodePattern = /\b\d\d-\d\d\d\b/;
        var func_return = zipCodePattern.test(zipCodeField.value);
        if (func_return) {
            document.getElementById('zip_code_field_error').innerHTML = ""
        }
        else {
            document.getElementById('zip_code_field_error').innerHTML = "Niepoprawny kod pocztowy!"
        }
        return func_return;
    }
    zipCodeField.addEventListener('change', validateZipCode);
}
