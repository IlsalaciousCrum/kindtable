if($("#timezone") !== null){
    $(document).ready(function() {
        'use strict';
        var timezone = (Intl.DateTimeFormat().resolvedOptions().timeZone);
        $("#timezone").val(timezone);
    });
}