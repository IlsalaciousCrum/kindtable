function showUpcomingParties(results) {
    "use strict";
    $(".upcomingParties").load(location.href + " #upcomingParties");
    $(".modal.in").modal("hide");
}

$(document).ready(function() {
    "use strict";
    $('#inviteForm').on('submit', (function(event) {
        console.log($('#inviteForm').serialize());
        event.preventDefault();
        var url = $('#inviteForm').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#inviteForm').serialize(),
            success: showUpcomingParties
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