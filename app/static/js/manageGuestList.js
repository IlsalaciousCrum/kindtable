function showCurrentGuests(results) {
    "use strict";
    $(".guests").load(location.href + " #guests");
    $(".recipes").load(location.href + " #recipes");
    $(".modal.in").modal("hide");
}

$(document).ready(function() {
    "use strict";
    $('#manage_guest_list_form').on('submit', (function(event) {
        event.preventDefault();
        var url = $('#manage_guest_list_form').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#manage_guest_list_form').serialize(),
            success: showCurrentGuests
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