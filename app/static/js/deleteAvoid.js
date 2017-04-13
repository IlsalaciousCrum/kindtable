function showCurrentAvoid(results) {
    "use strict";
    console.dir(results); // for debugging
    $("#avoid").load(location.href + " #avoid");
    $("#deleteAvoidForm")[0].reset();
    $(".modal.in").modal("hide");

}


$(document).ready(function() {
    "use strict";
    $('#deleteAvoidForm').on('submit', (function(event) {
        event.preventDefault();
        var url = $('#deleteAvoidForm').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#deleteAvoidForm').serialize(),
            success: showCurrentAvoid
        });
    }));

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{ deleteAvoidForm.csrf_token._value() }}");
            }
        }
    });
});