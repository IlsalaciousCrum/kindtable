$(document).ready(function() {
    "use strict";
    $('.recipe_results').on('click', (function (event) {
        event.preventDefault();
        $( "#loadRecipeHere" ).empty();
        var $this = $(event.target).data('recipeid');
        console.dir($this); // for debugging
        $('#loadRecipeHere').load(Flask.url_for("spoonacular.see_recipe", {'recipe_id': $this}), function (response, status, xhr) {
            if (status == "success") {
                $('#seeRecipeModal').modal('toggle');
                $('#notes_input').focus();
            }
        });
    }));
});

$(document).ready(function() {
    "use strict";
    $('.printButton').click(function(){
         $("#recipePrintWindow").print();
    });
});