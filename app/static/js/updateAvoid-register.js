$(document).ready(function() {
    "use strict";
    $('#updateAvoidRegisterModal').on('show.bs.modal', (function(event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var avoid_key = button.data('key'); // Extract info from data-* attributes
        console.log(avoid_key);
        var avoid_value = button.data('value'); // Extract info from data-* attributes
        $('input[name="update_avoid_key"]').val(avoid_key);
        $('textarea[name="update_avoid_value"]').val(avoid_value);
        $('input[name="original_key"]').val(avoid_key);
        $(".updateAvoidRegisterModal").modal("show");
    }));
});

function showCurrentAvoidsRegister(results) {
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
            success: showCurrentAvoidsRegister
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
    $('#deleteavoidreg').on('click', (function(event) {
        var url = Flask.url_for("auth.delete_stored_ingredient");
        console.log(url);
        $.ajax({
            type: "POST",
            url: url,
            data: $('#updateAvoidForm').serialize(),
            success: showCurrentAvoidsRegister
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
    $('#deleteavoidreasonreg').on('click', (function(event) {
        var url = Flask.url_for("auth.delete_stored_reason");
        console.log(url);
        $.ajax({
            type: "POST",
            url: url,
            data: $('#updateAvoidForm').serialize(),
            success: showCurrentAvoidsRegister
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

