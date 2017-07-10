function showCurrentDate(results) {
    "use strict";
    var answer = results;
    $(".modal.in").modal("hide");
    $(".dtm-dtm").html(answer);
}

$(document).ready(function() {
    "use strict";
    $('#party_datetime').on('submit', (function(event) {
        event.preventDefault();
        var url = $('#party_datetime').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#party_datetime').serialize(),
            success: showCurrentDate
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