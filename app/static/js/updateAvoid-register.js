$(document).ready(function() {
    "use strict";
    $('#updateAvoidModal').on('show.bs.modal', (function(event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var avoid_key = button.data('key'); // Extract info from data-* attributes
        var avoid_value = button.data('value'); // Extract info from data-* attributes
        $('textarea[name="update_avoid_key"]').val(avoid_key);
        $('textarea[name="update_avoid_value"]').val(avoid_value);
        $('input[name="original_key"]').val(avoid_key);
        $(".updateAvoidModal").modal("show");
    }));
});

function showCurrentAvoids(results) {
    "use strict";
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
    $(".avoids").load(location.href + " #avoids");
    $(".modal.in").modal("hide");
}

$(document).ready(function() {
    "use strict";
    $('#deleteavoid').on('click', (function(event) {
        var url = Flask.url_for("auth.delete_stored_ingredient");
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
    $(".avoids").load(location.href + " #avoids");
    $(".modal.in").modal("hide");
}

$(document).ready(function() {
    "use strict";
    $('#deleteavoidreason').on('click', (function(event) {
        var url = Flask.url_for("auth.delete_stored_reason");
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

