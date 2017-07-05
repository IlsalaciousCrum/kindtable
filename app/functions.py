# # from sqlalchemy import func

from app.models import (db, Diet, Cuisine, Course, Party, PartyGuest)

# from server import app

import itertools

import requests
import os
import simplejson as json
from flask import url_for


def guest_diet(party_id):
    """Query that gets the diet of each guest coming to the party and figures out the most limiting"""

    most_limiting = min(guest.profiles.diet.ranking for guest in Party.query.get(party_id))
    diet_string = Diet.query.filter_by(ranking=most_limiting).first()
    return str(diet_string.diet_type)


def new_guest_diet(diets):
    """Query that takes the diets from the form and determines the most limiting"""

    if diets:
        diet_ranking = []
        for each_diet in diets:
            this_diet = db.session.query(Diet).filter(Diet.diet_type == each_diet).first()
            this_diet_rank = this_diet.ranking
            diet_ranking.append(this_diet_rank)

        most_limiting = min(diet_ranking)
    else:
        most_limiting = 10

    diet_string = Diet.query.filter_by(ranking=most_limiting).first()

    return str(diet_string.diet_type)


def guest_avoidances(party_id):
    """Query that gets the avoidances of each guest coming to the party"""

    party_guests = PartyGuest.query.filter(PartyGuest.party_id == party_id).all()

    _a_list = [[avoid.ingredient for avoid in guest.profiles.avoidances] for guest in party_guests]
    a_list = list(itertools.chain.from_iterable(_a_list))
    a_set = set()
    a_set.update(a_list)

    return list(a_set)


def guest_intolerances(party_id):
    """Query that gets the avoidances of each guest coming to the party"""

    party_guests = PartyGuest.query.filter(PartyGuest.party_id == party_id).all()

    _i_list = [[intol.intol_name for intol in guest.profiles.intolerances] for guest in party_guests]
    i_list = list(itertools.chain.from_iterable(_i_list))
    i_set = set()
    i_set.update(i_list)

    return list(i_set)


def spoonacular_request(diet, intols, avoids, cuisine, course, offset):
    """Assembles a new API request with new variables, to Spoonacular"""

    avoid_string = ', '.join(avoids)
    intolerance_string = ', '.join(intols)
    diet = new_guest_diet(diet)
    cuisine = Cuisine.query.get(cuisine)
    cuisine = str(cuisine.cuisine_name)
    if cuisine == "any":
        cuisine = ""

    course = Course.query.get(course)
    course = str(course.course_name)

    url = 'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search'
    headers = {"X-Mashape-Key": os.environ['SECRET_KEY'], "Accept": "application/json"}
    payload = {'cuisine': cuisine, 'diet': str(diet), 'excludeIngredients': str(avoid_string),
               'instructionsRequired': 'false', 'intolerances': str(intolerance_string),
               'limitLicense': 'false', 'number': 100, 'offset': offset, 'query': 'recipe',
               'type': course}

    print "This is the payload"
    print payload

    response = requests.get(url, headers=headers, params=payload)

    responses = {}

    spoon = response.json()

    print "the response is below this one"
    print spoon

    responses["number"] = spoon['number']
    responses["totalResults"] = spoon['totalResults']

    number = min(spoon['number'], spoon['totalResults'])

    image_base = spoon.get('baseUri')
    recipe_base = "https://spoonacular.com/recipes/"
    responses['response'] = []

    for i in range(number):
        recipe_id = spoon['results'][i].get('id')
        try:
            _image_url = spoon['results'][i]['imageUrls'][0]
            image_url = image_base + _image_url
        except:
            image_url = url_for('static', filename='knife_fork.png')
        title = spoon['results'][i].get('title')
        recipe_url = recipe_base + image_url[:-4]
        print recipe_url
        response = {"title": title, "recipe_url": recipe_url, "image_url": image_url, "recipe_id": recipe_id}
        responses['response'].append(response)

    return responses

    # TODO, use: cleaned = bleach.clean(html, tags=[], attributes={}, styles=[], strip=True)
    # where html is the text you want any html tags or script tags removed.


def spoonacular_recipe_information(recipe_id):
    """Assembles an API request to Spoonacular to get recipe information"""

    url = 'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/%s/information' % str(recipe_id)

    headers = {"X-Mashape-Key": os.environ['SECRET_KEY']}
    payload = {'id': recipe_id, 'includeNutrition': False}
    response = requests.get(url, headers=headers, params=payload)

    spoon = response.json()
    print spoon

    title = spoon["title"]
    image = spoon["image"]
    spoonacular_url = spoon["spoonacularSourceUrl"]
    sourceUrl = spoon["sourceUrl"]
    _id = spoon["id"]

    ingredients_list = json.dumps(((each["originalString"]) for each in spoon['extendedIngredients']), iterable_as_array=True)
    print ingredients_list

    if len(spoon['analyzedInstructions']) == 0:
        instructions = json.dumps("Instructions located at the 'Original Recipe Source' link below")
    else:
        instructions_list = []
        for each in spoon['analyzedInstructions']:
            for step in each['steps']:
                instructions_list.append(step['step'])

        instructions = json.dumps(instructions_list)

    return {'title': title, 'image_url': image, 'source_url': sourceUrl,
            'spoonacular_url': spoonacular_url, 'ingredients_list': ingredients_list,
            'instructions_list': instructions, 'recipe_id': _id}
