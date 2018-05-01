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


function checkEmailInDB(inputId, errorId, keyWord, url) {
    var xhr = ajaxInit();
    var errorElement = document.getElementById(inputId)
    if (xhr != null) {
        xhr.open("POST", url, true);
        xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
        xhr.send(keyWord + "=" + errorElement.value);
        xhr.onreadystatechange = function(){
            if (xhr.readyState == 4){
                if (xhr.status == 200){
                    errorElement.innerHTML = xhr.responseText;
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
