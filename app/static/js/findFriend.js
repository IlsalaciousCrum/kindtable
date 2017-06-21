

$(document).ready(function() {
    "use strict";
    $('#findFriendLink').on('click', (function (event) {
        var $this = $(this).data('target');
        $('#loadFindFriendHere').load('/profiles/connect_friends' + $this, function (response, status, xhr) {
            if (status == "success") {
                $(this).modal('show');
            }
        });
    }));
});
