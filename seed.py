"""Utility file to seed K(i)nd database data for testing"""

from sqlalchemy import func

from Model import connect_to_db, db, Intolerance, Diet, Cuisine, Course
from server import app


def load_seeddata():
    """Load users from u.users into database."""

    diet1 = Diet(diet_type="vegan", description="does not eat an animal byproducts", ranking=1)
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="ketogenic", description="high-fat, adequate-protein, low-carbohydrate diet", ranking=2)
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="vegetarian", description="does not eat meat", ranking=3)
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="ovo vegetarian", description="vegetarianism which allows for the consumption of eggs but not dairy products", ranking=4)
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="lacto vegetarian", description="vegetarian who abstains from eating meat and eggs, but who eats dairy products", ranking=5)
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="pescatarian", description="does not eat meat but does eat fish.", ranking=6)
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="paleo", description="it's complex, but basically dairy, no gluten, corn, sugar or processed foods", ranking=7)
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="primal", description="it's complex, but basically no gluten, corn, sugar or processed foods", ranking=8)
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="whole 30", description="It's complex. No processed foods and few ingredients", ranking=9)
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="any", description="does not follow any limiting diet", ranking=10)
    db.session.add(diet1)
    db.session.commit()

    print "loaded diets"

    intol1 = Intolerance(intol_name="dairy", intol_description="Intolerance or allergy to the milk of a cow")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_name="egg", intol_description="Intolerance or allergy to eggs")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_name="gluten", intol_description="Intolerance or allergy to gluten")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_name="peanut", intol_description="Intolerance or allergy to peanuts and peanut products")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_name="sesame", intol_description="Intolerance or allergy to sesame seeds and sesame products")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_name="seafood", intol_description="Intolerance or allergy to seafood")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_name="shellfish", intol_description="Intolerance or allergy to shellfish")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_name="soy", intol_description="Intolerance or allergy to soy products")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_name="sulfites", intol_description="Intolerance or allergy to sulfites")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_name="tree nut", intol_description="Intolerance or allergy to tree nuts")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_name="wheat", intol_description="Intolerance or allergy to wheat")
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


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_testdata()
