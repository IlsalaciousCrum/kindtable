$(document).ready(function() {
    "use strict";
    $('#addFriendProfileLink').on('click', (function (event) {
        var $this = $(this).data('target');
        $('#loadAddFriendProfileHere').load(Flask.url_for("profiles.add_friend_profile") + $this, function (response, status, xhr) {
            if (status == "success") {
                $(this).modal('show');
            }
        });
    }));
});