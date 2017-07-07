function showCurrentNotes(results) {
    "use strict";
    console.dir(results); // for debugging
    $(".modal.in").modal("hide");
    $(".recipe_notes").load(location.href + " #recipe_notes");
}

$(document).ready(function() {
    "use strict";
    $('#notesForm').on('submit', (function(event) {
        event.preventDefault();
        var url = $('#notesForm').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#notesForm').serialize(),
            success: showCurrentNotes
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

$(document).ready(function() {
    "use strict";
    $('#deletenote').on('click', (function(event) {
        var url = Flask.url_for("profiles.clearrecipenotes");
        $.ajax({
            type: "POST",
            url: url,
            data: $('#notesForm').serialize(),
            success: showCurrentNotes
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