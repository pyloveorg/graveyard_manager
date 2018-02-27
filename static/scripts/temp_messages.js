function remove_message(div_id){
   var div_name = document.getElementById(div_id);
   div_name.parentNode.removeChild(div_name);
}

function start_counting(div_id){
   setTimeout("remove_message(div_id)", 1000);
}
