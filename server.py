"""K(i)nd app"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from Model import connect_to_db, db, Diet, UserIntolerance, User, IngToAvoid, Intolerance

import os

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    diets = Diet.query.order_by(Diet.diet_type).all()

    return render_template("register_form.html", diets=diets)


@app.route('/registered', methods=['POST'])
def register_users():
    """Process registration."""

    password = request.form.get("password")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    diet_id = request.form.get("diet_type")
    diet_reason = request.form.get("diet_reason")

    new_user = User(password=password, first_name=first_name,
                    last_name=last_name, email=email, diet_id=diet_id, diet_reason=diet_reason)

    db.session.add(new_user)
    db.session.commit()

    newuser = db.session.query(User).filter_by(email=email).first()
    user_id = newuser.user_id

    session["user_id"] = user_id

    flash("Welcome to Kind Table, %s." % first_name)
    return redirect("/userprofile")


@app.route('/addintoleranceform', methods=['GET'])
def get_an_intolerance():
    """Get information about a user intolerance"""

    intol_list = Intolerance.query.order_by(Intolerance.intol_name).all()
    user_id = session.get("user_id")

    flash("Intolerance added.")

    return render_template("/add_food_intolerance.html", intol_list=intol_list, user_id=user_id)


@app.route('/intolerance_added', methods=['POST'])
def add_an_intolerance():
    """Add a user intolerance to the user profile"""

    user_id = session.get("user_id")
    intol_id = request.form.get("intol_id")

    new_intol = UserIntolerance(user_id=user_id, intol_id=intol_id)
    db.session.add(new_intol)
    db.session.commit()

    return redirect("/addintoleranceform")


@app.route('/addingredienttoavoid', methods=['GET'])
def get_an_ingredient():
    """Get a user's ingredient to avoid"""

    user_id = session.get("user_id")

    return render_template("/add_ingredient_to_avoid.html", user_id=user_id)


@app.route('/ingredientadded', methods=['POST'])
def add_an_ingredient():
    """Add an user's ingredient to avoid to the user profile"""

    user_id = session.get("user_id")
    ingredient = request.form.get("ingredient")
    reason = request.form.get("reason")

    new_avoid = IngToAvoid(user_id=user_id, ingredient=ingredient, reason=reason)
    db.session.add(new_avoid)
    db.session.commit()

    flash("Ingredient added.")

    return redirect("/addingredienttoavoid")


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if user:
        if user.password is None:
            flash("Would you like to claim this email address as your own? Someone has already saved a place for you.")
            return redirect("/register")
        elif user.password != password:
            flash("Incorrect password")
            return redirect("/login")
    elif not user:
        flash("You seem to be new here. Would you like to register? If not, please check your email address")
        return redirect("/register")
    elif user.password == password:
        session["user_id"] = user.user_id
        flash("Logged in")
        return redirect("/userprofile")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/userprofile', methods=['GET'])
def show_user_profile():
    """Add a guest to a dinner party"""

    user_id = session.get("user_id")
    this_user = db.session.query(User).filter(User.user_id == user_id).first()
    this_users_avoids = db.session.query(IngToAvoid).filter(IngToAvoid.user_id == user_id).all()
    this_users_diet = db.session.query(Diet).filter(this_user.diet_id == Diet.diet_id).first()

    return render_template("/user_profile_page.html",
                           user_id=user_id,
                           this_user=this_user,
                           this_users_avoids=this_users_avoids,
                           this_users_diet=this_users_diet)


@app.route('/findafriend', methods=['GET'])
def get_a_friend():
    """Find a friend to add to the friends table"""

    user_id = session.get("user_id")

    return render_template("/add_a_friend.html", user_id=user_id)


@app.route('/addafriend', methods=['post'])
def add_a_friend():
    """Add a friend connections to the friends table"""

    user_id = session.get("user_id")
    email_address = request.form.get("email_address")

    your_friend = db.session.query(User).filter(User.email == friend_email).first()

    # if your_friend:
    #     new_friend =


    all_users = User.quert

    return render_template("/add_a_friend.html", user_id=user_id)


@app.route('/addaparty', methods=['GET'])
def register_party():
    """Add a new dinner party to the dinner party table"""

    user_id = session.get("user_id")

    return render_template("/add_a_party.html", user_id=user_id)


@app.route('/addaguest', methods=['GET'])
def register_guest():
    """Add a guest to a dinner party"""

    user_id = session.get("user_id")

    return render_template("/add_a_party.html", user_id=user_id)










if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
