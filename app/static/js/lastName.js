function showCurrentLastName(results) {
    "use strict";
    $(".modal.in").modal("hide");
    $(".last").load(location.href + " #last");
}

$(document).ready(function() {
    "use strict";
    $('#changeLastName').on('submit', (function(event) {
        event.preventDefault();
        var url = $('#changeLastName').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#changeLastName').serialize(),
            success: showCurrentLastName
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