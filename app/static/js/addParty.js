$(document).ready(function() {
    "use strict";
    $('#addPartyLink').on('click', (function (event) {
        var $this = $(this).data('target');
        $('#loadAddPartyHere').load(Flask.url_for("profiles.add_new_party") + $this, function (response, status, xhr) {
            if (status == "success") {
                $(this).modal('show');
            }
        });
    }));
});