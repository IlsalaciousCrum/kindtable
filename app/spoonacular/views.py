"""K(i)nd app views"""

from flask import (render_template, request, flash, redirect, session, json, url_for, jsonify)

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


@spoonacular.route('/show_recipe/<int:record_id>')
@login_required
@email_confirmation_required
def preview_saved_recipe(record_id):
    """Show a recipe preview of recipes saved in the RecipeCard table, from the party page"""

    session_token = session.get("session_token")
    this_user = current_user
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

    saveform = SaveRecipe(request.form)

    newdiets = session["diets"]
    party_id = session["party_id"]
    avoids = session["avoids"]
    intols = session["intols"]
    cuisine_id = session["cuisine"]
    course_id = session["course"]

    party = Party.query.get(party_id)
    title = party.title

    course_query = Course.query.get(course_id)
    course = course_query.course_name
    cuisine_query = Cuisine.query.get(cuisine_id)
    cuisine = cuisine_query.cuisine_name

    existing_recipe = RecipeCard.query.filter(RecipeCard.recipe_id == str(recipe_id)).first()
    if existing_recipe:
        print "This is loading from an existing recipe"
        info = {'title': existing_recipe.title, 'image_url': existing_recipe.recipe_image_url, 'source_url': existing_recipe.source_recipe_url,
                'spoonacular_url': existing_recipe.spoonacular_recipe_url, 'recipe_id': recipe_id}
        ingredients = json.loads(existing_recipe.ingredients)
        instructions = json.loads(existing_recipe.instructions)

    else:
        print "this is making the spoonacular call again"
        info = spoonacular_recipe_information(recipe_id)
        ingredients = json.loads(info['ingredients_list'])
        print ingredients
        instructions = json.loads(info['instructions_list'])

    session['info'] = info
    saved_recipe = db.session.query(PartyRecipes).join(RecipeCard).filter(RecipeCard.recipe_id == str(recipe_id), PartyRecipes.party_id == str(party_id)).first()

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
                           saveform=saveform,
                           title=title)


@spoonacular.route('/addtorecipebox', methods=['POST'])
@login_required
@email_confirmation_required
def add_recipe_box():
    """Add a recipe to the recipe box"""

    saveform = SaveRecipe(request.form)

    if request.method == 'POST' and saveform.validate():
        party_id = session["party_id"]
        avoids = session["avoids"]
        intols = session["intols"]
        cuisine = session["cuisine"]
        course = session["course"]
        diets = session["diets"]
        party_id = session["party_id"]

        recipe_id = saveform.recipe_id.data
        notes = saveform.notes.data

        works_for_dump = json.dumps({'avoids': tuple(avoids), 'diets': tuple(diets), 'intols': tuple(intols)})

        recipe_exists = RecipeCard.query.filter(RecipeCard.recipe_id == recipe_id).first()
        if recipe_exists:
            saved_recipe_card_id = recipe_exists.recipe_record_id
            title = recipe_exists.title
        else:
            info = session["info"]
            title = info["title"]
            image_url = info["image_url"]
            spoonacular = info["spoonacular_url"]
            source_url = info["source_url"]
            ingredients = info["ingredients_list"]
            instructions = info["instructions_list"]

            new_recipe = RecipeCard.create_record(recipe_id=recipe_id,
                                                  title=title,
                                                  recipe_image_url=image_url,
                                                  spoonacular_recipe_url=spoonacular,
                                                  source_recipe_url=source_url,
                                                  ingredients=ingredients,
                                                  instructions=instructions)

            saved_recipe_card_id = new_recipe.recipe_record_id

        PartyRecipes.create_record(party_id=party_id,
                                   recipe_record_id=saved_recipe_card_id,
                                   course_id=course,
                                   cuisine_id=cuisine,
                                   recipe_notes=notes,
                                   works_for=works_for_dump)
        return jsonify(data={'message': 'Recipe saved'})
    else:
        for field, error in saveform.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(saveform, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)

