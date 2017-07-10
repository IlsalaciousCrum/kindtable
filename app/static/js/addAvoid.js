function showCurrentAvoid(results) {
    "use strict";
    $(".avoids").load(location.href + " #avoids");
    $(".modal.in").find('form')[0].reset();
    $("#flashedalert").html('<div class="alert alert-success"><strong>Success!</strong> Would you like to add another ingredient?</div>');
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
            success: showCurrentAvoid
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