function showCurrentDiet(results) {
    console.dir(results); // for debugging
    $(".modal.in").modal("hide");
    $("#diet").load(location.href + " #diet");
}


$(document).ready(function() {
    $('#changeDiet').on('submit', (function(event) {
        event.preventDefault();
        var url = $('#changeDiet').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#changeDiet').serialize(),
            success: showCurrentDiet
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
