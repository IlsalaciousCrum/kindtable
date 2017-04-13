function showCurrentAvoids(results) {
    "use strict";
    console.dir(results); // for debugging
    $(".avoids").load(location.href + " #avoids");
    $(".modal.in").find('form')[0].reset();
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
            success: showCurrentAvoids
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