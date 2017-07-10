function showCurrentTitle(results) {
    "use strict";
    console.dir(results); // for debugging
    $(".modal.in").modal("hide");
    $(".name").load(location.href + " #name");
    $(".headerName").load(location.href + " #headerName");
}

$(document).ready(function() {
    "use strict";
    $('#changeTitle').on('submit', (function(event) {
        event.preventDefault();
        var url = $('#changeTitle').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#changeTitle').serialize(),
            success: showCurrentTitle
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