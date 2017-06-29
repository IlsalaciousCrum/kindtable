
$(document).ready(function() {
    "use strict";
    $('#recipe_results').on('click', (function (event) {
        event.preventDefault();
        $( "#loadRecipeHere" ).empty();
        var $this = $(event.target).closest('button').data('recipeid');
        console.dir($this); // for debugging
        $('#loadRecipeHere').load('/spoonacular/see_recipe/' + $this, function (response, status, xhr) {
            if (status == "success") {
                $('#seeRecipeModal').modal('toggle');
                $('#notes_input').focus();
            }
        });
    }));
});

$(document).ready(function() {
    "use strict";
    $('#recipe_close_button').on('click', (function (event) {
    $('#seeRecipeModal').modal('toggle');
    $( "#loadRecipeHere" ).empty();
    }));
});
