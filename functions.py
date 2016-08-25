# # from sqlalchemy import func

from Model import connect_to_db, db, User, UserIntolerance, Intolerance, Diet, IngToAvoid, PartyGuest, Party
# from server import app

import requests
import os
import json


# payload = {'query': 'recipe', 'diet': 'vegan', 'type': 'main course',
#            'number': 60, 'intolerances': 'gluten', 'excludeIngredients': 'peanuts, broccoli'}


# payload = {'query': 'recipe', 'diet': guest_diets(partyid), 'type': 'main course',
#            'number': 60, 'intolerances': guest_intolerances(), 'excludeIngredients': guest_avoidances()}

def guest_diets(partyid):
    """Query that gets the diet of each guest coming to the party"""

    diet_string = set()
    hostparty = Party.query.get(partyid)
    party_guests = hostparty.users

    for guest in party_guests:
        diet = guest.diet
        diet_string.add(diet.diet_type)

    ', '.join(diet_string)

    return diet_string


def guest_avoidances(partyid):
    """Query that gets the avoidances of each guest coming to the party"""

    avoidance_string = set()
    hostparty = Party.query.get(partyid)
    party_guests = hostparty.users

    for guest in party_guests:
        avoids = guest.avoidances
        for each in avoids:
            avoidance_string.add(each.ingredient)

    ', '.join(avoidance_string)
    return avoidance_string


def guest_intolerances(partyid):
    """Query that gets the avoidances of each guest coming to the party"""

    intolerance_string = set()
    hostparty = Party.query.get(partyid)
    party_guests = hostparty.users

    for guest in party_guests:
        f = guest.user_id
        person = User.query.get(f)
        person_intolerances = person.intolerances  # this is where it goes awry
        for each in person_intolerances:
            intolerance_string.add(each.intol_name)
        ', '.join(intolerance_string)
    return intolerance_string

# ************************************************


def spoonacular_request(party_id):

    diet_string = guest_diets(party_id)
    intolerance_string = guest_intolerances(party_id)
    avoid_string = guest_avoidances(party_id)

    url = 'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search'
    headers = {"X-Mashape-Key": os.environ['SECRET_KEY']}
    payload = {'query': 'recipe', 'diet': diet_string, 'type': 'main course',
               'number': 60, 'intolerances': intolerance_string, 'excludeIngredients': avoid_string}
    response = requests.get(url, headers=headers, params=payload)

    responses = {}

    spoon = response.json()
    num_results = spoon['number']
    base_url = spoon.get('baseUri')
    responses["number"] = num_results
    response = []

    for i in range(num_results):
        image = spoon['results'][i].get('image')
        image_urls = spoon['results'][i].get('imageUrls')
        for image_url in image_urls:
            image_url = image_url
        title = spoon['results'][i].get('title')
        recipe_url_base = "http://spoonacular.com/recipes/"
        recipe_url = image.rstrip(".jpg")
        recipe_url = recipe_url_base + recipe_url
        image_url = base_url + image_url
        each_response = {}
        each_response["title"] = title
        each_response["recipe_url"] = recipe_url
        each_response["image_url"] = image_url
        response.append(each_response)

    responses["response"] = response
    return responses

# animals = {
#     'goat': {'number': 6,  'feed': 'everything',   'bites': True},
#     'pony': {'number': 1,  'feed': 'hay and oats', 'bites': True},
#     'duck': {'number': 14, 'feed': 'pond muck',    'bites': False},
# }
# >>> # do ponies bite?
# >>> print animals["pony"]["bites"]
# True



#  The url for the recipe will be a dash seperated title + dash + _id
