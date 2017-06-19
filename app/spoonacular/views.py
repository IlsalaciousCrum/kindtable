"""K(i)nd app views"""

from flask import (render_template, request, flash, redirect, session, json, url_for)

from . import spoonacular

from app.models import (User, Cuisine, Course, Party,
                        PartyRecipes, RecipeCard, RecipeWorksFor)

from flask_login import login_required, current_user
from ..decorators import email_confirmation_required

from functions import (all_guest_diets, guest_avoidances,
                       guest_intolerances, new_spoonacular_request,
                       new_guest_diet, spoonacular_recipe_ingredients,
                       spoonacular_recipe_instructions, spoonacular_request)


@spoonacular.route('/searchrecipes')
@login_required
@email_confirmation_required
def show_search_spoonacular():
    """Collate party information, query spoonacular and show results."""

    session_token = session.get("session_token")
    this_user = User.query.filter_by(session_token=session_token).first()
    party_id = session.get("party_id")
    party = Party.query.get(party_id)
    responses = spoonacular_request(party_id)
    get_avoid = (guest_avoidances(party_id)).split(", ")
    get_intolerance = (guest_intolerances(party_id)).split(", ")
    cuisine_list = Cuisine.query.order_by(Cuisine.cuisine_name).all()
    course_list = Course.query.order_by(Course.course_name).all()
    party_diets = (all_guest_diets(party_id)).split(", ")
    session["diets"] = party_diets
    session["intols"] = get_intolerance
    session["avoids"] = get_avoid
    session["course"] = "any"
    session["cuisine"] = "any"

    print "This is number"
    print responses.get('number', None)
    print "this is totalResults"
    print responses.get('totalResults', None)

    result_number = int(min(responses.get('number', None), responses.get('totalResults', None)))

    return render_template("spoonacular/recipe_search.html", party=party,
                           responses=responses,
                           avoids=get_avoid,
                           intols=get_intolerance,
                           this_user=this_user,
                           party_diets=party_diets,
                           cuisine_list=cuisine_list,
                           course_list=course_list,
                           party_avoids=get_avoid,
                           party_intols=get_intolerance,
                           cuisine=25,
                           course=1,
                           newdiets=party_diets,
                           result_number=result_number)


@spoonacular.route('/reloadsearchrecipes', methods=["POST"])
@login_required
@email_confirmation_required
def show_re_search_spoonacular():
    """Collate party information, query spoonacular and show results."""

    session_token = session.get("session_token")
    this_user = User.query.filter_by(session_token=session_token).first()
    party_id = session.get("party_id")
    party = Party.query.get(party_id)
    cuisine = request.form.get("cuisine")
    session["cuisine"] = cuisine
    course = request.form.get("course")
    session["course"] = course
    newdiets = request.form.getlist("diets")
    diets = []
    for each in newdiets:
        diets.append(str(each))
    session["diets"] = diets
    newintols = request.form.getlist("intols")
    intols = []
    for each in newintols:
        intols.append(str(each))
    session["intols"] = intols

    newavoids = request.form.getlist("avoids")
    avoids = []

    for each in newavoids:
        avoids.append(str(each))
    session["avoids"] = avoids

    new_diet = new_guest_diet(newdiets)

    party_diets = (all_guest_diets(party_id)).split(", ")
    responses = new_spoonacular_request(diet=new_diet, intols=intols, avoids=avoids, cuisine=cuisine, course=course)
    # print responses
    get_avoid = guest_avoidances(party_id).split(", ")
    get_intolerance = guest_intolerances(party_id).split(", ")
    # ---------------
    cuisine_list = Cuisine.query.order_by(Cuisine.cuisine_name).all()
    course_list = Course.query.order_by(Course.course_name).all()
    result_number = int(min(responses.get('number', None), responses.get('totalResults', None)))

    return render_template("spoonacular/recipe_search.html", party=party,
                           responses=responses,
                           this_user=this_user,
                           party_diets=party_diets,
                           cuisine_list=cuisine_list,
                           course_list=course_list,
                           party_avoids=get_avoid,
                           party_intols=get_intolerance,
                           avoids=avoids,
                           intols=intols,
                           cuisine=cuisine,
                           course=course,
                           newdiets=diets,
                           result_number=result_number)


@spoonacular.route('/show_recipe/<int:record_id>')
@login_required
@email_confirmation_required
def preview_saved_recipe(record_id):
    """Show a recipe preview of recipes saved in the RecipeCard table, from the party page"""

    session_token = session.get("session_token")
    this_user = User.query.filter_by(session_token=session_token).first()
    this_recipe = RecipeCard.query.get(record_id)
    recipe_id = this_recipe.recipe_id
    works_for = json.loads(this_recipe.works_for)
    ingredients = spoonacular_recipe_ingredients(recipe_id)
    instructions = spoonacular_recipe_instructions(recipe_id)
    party = Party.query.get(this_recipe.party_id)

    avoid = guest_avoidances(party.party_id)
    intolerances = guest_intolerances(party.party_id)

    return render_template("spoonacular/recipe_preview.html",
                           this_user=this_user,
                           this_recipe=this_recipe,
                           party=party,
                           avoid=avoid,
                           intolerances=intolerances,
                           works_for=works_for,
                           ingredients=ingredients,
                           instructions=instructions)


@spoonacular.route('/recipe/<int:record_id>')
@login_required
@email_confirmation_required
def show_saved_recipe(record_id):
    """Show a recipe saved in the RecipeCard in it's own page, from the recipe preview, on the party page"""

    session_token = session.get("session_token")
    this_user = User.query.filter_by(session_token=session_token).first()
    this_recipe = RecipeCard.query.get(record_id)
    recipe_id = this_recipe.recipe_id
    works_for = json.loads(this_recipe.works_for)
    ingredients = spoonacular_recipe_ingredients(recipe_id)
    instructions = spoonacular_recipe_instructions(recipe_id)
    party = Party.query.get(this_recipe.party_id)

    avoid = guest_avoidances(party.party_id)
    intolerances = guest_intolerances(party.party_id)
    return render_template("spoonacular/recipe_profile.html",
                           this_user=this_user,
                           this_recipe=this_recipe,
                           party=party,
                           avoid=avoid,
                           intolerances=intolerances,
                           works_for=works_for,
                           ingredients=ingredients,
                           instructions=instructions)


@spoonacular.route('/see_recipe', methods=['POST'])
@login_required
@email_confirmation_required
def show_recipe():
    """Preview a recipe not yet saved, from the recipe search page"""

    if request.method == 'POST':
        session_token = session.get("session_token")
        this_user = User.query.filter_by(session_token=session_token).first()
        party_id = session.get("party_id")
        recipe_id = request.form.get("recipe_id")
        avoids = session.get("avoids")
        intols = session.get("intols")
        cuisine = request.form.get("cuisine")
        course = request.form.get("course")
        newdiets = session.get("diets")
        title = request.form.get("title")
        recipe_image_url = request.form.get("recipe_image_url")
        recipe_url = request.form.get("recipe_url")
        ingredients = spoonacular_recipe_ingredients(recipe_id)
        instructions = spoonacular_recipe_instructions(recipe_id)

        return render_template("spoonacular/view_recipe.html",
                               recipe_id=recipe_id,
                               party_id=party_id,
                               title=title,
                               recipe_image_url=recipe_image_url,
                               recipe_url=recipe_url,
                               this_user=this_user,
                               ingredients=ingredients,
                               instructions=instructions,
                               avoids=avoids,
                               intols=intols,
                               cuisine=cuisine,
                               course=course,
                               newdiets=newdiets)
    else:
        return redirect(request.referrer)

#  I think 'Get Recipe Information' API call would take it from two requests down to one


@spoonacular.route('/addtorecipebox', methods=['POST'])
@login_required
@email_confirmation_required
def add_recipe_box():
    """Add a recipe to the recipe box"""

    party_id = session.get("party_id")
    title = request.form.get("title")
    cuisine = session.get("cuisine")
    cuisine_object = Cuisine.query.filter_by(cuisine_name=cuisine).first()
    course = session.get("course")
    course_object = Course.query.filter_by(course_name=course).first()

    # Creates the -workfor- json

    avoids = session.get("avoids")
    intols = session.get("intols")
    diets = session.get("diets")

    party = Party.query.filter_by(party_id=party_id).first()

    recipe_id = request.form.get("recipe_id")
    this_recipe = RecipeCard.query.filter(recipe_id == recipe_id).first()
    if this_recipe:
        party_recipe = PartyRecipes.query.filter(recipe_id == recipe_id, party_id == party_id).first()
        if party_recipe:
            flash("This recipe is already saved.", "warning")
            return redirect(request.referrer)
        else:
            PartyRecipes.create_record(party_id=party_id,
                                       recipe_record_id=recipe_id,
                                       course_id=course_object.course_id,
                                       cuisine_id=cuisine_object.cuisine_id)
            flash("The recipe for %s has been saved." % title, "success")
            return redirect(url_for('spoonacular.show_search_spoonacular'))
    else:
        recipe_image_url = request.form.get("recipe_image_url")
        recipe_url = request.form.get("recipe_url")

        instruction_list = request.form.get("instructions")
        ingredient_list = request.form.get("ingredients")

        print instruction_list
        print ingredient_list

        ingredient_dump = (json.dumps(ingredient_list))
        instruction_dump = (json.dumps(instruction_list))

        new_recipe = RecipeCard.create_record(recipe_id=recipe_id,
                                              title=title,
                                              recipe_image_url=recipe_image_url,
                                              recipe_url=recipe_url,
                                              ingredients=ingredient_dump,
                                              instructions=instruction_dump)

        PartyRecipes.create_record(party_id=party_id,
                                   recipe_record_id=new_recipe.recipe_record_id,
                                   course_id=course_object.course_id,
                                   cuisine_id=cuisine_object.cuisine_id)

        for guest in party.guest_profiles:
            if guest.diet.diet_type in diets and guest.avoidances in avoids and guest.intolerances in intols:
                RecipeWorksFor.create_record(recipe_card_id=party_id,
                                             guest_profile_id=guest.profile_id)

        flash("The recipe for %s has been saved to your recipe box." % title, "success")
        return redirect(url_for('spoonacular.show_search_spoonacular'))
