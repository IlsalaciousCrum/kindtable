function showCurrentPartyTitle(results) {
    "use strict";
    $(".modal.in").modal("hide");
    $(".partytitle").load(location.href + " #partytitle");
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
            success: showCurrentPartyTitle
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