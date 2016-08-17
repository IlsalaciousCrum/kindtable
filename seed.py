"""Utility file to seed K(i)nd database data for testing"""

from sqlalchemy import func

from Model import connect_to_db, db, Intolerance, Diet
from server import app


def load_testdata():
    """Load users from u.users into database."""

    diet1 = Diet(diet_type="pescatarian", description="does not eat meat but does eat fish.")
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="lacto vegetarian", description="vegetarian who abstains from eating meat and eggs, but who eats dairy products")
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="ovo vegetarian", description="vegetarianism which allows for the consumption of eggs but not dairy products")
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="vegan", description="does not eat an animal byproducts")
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="vegetarian", description="does not eat meat")
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="any", description="does not follow any limiting diet")
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="primal", description="it's complex, but basically no gluten, corn, sugar or processed foods")
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="paleo", description="it's complex, but basically dairy, no gluten, corn, sugar or processed foods")
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="ketogenic", description="high-fat, adequate-protein, low-carbohydrate diet")
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="whole 30", description="It's complex. No processed foods and few ingredients")
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


   


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_testdata()
