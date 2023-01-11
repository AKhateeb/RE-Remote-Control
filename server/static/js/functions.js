$(document).ready(function () {

    socket.on('connect', function(msg){
        $("div.spinner").fadeOut(400);
        $("div.content").fadeIn(400);
        // $(".connection-status").html(":✔️ Connected").addClass('text-success').removeClass('text-danger text-primary');
    });
    
    socket.on('disconnect', function(msg){
        $("div.content").fadeOut(400);
        $("div.spinner").fadeIn(400);
        // $(".connection-status").html("❌ Disconnected").addClass('text-danger').removeClass('text-success text-primary')
    });
    
    socket.on("START", function (msg) {
        console.log("Received :START: " + msg.name);
        $(".name").html(msg.name);
    });
});