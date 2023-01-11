function submit_code(player_index, code, name) {
    $.ajax({
        type: "POST",
        url: "/submit_code",
        data: JSON.stringify({ code: code, player: player_index, name: name }),
        headers: { 'Content-Type': 'application/json' },
        success: function (response) {
            // to make sure the code has successfully reached the server
            $("#btn-generate-" + player_index).toggleClass('disabled', false);
        }
    });
}

function generate_code(player_index) {
    let code = Math.floor(Math.random() * 99999);
    let name = $("#player-name-"+player_index).val().trim();
    $("#code-" + player_index).html(code);
    $("#btn-generate-" + player_index).toggleClass('disabled', true);
    submit_code(player_index, code, name);
}

function copy_link(player_index) {
    let code = $("#code-" + player_index).html();
    let link = location.origin + "/player?code=" + code
    console.log(link);
    // navigator.clipboard.writeText(link);

    alertify.success('Link is copied for player' + player_index);
}

function enable_buzzer() {
    socket.emit("ENABLE_BUZZER", function (msg) {
        $("#buzzer-status").html("ON").addClass('bg-success').removeClass('bg-secondary');
        $("#btn-enable-buzzer").addClass("disabled");
        $("#btn-disable-buzzer").removeClass("disabled");
    })
}

function disable_buzzer() {
    socket.emit("DISABLE_BUZZER", function (msg) {
        $("#buzzer-status").html("OFF").addClass('bg-secondary').removeClass('bg-success');
        $("#btn-disable-buzzer").addClass("disabled", "");
        $("#btn-enable-buzzer").removeClass("disabled");
    })
    socket.emit("BUZZER_RESULTS");
}

socket.on("PLAYERS_ORDER", function (data) {
    $("#players-container").empty();
    data.forEach(player => {
        let content = `
        <div>
            <h1 class="p-3 m-2 player-item animate__animated border border-primary rounded animate__bounceInLeft animate__delay-${2*player['ix']}s">
                <span class="mx-5 fs-1 p-2 badge bg-success">${player['ix']}</span>
                <strong>${player['name']}</strong>
            </h1>
        </div>`;
        $("#players-container").append(content);
    });
});

$(document).ready(function () {

});