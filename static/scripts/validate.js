function validate1(){
    return false;
}

function validate(){
    if (this.id == 'email'){
        if (this.value == ""){
            document.getElementById('email_field_error').innerHTML = "Pole wymagane!"
        }
        else if (this.value == "xyz"){
            document.getElementById('email_field_error').innerHTML = "Nieprawidłowy e-mail!"
        }
        else {
            document.getElementById('email_field_error').innerHTML = ""
        }
    }
}

var emailField = document.getElementById('email');
emailField.addEventListener('blur', validate);

// var passwordField = document.getElementById('password');
// var passwordRepeatField = document.getElementById('repeat_password');
// var nameField = document.getElementById('name');
// var lastNameField = document.getElementById('last_name');
// var cityField = document.getElementById('city');
// var zipCodeField = document.getElementById('zip_code');
// var streetField = document.getElementById('street');
// var houseNumberField = document.getElementById('house_number');
// var flatNumberField = document.getElementById('flat_number');
