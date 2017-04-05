function showCurrentAvoid(results) {
    console.dir(results); // for debugging
    $("#avoid").load(location.href + " #avoid");
    $(".modal.in").modal("hide");
}


$(document).ready(function() {
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
