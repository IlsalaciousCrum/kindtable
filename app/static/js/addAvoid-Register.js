function showCurrentAvoidRegister(results) {
    "use strict";
    $(".avoids").load(location.href + " #avoids");
    $(".avoids").show();
    $(".modal.in").find('form')[0].reset();
    $("#flashed_alert").css('display', 'inline');
     $("#avoid-success").css('display', 'inline');
    $("#avoid-success").fadeOut(4000, (function(){
        $('#avoid-success').css('display', 'none');
    }));
}

$(document).ready(function() {
    "use strict";
    $('#addAvoidForm').on('submit', (function(event) {
        event.preventDefault();
        var url = $('#addAvoidForm').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#addAvoidForm').serialize(),
            success: showCurrentAvoidRegister
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