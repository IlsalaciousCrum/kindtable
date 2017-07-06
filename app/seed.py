"""Loads seed data"""

from models import (Diet, Intolerance, Cuisine, Course, Profile, User,
                    Friend, Party, PartyGuest, RecipeCard,
                    PartyRecipes, IngToAvoid, ProfileIntolerance)
import pytz
from datetime import datetime


def LoadSeedData():
    """Load seed data about Spoonacular."""

    Diet.create_record(diet_id=1,
                       diet_type="vegan",
                       description="does not eat any animal byproducts",
                       ranking=1)
    Diet.create_record(diet_id=2,
                       diet_type="ketogenic",
                       description="high-fat, adequate-protein, low-carbohydrate diet",
                       ranking=2)
    Diet.create_record(diet_id=3,
                       diet_type="vegetarian",
                       description="does not eat meat",
                       ranking=3)
    Diet.create_record(diet_id=4,
                       diet_type="ovo vegetarian",
                       description="vegetarianism which allows for the consumption of eggs but not dairy products",
                       ranking=4)
    Diet.create_record(diet_id=5,
                       diet_type="lacto vegetarian",
                       description="vegetarian who abstains from eating meat and eggs, but who eats dairy products",
                       ranking=5)
    Diet.create_record(diet_id=6,
                       diet_type="pescatarian",
                       description="does not eat meat but does eat fish.",
                       ranking=6)
    Diet.create_record(diet_id=7,
                       diet_type="paleo",
                       description="it's complex, but basically no dairy, no gluten, no corn, no sugar nor processed foods",
                       ranking=7)
    Diet.create_record(diet_id=8,
                       diet_type="primal",
                       description="it's complex, but basically no gluten, no corn, no sugar nor processed foods",
                       ranking=8)
    Diet.create_record(diet_id=9,
                       diet_type="whole 30",
                       description="it's complex. No processed foods and fewer ingredients",
                       ranking=9)
    Diet.create_record(diet_id=10,
                       diet_type="any",
                       description="does not follow any limiting diet",
                       ranking=10)

    print "loaded diets"

    Intolerance.create_record(intol_id=1,
                              intol_name="dairy",
                              intol_description="Intolerance or allergy to animal milk or animal milk products")
    Intolerance.create_record(intol_id=2,
                              intol_name="egg",
                              intol_description="Intolerance or allergy to eggs or egg byproducts")
    Intolerance.create_record(intol_id=3,
                              intol_name="gluten",
                              intol_description="Intolerance or allergy to ingredients that contain gluten")
    Intolerance.create_record(intol_id=4,
                              intol_name="peanut",
                              intol_description="Intolerance or allergy to peanuts and peanut products")
    Intolerance.create_record(intol_id=5,
                              intol_name="sesame",
                              intol_description="Intolerance or allergy to sesame seeds and sesame products")
    Intolerance.create_record(intol_id=6,
                              intol_name="seafood",
                              intol_description="Intolerance or allergy to fish or fish products ")
    Intolerance.create_record(intol_id=7,
                              intol_name="shellfish",
                              intol_description="Intolerance or allergy to shellfish or shellfish products")
    Intolerance.create_record(intol_id=8,
                              intol_name="soy",
                              intol_description="Intolerance or allergy to soy products")
    Intolerance.create_record(intol_id=9,
                              intol_name="sulfites",
                              intol_description="Intolerance or allergy to ingredients that contain sulfites")
    Intolerance.create_record(intol_id=10,
                              intol_name="tree nut",
                              intol_description="Intolerance or allergy to tree nuts or tree nut products")
    Intolerance.create_record(intol_id=11,
                              intol_name="wheat",
                              intol_description="Intolerance or allergy to wheat or wheat products")

    print "loaded intolerances"

    Cuisine.create_record(cuisine_id="1", cuisine_name="any")
    Cuisine.create_record(cuisine_id="2", cuisine_name="african")
    Cuisine.create_record(cuisine_id="3", cuisine_name="chinese")
    Cuisine.create_record(cuisine_id="4", cuisine_name="japanese")
    Cuisine.create_record(cuisine_id="5", cuisine_name="korean")
    Cuisine.create_record(cuisine_id="6", cuisine_name="vietnamese")
    Cuisine.create_record(cuisine_id="7", cuisine_name="thai")
    Cuisine.create_record(cuisine_id="8", cuisine_name="indian")
    Cuisine.create_record(cuisine_id="9", cuisine_name="british")
    Cuisine.create_record(cuisine_id="10", cuisine_name="irish")
    Cuisine.create_record(cuisine_id="11", cuisine_name="french")
    Cuisine.create_record(cuisine_id="12", cuisine_name="italian")
    Cuisine.create_record(cuisine_id="13", cuisine_name="mexican")
    Cuisine.create_record(cuisine_id="14", cuisine_name="spanish")
    Cuisine.create_record(cuisine_id="15", cuisine_name="middle eastern")
    Cuisine.create_record(cuisine_id="16", cuisine_name="jewish")
    Cuisine.create_record(cuisine_id="17", cuisine_name="american")
    Cuisine.create_record(cuisine_id="18", cuisine_name="cajun")
    Cuisine.create_record(cuisine_id="19", cuisine_name="southern")
    Cuisine.create_record(cuisine_id="20", cuisine_name="greek")
    Cuisine.create_record(cuisine_id="21", cuisine_name="german")
    Cuisine.create_record(cuisine_id="22", cuisine_name="nordic")
    Cuisine.create_record(cuisine_id="23", cuisine_name="eastern european")
    Cuisine.create_record(cuisine_id="24", cuisine_name="caribbean")
    Cuisine.create_record(cuisine_id="25", cuisine_name="latin american")

    print "loaded Cuisines"

    Course.create_record(course_id="1", course_name="main course")
    Course.create_record(course_id="2", course_name="side dish")
    Course.create_record(course_id="3", course_name="dessert")
    Course.create_record(course_id="4", course_name="appetizer")
    Course.create_record(course_id="5", course_name="salad")
    Course.create_record(course_id="6", course_name="bread")
    Course.create_record(course_id="7", course_name="breakfast")
    Course.create_record(course_id="8", course_name="soup")
    Course.create_record(course_id="9", course_name="beverage")
    Course.create_record(course_id="10", course_name="sauce")
    Course.create_record(course_id="11", course_name="drink")

    print "loaded Courses"
