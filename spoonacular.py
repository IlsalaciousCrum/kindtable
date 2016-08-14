import requests
import os
import json

url = 'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search'
headers = {"X-Mashape-Key": os.environ['SECRET_KEY']}

payload = {'query': 'recipe', 'diet': guest_diets(partyid), 'type': 'main course',
           'number': 60, 'intolerances': guest_intolerances(), 'excludeIngredients': guest_avoidances()}

# payload = {'query': 'recipe', 'diet': 'vegan', 'type': 'main course',
#            'number': 60, 'intolerances': 'gluten', 'excludeIngredients': 'peanuts, broccoli'}

response = requests.get(url, headers=headers, params=payload)

result = response.json()

f = open('data.json', 'w')

for recipe in result['results']:  # for each business, get details and dump into a file, one JSON per line
    _id = recipe['id']
    readyInMinutes = recipe['readyInMinutes']
    image = recipe['image']
    image_url = recipe['imageUrls']
    title = recipe['title']
    print title
    line = json.dumps(recipe)
    f.write(title + _id)
    f.write(line+'\n')


#  The url for the recipe will be a dash seperated title + dash + _id
