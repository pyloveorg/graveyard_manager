function validate(){
    var fields = {email: validateEmail,
                  repeat_password: validatePassword,
                  test: testowa
              }
                  // 'name', 'last_name', 'city', 'zip_code', 'street', 'house_number', 'flat_number'}
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
        else if (emailField.value == "xyz"){
            document.getElementById('email_field_error').innerHTML = "Nieprawidłowy adres e-mail!"
        }
        else {
            document.getElementById('email_field_error').innerHTML = ""
            return true;
        }
        return false;
    }
    emailField.addEventListener('blur', validateEmail);
}


// walidacja hasła
var passwordField = document.getElementById('password');
var passwordRepeatField = document.getElementById('repeat_password');
if (passwordField && passwordRepeatField){
    function validatePassword(){
        passwordField.addEventListener('blur', validatePassword);
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

// walidacja imienia
var nameField = document.getElementById('name');
if (nameField){
    // dokonczyc walidacje
}

// walidacja nazwiska
var lastNameField = document.getElementById('last_name');
if (lastNameField){
    // dokonczyc walidacje
}

// walidacja miasta
var cityField = document.getElementById('city');
if (cityField){
    // dokonczyc walidacje
}

// walidacja kodu pocztowego
var zipCodeField = document.getElementById('zip_code');
if (zipCodeField){
    // dokonczyc walidacje
}

// walidacja ulicy
var streetField = document.getElementById('street');
if (streetField){
    // dokonczyc walidacje
}

// walidacja numeru domu
var houseNumberField = document.getElementById('house_number');
if (houseNumberField){
    // dokonczyc walidacje
}

// walidacja numeru mieszkania
var flatNumberField = document.getElementById('flat_number');
if (flatNumberField){
    // dokonczyc walidacje
}

var test = document.getElementById('testowohej')
function testowa(){
    alert('funkcja testowa');
}
