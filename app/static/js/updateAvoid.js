$(document).ready(function() {
    "use strict";
    $('#updateAvoidModal').on('show.bs.modal', (function(event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var avoid_id = button.data('whatever'); // Extract info from data-* attributes
        var modal = $(this);
        $('#updateAvoidFormAvoidId').val(avoid_id);

        function replaceAvoidFormValues(results) {
            console.dir(results);
            $("#update_avoid_ingredient").val(results.data.ingredient);
            $("#update_avoid_reason").val(results.data.reason);
        }

        $.get(Flask.url_for("profiles.getavoid"), {id: avoid_id}, replaceAvoidFormValues);
    }));
});

function showCurrentAvoids(results) {
    "use strict";
    console.dir(results); // for debugging
    $(".avoids").load(location.href + " #avoids");
    $(".modal.in").modal("hide");
}

$(document).ready(function() {
    "use strict";
    $('#updateAvoidForm').on('submit', (function(event) {
        event.preventDefault();
        var url = $('#updateAvoidForm').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#updateAvoidForm').serialize(),
            success: showCurrentAvoids
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

function showCurrentAvoids(results) {
    "use strict";
    console.dir(results); // for debugging
    $(".avoids").load(location.href + " #avoids");
    $(".modal.in").modal("hide");
}

$(document).ready(function() {
    "use strict";
    $('#deleteavoid').on('click', (function(event) {
        var url = Flask.url_for("profiles.deleteavoid");
        $.ajax({
            type: "POST",
            url: url,
            data: $('#updateAvoidForm').serialize(),
            success: showCurrentAvoids
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

function showCurrentAvoids(results) {
    "use strict";
    console.dir(results); // for debugging
    $(".avoids").load(location.href + " #avoids");
    $(".modal.in").modal("hide");
}

$(document).ready(function() {
    "use strict";
    $('#deleteavoidreason').on('click', (function(event) {
        var url = "/profiles/deleteavoidreason.json";
        $.ajax({
            type: "POST",
            url: url,
            data: $('#updateAvoidForm').serialize(),
            success: showCurrentAvoids
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
