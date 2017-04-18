function showCurrentEmail(results) {
    "use strict";
    console.dir(results); // for debugging
    $(".modal.in").modal("hide");
    $(".friendEmail").load(location.href + " #friendEmail");
}


$(document).ready(function() {
    "use strict";
    $('#emailForm').on('submit', (function(event) {
        event.preventDefault();
        var url = $('#emailForm').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#emailForm').serialize(),
            success: showCurrentEmail
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
