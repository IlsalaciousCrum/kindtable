/*  TODO: "[Deprecation] Synchronous XMLHttpRequest on the main thread is deprecated 
  because of its detrimental effects to the end user's experience."
  shows up in the console but without loading this script in with the recipe
  search modal, the form just submits instead of using the ajax route. */

function showSuccessPreviewRecipe(results) {
    "use strict";
    $('#seeRecipeModal').modal('hide');
    var party_title = $("#party_title").html();
    $("#alert-recipe-party-title").html(party_title);
    var recipe_title = $("#recipe_title").html();
    $("#alert-recipe-title").html(recipe_title);
    $("#add-success").css('display', 'inline');
    $("#add-success").fadeOut(4000, (function(){
    $('#add-success').css('display', 'none');
    $(".modal-backdrop fade in").remove();
}));
}

$(document).ready(function() {
    "use strict";
    $('#saveRecipeButton').on('click', (function(event) {
        event.preventDefault();
        var url = $('#saveform').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#saveform').serialize(),
            success: showSuccessPreviewRecipe
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