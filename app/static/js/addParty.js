function showCurrentPartiesNav(results) {
    "use strict";
    console.dir(results); // for debugging
    $(".modal.in").find('form')[0].reset();
    $("#partiesDropDown").load(location.href + " .myParties");
    $("#ff-flashedalert").html('<div class="alert alert-success"><strong>Success!</strong> Go invite some people!</div>');
}


$(document).ready(function() {
    "use strict";
    $('#addPartyForm').on('submit', (function(event) {
        event.preventDefault();
        var url = $('#addPartyForm').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#addPartyForm').serialize(),
            success: showCurrentPartiesNav
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

// ---------


$(document).ready(function() {
    "use strict";
    $('#addPartyLink').on('click', (function (event) {
        var $this = $(this).data('target');
        $('#loadAddPartyHere').load('/profiles/connect_friends' + $this, function (response, status, xhr) {
            if (status == "success") {
                $(this).modal('show');
            }
        });
    }));
});
