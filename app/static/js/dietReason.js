function showCurrentDietReason(results) {
    console.dir(results); // for debugging
    $(".modal.in").modal("hide");
    $("#dietReason").load(location.href + " #dietReason");
}


$(document).ready(function() {
    $('#changeDietReason').on('submit', (function(event) {
        event.preventDefault();
        var url = $('#changeDietReason').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#changeDietReason').serialize(),
            success: showCurrentDietReason
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
