"""K(i)nd app"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from Model import connect_to_db, db, Diet, Intolerance, User

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


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    username = request.form["username"]
    password = request.form["password"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    phone = request.form["phone"]
    preferred_com = request.form["preferred_com"]
    diet_id = request.form["diet_type"]

    new_user = User(username=username, password=password, first_name=first_name,
                    last_name=last_name, email=email, phone=phone, preferred_com=preferred_com, diet_id=diet_id)

    db.session.add(new_user)
    db.session.commit()

    newuser = db.session.query(User).filter_by(username=username).first()
    newuser_id = newuser.user_id

    return redirect("/registerfood/%s" % newuser_id)


@app.route('/registerfood/<int:user_id>', methods=['POST'])
def register_form():
    """Show form for adding food preferences to profile."""

    intol_list = Intolerance.query.order_by(Intolerance.intol_name).all()

    intol_id = int(request.form["intolerances"])

    return render_template("register_food_preferences.html", intolerances=intolerances)


    diet_id = int(request.form["diet_id"])
    diet_reason = request.form["diet_reason"]





    new_user = User(email=email, password=password, age=age, zipcode=zipcode)

    db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % email)
    return redirect("/users/%s" % new_user.user_id)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
