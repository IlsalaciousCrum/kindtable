function showUpcomingParties(results) {
    "use strict";
    console.dir(results); // for debugging
    $(".upcoming_parties").load(location.href + " #upcoming_parties");
    $(".modal.in").modal("hide");
}

$(document).ready(function() {
    "use strict";
    $('#inviteForm').on('submit', (function(event) {
        event.preventDefault();
        var url = $('#inviteForm').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#inviteForm').serialize(),
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