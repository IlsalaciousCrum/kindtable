"""K(i)nd app views"""

from flask import (render_template, request, flash, redirect, session, json, url_for)

from . import spoonacular

from app.models import (User, Cuisine, Course, Party,
                        PartyRecipes, RecipeCard, PartyGuest)

from flask_login import login_required, current_user
from ..decorators import email_confirmation_required

from ..functions import (guest_avoidances, guest_intolerances,
                         spoonacular_recipe_information,
                         spoonacular_request)

from .. import db

from .forms import (SaveRecipe)


@spoonacular.route('/recipe/<int:record_id>')
@login_required
@email_confirmation_required
def show_saved_recipe(record_id):
    """Show a recipe saved in the RecipeCard in it's own page, from the recipe preview, on the party page"""

    session_token = session.get("session_token")
    this_user = User.query.filter_by(session_token=session_token).first()
    this_recipe = PartyRecipes.query.get(record_id)
    ingredients = json.loads(this_recipe.recipes.ingredients)
    instructions = json.loads(this_recipe.recipes.instructions)
    party = Party.query.get(this_recipe.party_id)
    works_for = json.loads(this_recipe.works_for)

    avoid = guest_avoidances(party.party_id)
    intolerances = guest_intolerances(party.party_id)

    return render_template("profiles/saved_recipe_profile.html",
                           this_user=this_user,
                           this_recipe=this_recipe,
                           party=party,
                           avoid=avoid,
                           intolerances=intolerances,
                           ingredients=ingredients,
                           instructions=instructions,
                           works_for=works_for)


@spoonacular.route('/searchrecipes')
@login_required
@email_confirmation_required
def show_search_spoonacular():
    """Collate party information, query spoonacular and show results."""

    party_id = session.get("party_id")
    party = Party.query.get(party_id)
    get_avoid = guest_avoidances(party_id)
    get_intolerance = guest_intolerances(party_id)
    cuisine_list = Cuisine.query.order_by(Cuisine.cuisine_name).all()
    course_list = Course.query.order_by(Course.course_name).all()
    party_guests = PartyGuest.query.filter(PartyGuest.party_id == party_id).all()
    party_diets = list(set(guest.profiles.diet.diet_type for guest in party_guests))

    diets = session["diets"]
    avoids = session["avoids"]
    intols = session["intols"]
    course = session["course"]
    cuisine = session["cuisine"]

    responses = spoonacular_request(party_id=party_id, diet=diets,
                                    intols=intols, avoids=avoids,
                                    cuisine=cuisine, course=course)

    print "This is number"
    print responses.get('number', None)
    print "this is totalResults"
    print responses.get('totalResults', None)

    result_number = int(min(responses.get('number', None), responses.get('totalResults', None)))

    return render_template("spoonacular/recipe_search.html",
                           party=party,
                           responses=responses,
                           avoids=get_avoid,
                           intols=get_intolerance,
                           party_diets=party_diets,
                           cuisine_list=cuisine_list,
                           course_list=course_list,
                           party_avoids=get_avoid,
                           party_intols=get_intolerance,
                           cuisine=cuisine,
                           course=course,
                           result_number=result_number)


@spoonacular.route('/rerun_search', methods=["POST"])
@login_required
@email_confirmation_required
def rerun_search():
    """Reruns a recipe search from the recipe page."""

    cuisine = request.form.get("cuisine")
    course = request.form.get("course")
    newdiets = request.form.getlist("diets")
    newintols = request.form.getlist("intols")
    newavoids = request.form.getlist("avoids")

    session['cuisine'] = cuisine
    session['course'] = course
    session['diets'] = newdiets
    session['intols'] = newintols
    session['avoids'] = newavoids

    return redirect(url_for("spoonacular.show_search_spoonacular"))


# @spoonacular.route('/reloadsearchrecipes', methods=["POST"])
# @login_required
# @email_confirmation_required
# def show_re_search_spoonacular():
#     """Collate party information, query spoonacular and show results."""

#     session_token = session.get("session_token")
#     this_user = User.query.filter_by(session_token=session_token).first()
#     party_id = session.get("party_id")
#     party = Party.query.get(party_id)
#     cuisine = request.form.get("cuisine")
#     session["cuisine"] = cuisine
#     course = request.form.get("course")
#     session["course"] = course
#     newdiets = request.form.getlist("diets")
#     diets = []
#     for each in newdiets:
#         diets.append(str(each))
#     session["diets"] = diets
#     newintols = request.form.getlist("intols")
#     intols = []
#     for each in newintols:
#         intols.append(str(each))
#     session["intols"] = intols

#     newavoids = request.form.getlist("avoids")
#     avoids = []

#     for each in newavoids:
#         avoids.append(str(each))
#     session["avoids"] = avoids

#     new_diet = new_guest_diet(newdiets)

#     party_diets = set(guest.profiles.diet.diet_type for guest in Party.query.get(party_id))
#     responses = new_spoonacular_request(diet=new_diet, intols=intols, avoids=avoids, cuisine=cuisine, course=course)
#     # print responses
#     get_avoid = guest_avoidances(party_id).split(", ")
#     get_intolerance = guest_intolerances(party_id).split(", ")
#     # ---------------
#     cuisine_list = Cuisine.query.order_by(Cuisine.cuisine_name).all()
#     course_list = Course.query.order_by(Course.course_name).all()
#     result_number = int(min(responses.get('number', None), responses.get('totalResults', None)))

#     return render_template("spoonacular/recipe_search.html", party=party,
#                            responses=responses,
#                            this_user=this_user,
#                            party_diets=party_diets,
#                            cuisine_list=cuisine_list,
#                            course_list=course_list,
#                            party_avoids=get_avoid,
#                            party_intols=get_intolerance,
#                            avoids=avoids,
#                            intols=intols,
#                            cuisine=cuisine,
#                            course=course,
#                            newdiets=diets,
#                            result_number=result_number)


@spoonacular.route('/show_recipe/<int:record_id>')
@login_required
@email_confirmation_required
def preview_saved_recipe(record_id):
    """Show a recipe preview of recipes saved in the RecipeCard table, from the party page"""

    session_token = session.get("session_token")
    this_user = User.query.filter_by(session_token=session_token).first()
    this_recipe = RecipeCard.query.get(record_id)
    partyrecipe = PartyRecipes.query.filter(PartyRecipes.recipe_record_id == this_recipe.recipe_record_id).first()
    party = Party.query.get(this_recipe.party_id)
    works_for = json.dumps(partyrecipe.works_for_json)

    return render_template("spoonacular/recipe_preview.html",
                           this_user=this_user,
                           this_recipe=this_recipe,
                           party=party,
                           works_for=works_for)


@spoonacular.route('/see_recipe/<int:recipe_id>')
@login_required
@email_confirmation_required
def see_recipe(recipe_id):
    """Preview a recipe not yet saved, from the recipe search page"""

    print "calling spoonacular.see_recipe"

    form = SaveRecipe(request.form)
    party_id = session.get("party_id")
    avoids = session.get("avoids")
    intols = session.get("intols")
    cuisine = session.get("cuisine")
    course = session.get("course")
    newdiets = session.get("diets")
    info = spoonacular_recipe_information(recipe_id)
    ingredients = json.loads(info['ingredients_list'])
    instructions = json.loads(info['instructions_list'])

    session['info'] = info

    saved_recipe = db.session.query(PartyRecipes).join(RecipeCard).filter(RecipeCard.recipe_record_id == recipe_id, PartyRecipes.party_id == party_id).first()

    return render_template("spoonacular/view_recipe.html",
                           recipe_id=recipe_id,
                           party_id=party_id,
                           avoids=avoids,
                           intols=intols,
                           cuisine=cuisine,
                           course=course,
                           newdiets=newdiets,
                           saved_recipe=saved_recipe,
                           info=info,
                           ingredients=ingredients,
                           instructions=instructions,
                           form=form)


@spoonacular.route('/addtorecipebox', methods=['POST'])
@login_required
@email_confirmation_required
def add_recipe_box():
    """Add a recipe to the recipe box"""


    form = SaveRecipe(request.form)
    party_id = session.get("party_id")
    avoids = session.get("avoids")
    intols = session.get("intols")
    cuisine = session.get("cuisine")
    course = session.get("course")
    newdiets = session.get("diets")
    info = spoonacular_recipe_information(recipe_id)
    ingredients = json.loads(info['ingredients_list'])
    instructions = json.loads(info['instructions_list'])
    party_id = session.get("party_id")
    title = request.form.get("title")
    cuisine = session.get("cuisine")
    cuisine_object = Cuisine.query.filter(Cuisine.cuisine_name == cuisine).first()
    course = session.get("course")
    course_object = Course.query.filter(Course.course_name == course).first()

    avoids = session.get("avoids")
    intols = session.get("intols")
    diets = session.get("diets")

    works_for_dump = json.dumps({'avoids': tuple(avoids), 'diets': tuple(diets), 'intols': tuple(intols)})

    recipe_id = request.form.get("recipe_id")
    this_recipe = RecipeCard.query.filter(RecipeCard.recipe_id == recipe_id).first()
    print "recipe is below"
    print this_recipe
    if this_recipe:
        party_recipe = PartyRecipes.query.filter(PartyRecipes.recipe_record_id == recipe_id, PartyRecipes.party_id == party_id).first()
        print "partyrecipe is below"
        print party_recipe
        if party_recipe:
            flash("This recipe is already saved.", "warning")
            return redirect(url_for('spoonacular.show_search_spoonacular'))
        else:
            PartyRecipes.create_record(party_id=party_id,
                                       recipe_record_id=recipe_id,
                                       course_id=course_object.course_id,
                                       cuisine_id=cuisine_object.cuisine_id,
                                       works_for=works_for_dump)
            flash("The recipe for %s has been saved." % title, "success")
            return redirect(url_for('spoonacular.show_search_spoonacular'))
    else:
        recipe_image_url = request.form.get("recipe_image_url")
        recipe_url = request.form.get("recipe_url")

        instructions = session['instructions']
        ingredients = session['ingredients']

        new_recipe = RecipeCard.create_record(recipe_id=recipe_id,
                                              title=title,
                                              recipe_image_url=recipe_image_url,
                                              recipe_url=recipe_url,
                                              ingredients=ingredients,
                                              instructions=instructions)

        PartyRecipes.create_record(party_id=party_id,
                                   recipe_record_id=new_recipe.recipe_record_id,
                                   course_id=course_object.course_id,
                                   cuisine_id=cuisine_object.cuisine_id,
                                   works_for=works_for_dump)

        flash("The recipe for %s has been saved to your recipe box." % title, "success")
        return redirect(url_for('spoonacular.show_search_spoonacular'))
