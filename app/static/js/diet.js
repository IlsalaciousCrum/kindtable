function showCurrentDiet(results) {
    "use strict";
    console.dir(results); // for debugging
    $(".modal.in").modal("hide");
    $("#dietModal").find('form')[0].reset();
    $(".dietType").load(location.href + " #dietType");
}


$(document).ready(function() {
    "use strict";
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
