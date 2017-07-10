function showCurrentIntols(results) {
    "use strict";
    $(".intols").load(location.href + " #intols");
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
            success: showCurrentIntols
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