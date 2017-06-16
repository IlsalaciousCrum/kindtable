# # from sqlalchemy import func

from app.models import (db, Diet, Cuisine, Course, Party)

# from server import app


import requests
import os


def all_guest_diets(partyid):
    """Query that gets the diet of each guest coming to the party"""

    diet_set = set()
    party = Party.query.get(partyid)
    party_guests = party.guests

    for guest in party_guests:
        diet = str(guest.profiles.diet.diet_type)
        diet_set.add(diet)

    diet_string = ', '.join(diet_set)

    return diet_string


def guest_diet(partyid):
    """Query that gets the diet of each guest coming to the party and figures out the most limiting"""

    diet_ranking = []
    party = Party.query.get(partyid)
    party_guests = party.guests

    for guest in party_guests:
        diet_rank = guest.profiles.diet.ranking
        diet_ranking.append(diet_rank)

    most_limiting = min(diet_ranking)
    diet_string = Diet.query.filter_by(ranking=most_limiting).first()
    diet_string = str(diet_string.diet_type)

    return diet_string


def guest_avoidances(partyid):
    """Query that gets the avoidances of each guest coming to the party"""

    avoidance_set = set()
    party = Party.query.get(partyid)
    party_guests = party.guests

    for guest in party_guests:
        avoids = guest.profiles.avoidances
        for each in avoids:
                avoidance_set.add(str(each.ingredient))

    avoidance_string = ', '.join(avoidance_set)
    return avoidance_string


def guest_intolerances(partyid):
    """Query that gets the avoidances of each guest coming to the party"""

    intolerance_set = set()
    party = Party.query.get(partyid)
    party_guests = party.guests

    for guest in party_guests:
        intols = guest.profiles.intolerances
        for each in intols:
                intolerance_set.add(str(each.intol_name))
    intolerance_string = ', '.join(intolerance_set)

    return intolerance_string


def spoonacular_request(party_id):
    """Assembles an API request to Spoonacular"""

    diet_string = guest_diet(party_id)
    intolerance_string = guest_intolerances(party_id)
    avoid_string = guest_avoidances(party_id)

    url = 'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search'
    headers = {"X-Mashape-Key": os.environ['SECRET_KEY']}
    payload = {'query': 'recipe', 'diet': diet_string, 'type': 'main course',
               'number': 300, 'intolerances': intolerance_string, 'excludeIngredients': avoid_string}
    response = requests.get(url, headers=headers, params=payload)

    print payload

    responses = {}

    spoon = response.json()

    print spoon

    possible_results = spoon['totalResults']
    print possible_results
    num_results = spoon['number']
    print num_results

    base_url = spoon.get('baseUri')
    responses["number"] = num_results
    responses["totalResults"] = possible_results
    response = []

    if num_results < possible_results:
        number = num_results
    else:
        number = possible_results

    for i in range(number):
        recipe_id = spoon['results'][i].get('id')
        image = spoon['results'][i].get('image')
        image_urls = spoon['results'][i].get('imageUrls')
        for image_url in image_urls:
            image_url = image_url
        title = spoon['results'][i].get('title')
        recipe_url_base = "http://spoonacular.com/recipes/"
        if image is not None:
            recipe_url = ""
            for letter in image:
                if letter != ".":
                    recipe_url = recipe_url + letter
                else:
                    break
        print recipe_url
        recipe_url = recipe_url_base + recipe_url
        print recipe_url
        image_url = base_url + image_url
        each_response = {}
        each_response["title"] = title
        each_response["recipe_url"] = recipe_url
        each_response["image_url"] = image_url
        each_response["recipe_id"] = recipe_id
        response.append(each_response)

    responses["response"] = response
    return responses


    # When redoing this code, use: cleaned = bleach.clean(html, tags=[], attributes={}, styles=[], strip=True)
    # where html is the text you want any html tags or script tags removed.


def new_guest_diet(diets):
    """Query that takes the diets from the form and determines the most limiting"""

    if diets:
        diet_ranking = []

        for each_diet in diets:
            this_diet = db.session.query(Diet).filter(Diet.diet_type == each_diet).first()
            this_diet_rank = this_diet.ranking
            diet_ranking.append(this_diet_rank)

        diet_ranking = sorted(diet_ranking)
        most_limiting = diet_ranking[0]
    else:
        most_limiting = 10

    diet_string = Diet.query.filter_by(ranking=most_limiting).first()
    diet_string = str(diet_string.diet_type)
    return diet_string


def new_spoonacular_request(diet, intols, avoids, cuisine, course):
    """Assembles a new API request with new variables, to Spoonacular"""

    if avoids:
        avoid_string = ', '.join(avoids)
    else:
        avoid_string = ""

    if intols:
        intolerance_string = ', '.join(intols)
    else:
        intolerance_string = ""

    cuisine = (Cuisine.query.get(cuisine))
    cuisine = (cuisine.cuisine_name)
    cuisine = str(cuisine)
    course = Course.query.get(course)
    course = course.course_name
    course = str(course)

    url = 'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search'
    headers = {"X-Mashape-Key": os.environ['SECRET_KEY']}
    payload = {'query': 'recipe', 'diet': diet, 'type': course, 'cuisine': cuisine,
               'number': 300, 'intolerances': intolerance_string, 'excludeIngredients': avoid_string}
    response = requests.get(url, headers=headers, params=payload)

    print payload

    responses = {}

    spoon = response.json()
    print spoon

    possible_results = spoon['totalResults']
    print possible_results

    num_results = spoon['number']
    base_url = spoon.get('baseUri')
    responses["number"] = num_results
    responses["totalResults"] = possible_results
    response = []

    if num_results < possible_results:
        number = num_results
    else:
        number = possible_results

    for i in range(number):
        recipe_id = spoon['results'][i].get('id')
        image = spoon['results'][i].get('image')
        image_urls = spoon['results'][i].get('imageUrls')
        for image_url in image_urls:
            image_url = image_url
        title = spoon['results'][i].get('title')
        recipe_url_base = "http://spoonacular.com/recipes/"
        if image is not None:
            recipe_url = ""
            for letter in image:
                if letter != ".":
                    recipe_url = recipe_url + letter
                else:
                    break
        # print recipe_url
        recipe_url = recipe_url_base + recipe_url
        # print recipe_url
        image_url = base_url + image_url
        each_response = {}
        each_response["title"] = title
        each_response["recipe_url"] = recipe_url
        each_response["image_url"] = image_url
        each_response["recipe_id"] = recipe_id
        each_response["avoids"] = avoid_string
        each_response["intols"] = intolerance_string
        each_response["cuisine"] = cuisine
        each_response["course"] = course

        response.append(each_response)

    responses["response"] = response
    return responses


def spoonacular_recipe_ingredients(recipe_id):
    """Assembles an API request to Spoonacular to get a recipes ingredients"""

    url1 = 'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/'
    url2 = '/information'
    url = url1 + str(recipe_id) + url2

    headers = {"X-Mashape-Key": os.environ['SECRET_KEY']}
    payload = {'id': recipe_id, 'includeNutrition': False}
    response = requests.get(url, headers=headers, params=payload)

    spoon = response.json()
    ingredients = spoon['extendedIngredients']
    ingredients_list = []
    for each in ingredients:
        print each
        one = each["originalString"]
        ingredients_list.append(one)
    print ingredients_list
    return ingredients_list


def spoonacular_recipe_instructions(recipe_id):
    """Assembles an API request to Spoonacular to get a recipes instructions"""

    url1 = 'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/'
    url2 = '/analyzedInstructions'
    url = url1 + str(recipe_id) + url2
    headers = {"X-Mashape-Key": os.environ['SECRET_KEY']}
    payload = {'stepBreakdown': True}
    response = requests.get(url, headers=headers, params=payload)

    spoon = response.json()
    print "spoon:"
    print spoon

    instructions_list = [steps['step'] for steps in spoon[0]['steps']]

    return instructions_list
