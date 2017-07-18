function showEmailMenuSuccess(results) {
    "use strict";
    $("#emailSuccess").css('display', 'inline');
    $("#emailSuccess").fadeOut(6000, (function(){
    $('#emailSuccess').css('display', 'none');
    }));
}

$(document).ready(function() {
    "use strict";
    $('#emailMenuForm').on('submit', (function(event) {
        event.preventDefault();
        var url = $('#emailMenuForm').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#emailMenuForm').serialize(),
            success: showEmailMenuSuccess
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