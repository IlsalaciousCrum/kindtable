function showCurrentIntolsRegister(results) {
    "use strict";
    $("#intol-success").css('display', 'inline');
    $("#intol-success").fadeOut(2500, (function(){
        $('#intol-success').css('display', 'none');
    }));
    $(".modal.in").modal("hide");
}

$(document).ready(function() {
    "use strict";
    $('#intolsForm').on('submit', (function(event) {
        event.preventDefault();
        var url = $('#intolsForm').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#intolsForm').serialize(),
            success: showCurrentIntolsRegister
        });
    }));

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}");
            }
        }
    });
});