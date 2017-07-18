function showCurrentFriendEmail(results) {
    "use strict";
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
            success: showCurrentFriendEmail
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