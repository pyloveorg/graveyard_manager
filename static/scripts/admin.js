function showElement(elementId, itemFunc){
    var element = document.getElementById(elementId);
    element.style.display='block';
    itemFunc.removeEventListener('click', function(){showElement(elementId, itemFunc);});
    itemFunc.addEventListener('click', function(){hideElement(elementId, itemFunc);});
}

function hideElement(elementId, itemFunc){
    var element = document.getElementById(elementId);
    element.style.display='none';
    itemFunc.addEventListener('click', function(){showElement(elementId, itemFunc);});
    itemFunc.removeEventListener('click', function(){hideElement(elementId, itemFunc);});
}

var newPost = document.getElementById('new_post')
newPost.addEventListener('click', function(){showElement('new_post_box', newPost);})

var newEmail = document.getElementById('new_email')
newEmail.addEventListener('click', function(){showElement('new_email_box', newEmail);})

var newNecrology = document.getElementById('new_necrology')
newNecrology.addEventListener('click', function(){showElement('new_necrology_box', newNecrology);})
