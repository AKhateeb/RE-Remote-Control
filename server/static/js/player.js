
function disable_buzzer(){
    $("#btn-buzzer").addClass("disabled btn-light").removeClass("btn-success");
}

function enable_buzzer(){
    $("#btn-buzzer").removeClass("disabled btn-light").addClass("btn-success");
}

function set_code(){
    var url = new URL(window.location.href);
    var code = url.searchParams.get("code");
    $("#code").html(code? code : "*****");
}

function buzz_in(){
    let timestamp = Date.now()
    let code = parseInt($("#code").html());
    if(!code) return;
    socket.emit("BUZZ_IN", {'timestamp': timestamp, 'code': code});
    $("#btn-buzzer").addClass("disabled");
}

socket.on('ENABLE_BUZZER', function(msg){
    console.log("---------- ENABLE_BUZZER EVENT ----------");
    console.log(msg);
    enable_buzzer();
})

socket.on('DISABLE_BUZZER', function(msg){
    disable_buzzer();
})

$(document).ready(function () {
    // set_code();
});