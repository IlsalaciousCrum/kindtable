"""Loads seed data"""

from models import Diet, Intolerance, Cuisine, Course, Profile, User, Friend, Party
from app import db
from pytz import timezone
import pytz
from datetime import datetime


def LoadTestPeople():
    """Load fake users and information in development only"""

    ilsa = Profile(profile_id=1, is_user_profile=True, created_by_email_owner=True, email='ilsalacious@gmail.com', email_verified=True, first_name='Ilsa', last_name='Gordon')
    db.session.add(ilsa)
    db.session.commit()
    todd = Profile(profile_id=2, is_user_profile=True, created_by_email_owner=True, email='censorydep@gmail.com', email_verified=True, first_name='Todd', last_name='Gage')
    db.session.add(todd)
    db.session.commit()

    darrin = Profile(profile_id=3, is_user_profile=False, created_by_email_owner=False, email='darrin@erin.com', email_verified=False, first_name='Darrin', last_name='Ward')
    db.session.add(darrin)
    db.session.commit()
    erin = Profile(profile_id=4, is_user_profile=False, created_by_email_owner=False, email='erin@darrin.com', email_verified=False, first_name='Erin', last_name='Rosenthal')
    db.session.add(erin)
    db.session.commit()
    ilsa = User(id=1, password="Password!", profile_id=1)
    db.session.add(ilsa)
    db.session.commit()
    todd = User(id=2, password='No', profile_id=2)
    db.session.add(todd)
    db.session.commit()

    print "Profiles and Users loaded"

    ilsa_friend = Friend(user_id=1, friend_profile_id=2, friendship_verified_by_email=True)
    db.session.add(ilsa_friend)
    db.session.commit()

    darrin_friend = Friend(user_id=1, friend_profile_id=3, friendship_verified_by_email=False)
    db.session.add(darrin_friend)
    db.session.commit()

    erin_friend = Friend(user_id=1, friend_profile_id=4, friendship_verified_by_email=False)
    db.session.add(erin_friend)
    db.session.commit()

    todd_friend = Friend(user_id=2, friend_profile_id=1, friendship_verified_by_email=True)
    db.session.add(todd_friend)
    db.session.commit()

    print "Friends added"

    pac = pytz.timezone('America/Los_Angeles')
    utc = pytz.utc

    dt = datetime(2017, 2, 14, 19, 0)
    dt1 = pac.localize(dt, is_dst=True)
    utc_dt2 = dt1.astimezone(utc)

    party = Party(party_id="1", title="This is the best party", user_id=1, datetime_of_party=utc_dt2)
    db.session.add(party)
    db.session.commit()

    dt = datetime(2017, 3, 14, 17, 0)
    dt1 = pac.localize(dt, is_dst=True)
    utc_dt2 = dt1.astimezone(utc)

    party = Party(party_id="2", title="This party is ok", user_id=1, datetime_of_party=utc_dt2)
    db.session.add(party)
    db.session.commit()

    print "Party added"


def LoadSeedData():
    """Load seed data about Spoonacular."""

    diet1 = Diet(diet_id=1, diet_type="vegan", description="does not eat an animal byproducts", ranking=1)
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_id=2, diet_type="ketogenic", description="high-fat, adequate-protein, low-carbohydrate diet", ranking=2)
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_id=3, diet_type="vegetarian", description="does not eat meat", ranking=3)
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_id=4, diet_type="ovo vegetarian", description="vegetarianism which allows for the consumption of eggs but not dairy products", ranking=4)
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_id=5, diet_type="lacto vegetarian", description="vegetarian who abstains from eating meat and eggs, but who eats dairy products", ranking=5)
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_id=6, diet_type="pescatarian", description="does not eat meat but does eat fish.", ranking=6)
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_id=7, diet_type="paleo", description="it's complex, but basically dairy, no gluten, corn, sugar or processed foods", ranking=7)
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_id=8, diet_type="primal", description="it's complex, but basically no gluten, corn, sugar or processed foods", ranking=8)
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_id=9, diet_type="whole 30", description="It's complex. No processed foods and few ingredients", ranking=9)
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_id=10, diet_type="any", description="does not follow any limiting diet", ranking=10)
    db.session.add(diet1)
    db.session.commit()

    print "loaded diets"

    intol1 = Intolerance(intol_id=1, intol_name="dairy", intol_description="Intolerance or allergy to the milk of a cow")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_id=2, intol_name="egg", intol_description="Intolerance or allergy to eggs")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_id=3, intol_name="gluten", intol_description="Intolerance or allergy to gluten")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_id=4, intol_name="peanut", intol_description="Intolerance or allergy to peanuts and peanut products")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_id=5, intol_name="sesame", intol_description="Intolerance or allergy to sesame seeds and sesame products")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_id=6, intol_name="seafood", intol_description="Intolerance or allergy to seafood")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_id=7, intol_name="shellfish", intol_description="Intolerance or allergy to shellfish")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_id=8, intol_name="soy", intol_description="Intolerance or allergy to soy products")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_id=9, intol_name="sulfites", intol_description="Intolerance or allergy to sulfites")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_id=10, intol_name="tree nut", intol_description="Intolerance or allergy to tree nuts")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_id=11, intol_name="wheat", intol_description="Intolerance or allergy to wheat")
    db.session.add(intol1)
    db.session.commit()

    print "loaded intolerances"

    cuisine1 = Cuisine(cuisine_name="african")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="chinese")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="japanese")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="korean")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="vietnamese")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="thai")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="indian")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="british")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="irish")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="french")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="italian")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="mexican")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="spanish")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="middle eastern")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="jewish")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="american")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="cajun")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="southern")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="greek")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="german")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="nordic")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="eastern european")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="caribbean")
    db.session.add(cuisine1)
    db.session.commit()
    cuisine1 = Cuisine(cuisine_name="latin american")
    db.session.add(cuisine1)
    db.session.commit()

    print "loaded Cuisines"

    course1 = Course(course_name="main course")
    db.session.add(course1)
    db.session.commit()
    course1 = Course(course_name="side dish")
    db.session.add(course1)
    db.session.commit()
    course1 = Course(course_name="dessert")
    db.session.add(course1)
    db.session.commit()
    course1 = Course(course_name="appetizer")
    db.session.add(course1)
    db.session.commit()
    course1 = Course(course_name="salad")
    db.session.add(course1)
    db.session.commit()
    course1 = Course(course_name="bread")
    db.session.add(course1)
    db.session.commit()
    course1 = Course(course_name="breakfast")
    db.session.add(course1)
    db.session.commit()
    course1 = Course(course_name="soup")
    db.session.add(course1)
    db.session.commit()
    course1 = Course(course_name="beverage")
    db.session.add(course1)
    db.session.commit()
    course1 = Course(course_name="sauce")
    db.session.add(course1)
    db.session.commit()
    course1 = Course(course_name="drink")
    db.session.add(course1)
    db.session.commit()

    print "loaded Courses"
