function ajaxInit(){
    var xhr = null;
    try {
        xhr = new XMLHttpRequest();
    }
    catch {
        try {
            xhr = new ActiveXObject('Msxm12.XMLHttp');
        }
        catch {
            try {
                xhr = new ActiveXObject('Microsoft.XMLHTTP');
            }
            catch(e) {
                alert('Niestety twoja przeglądarka nie obsługuje AJAXa');
            }
        }
    }
    return xhr;
}

function checkEmailInDB(inputId, keyWord, url) {
    var xhr = ajaxInit();
    var inputElement = document.getElementById(inputId)
    if (xhr != null) {
        xhr.open("POST", url, true);
        xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
        xhr.send(keyWord + "=" + inputElement.value);
        xhr.onreadystatechange = function(){
            if (xhr.readyState == 4){
                if (xhr.status == 200){
                    if (xhr.responseText == 'none'){
                        // fragment na roboczo
                        document.getElementById('email_field_succes').innerHTML = "Adres e-mail jest wolny!"
                        document.getElementById('email_field_error').innerHTML = ""
                    }
                    else {
                        document.getElementById('email_field_succes').innerHTML = ""
                        document.getElementById('email_field_error').innerHTML = "Adres e-mail jest zajęty!"
                        // koniec fragmentu roboczego
                    }
                }
                else {
                    alert('Przepraszamy, wystąpił błąd ' + xhr.status)
                }
            }
            else {
                // TODO dodać gifa - wczytywanie
            }
        }
    }
}
