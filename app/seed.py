"""Loads seed data"""

from models import Diet, Intolerance, Cuisine, Course, Profile, User, Friend, Party
import pytz
from datetime import datetime


def LoadSeedData():
    """Load seed data about Spoonacular."""

    Diet.create_record(diet_id=1, diet_type="vegan", description="does not eat any animal byproducts", ranking=1)
    Diet.create_record(diet_id=2, diet_type="ketogenic", description="high-fat, adequate-protein, low-carbohydrate diet", ranking=2)
    Diet.create_record(diet_id=3, diet_type="vegetarian", description="does not eat meat", ranking=3)
    Diet.create_record(diet_id=4, diet_type="ovo vegetarian", description="vegetarianism which allows for the consumption of eggs but not dairy products", ranking=4)
    Diet.create_record(diet_id=5, diet_type="lacto vegetarian", description="vegetarian who abstains from eating meat and eggs, but who eats dairy products", ranking=5)
    Diet.create_record(diet_id=6, diet_type="pescatarian", description="does not eat meat but does eat fish.", ranking=6)
    Diet.create_record(diet_id=7, diet_type="paleo", description="it's complex, but basically no dairy, no gluten, no corn, no sugar nor processed foods", ranking=7)
    Diet.create_record(diet_id=8, diet_type="primal", description="it's complex, but basically no gluten, no corn, no sugar nor processed foods", ranking=8)
    Diet.create_record(diet_id=9, diet_type="whole 30", description="it's complex. No processed foods and fewer ingredients", ranking=9)
    Diet.create_record(diet_id=10, diet_type="any", description="does not follow any limiting diet", ranking=10)

    print "loaded diets"

    Intolerance.create_record(intol_id=1, intol_name="dairy", intol_description="Intolerance or allergy to animal milk or animal milk products")
    Intolerance.create_record(intol_id=2, intol_name="egg", intol_description="Intolerance or allergy to eggs or egg byproducts")
    Intolerance.create_record(intol_id=3, intol_name="gluten", intol_description="Intolerance or allergy to ingredients that contain gluten")
    Intolerance.create_record(intol_id=4, intol_name="peanut", intol_description="Intolerance or allergy to peanuts and peanut products")
    Intolerance.create_record(intol_id=5, intol_name="sesame", intol_description="Intolerance or allergy to sesame seeds and sesame products")
    Intolerance.create_record(intol_id=6, intol_name="seafood", intol_description="Intolerance or allergy to fish or fish products ")
    Intolerance.create_record(intol_id=7, intol_name="shellfish", intol_description="Intolerance or allergy to shellfish or shellfish products")
    Intolerance.create_record(intol_id=8, intol_name="soy", intol_description="Intolerance or allergy to soy products")
    Intolerance.create_record(intol_id=9, intol_name="sulfites", intol_description="Intolerance or allergy to ingredients that contain sulfites")
    Intolerance.create_record(intol_id=10, intol_name="tree nut", intol_description="Intolerance or allergy to tree nuts or tree nut products")
    Intolerance.create_record(intol_id=11, intol_name="wheat", intol_description="Intolerance or allergy to wheat or wheat products")

    print "loaded intolerances"

    Cuisine.create_record(cuisine_name="african")
    Cuisine.create_record(cuisine_name="chinese")
    Cuisine.create_record(cuisine_name="japanese")
    Cuisine.create_record(cuisine_name="korean")
    Cuisine.create_record(cuisine_name="vietnamese")
    Cuisine.create_record(cuisine_name="thai")
    Cuisine.create_record(cuisine_name="indian")
    Cuisine.create_record(cuisine_name="british")
    Cuisine.create_record(cuisine_name="irish")
    Cuisine.create_record(cuisine_name="french")
    Cuisine.create_record(cuisine_name="italian")
    Cuisine.create_record(cuisine_name="mexican")
    Cuisine.create_record(cuisine_name="spanish")
    Cuisine.create_record(cuisine_name="middle eastern")
    Cuisine.create_record(cuisine_name="jewish")
    Cuisine.create_record(cuisine_name="american")
    Cuisine.create_record(cuisine_name="cajun")
    Cuisine.create_record(cuisine_name="southern")
    Cuisine.create_record(cuisine_name="greek")
    Cuisine.create_record(cuisine_name="german")
    Cuisine.create_record(cuisine_name="nordic")
    Cuisine.create_record(cuisine_name="eastern european")
    Cuisine.create_record(cuisine_name="caribbean")
    Cuisine.create_record(cuisine_name="latin american")

    print "loaded Cuisines"

    Course.create_record(course_name="main course")
    Course.create_record(course_name="side dish")
    Course.create_record(course_name="dessert")
    Course.create_record(course_name="appetizer")
    Course.create_record(course_name="salad")
    Course.create_record(course_name="bread")
    Course.create_record(course_name="breakfast")
    Course.create_record(course_name="soup")
    Course.create_record(course_name="beverage")
    Course.create_record(course_name="sauce")
    Course.create_record(course_name="drink")

    print "loaded Courses"


def LoadTestPeople():
    """Load fake users and information in development only"""

    ilsa_profile = Profile.create_record(email='ilsalacious@gmail.com', email_verified=True, first_name='Ilsa', last_name='Gordon')
    todd_profile = Profile.create_record(email='censorydep@gmail.com', email_verified=True, first_name='Todd', last_name='Gage')
    darrin_profile = Profile.create_record(email='darrin@erin.com', email_verified=False, first_name='Darrin', last_name='Ward')
    erin_profile = Profile.create_record(email='erin@darrin.com', email_verified=False, first_name='Erin', last_name='Rosenthal')

    User.create_record(password="Password!", profile_id=1)
    User.create_record(password='No', profile_id=2)

    ilsa_profile = Profile.query.get(1)
    todd_profile = Profile.query.get(2)
    darrin_profile = Profile.query.get(3)
    erin_profile = Profile.query.get(4)

    ilsa_profile.update({'owned_by_user_id': 1})
    darrin_profile.update({'owned_by_user_id': 1})
    erin_profile.update({'owned_by_user_id': 1})
    todd_profile.update({'owned_by_user_id': 2})

    print "Profiles and Users loaded"

    Friend.create_record(user_id=1, friend_profile_id=2, friendship_verified_by_email=True)
    Friend.create_record(user_id=1, friend_profile_id=3, friendship_verified_by_email=False)
    Friend.create_record(user_id=1, friend_profile_id=4, friendship_verified_by_email=False)
    Friend.create_record(user_id=2, friend_profile_id=1, friendship_verified_by_email=True)

    print "Friends added"

    pac = pytz.timezone('America/Los_Angeles')
    utc = pytz.utc

    dt = datetime(2017, 2, 14, 19, 0)
    dt1 = pac.localize(dt, is_dst=True)
    utc_dt2 = dt1.astimezone(utc)

    Party.create_record(party_id="1", title="This is the best party", user_id=1, datetime_of_party=utc_dt2)

    dt = datetime(2017, 3, 14, 17, 0)
    dt1 = pac.localize(dt, is_dst=True)
    utc_dt2 = dt1.astimezone(utc)

    Party.create_record(party_id="2", title="This party is ok", user_id=1, datetime_of_party=utc_dt2)

    print "Party added"
