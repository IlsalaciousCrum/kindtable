function showCurrentFriendsNav(results) {
    "use strict";
    console.dir(results); // for debugging
    $(".modal.in").find('form')[0].reset();
    $("#friendsDropDown").load(location.href + " .myFriends");
    $("#ff-flashedalert").html('<div class="alert alert-success"><strong>Success!</strong> Would you like to connect with someone else?</div>');
}


$(document).ready(function() {
    "use strict";
    $('#connectForm').on('submit', (function(event) {
        event.preventDefault();
        var url = $('#connectForm').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#connectForm').serialize(),
            success: showCurrentFriendsNav
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
    $('#findFriendLink').on('click', (function (event) {
        var $this = $(this).data('target');
        $('#loadFindFriendHere').load('/profiles/findfriend' + $this, function (response, status, xhr) {
            if (status == "success") {
                $(this).modal('show');
            }
        });
    }));
});
