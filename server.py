"""K(i)nd app"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from Model import connect_to_db, db, Diet, UserIntolerance, User, IngToAvoid, Intolerance, Friends, Party, PartyGuest

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
                    last_name=last_name, email=email, diet_id=diet_id, diet_reason=diet_reason, verified=True)

    db.session.add(new_user)
    db.session.commit()

    newuser = db.session.query(User).filter_by(email=email).first()
    user_id = newuser.user_id

    session["user_id"] = user_id

    flash("Welcome to Kind Table, %s." % first_name)
    return redirect("/userprofile")


@app.route('/createfriendsprofile', methods=['GET'])
def register_friend_form():
    """Show form for adding a profile for a friend."""

    diets = Diet.query.order_by(Diet.diet_type).all()

    return render_template("create_friends_profile_form.html", diets=diets)


@app.route('/friendregistered', methods=['POST'])
def friend_profile_registered():
    """Instantiate User for friend and make connection on friends table."""

    user_id = session.get("user_id")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    diet_id = request.form.get("diet_type")
    diet_reason = request.form.get("diet_reason")

    friend_user = User(first_name=first_name,
                       last_name=last_name, email=email, diet_id=diet_id, diet_reason=diet_reason)

    db.session.add(friend_user)
    db.session.commit()

    newfriend = db.session.query(User).filter_by(email=email).first()

    add_to_friends = Friends(user_id=user_id, friend_id=newfriend.user_id)

    db.session.add(add_to_friends)
    db.session.commit()

    flash("A profile has been created for your friend: %s." % first_name)
    return redirect("/createfriendsprofile")


@app.route('/addintoleranceform', methods=['GET'])
def get_an_intolerance():
    """Get information about a user intolerance"""

    user_id = session.get("user_id")

    intol_list = Intolerance.query.order_by(Intolerance.intol_name).all()
    this_user = User.query.get(user_id)

    flash("Intolerance added.")

    return render_template("/add_food_intolerance.html",
                           intol_list=intol_list,
                           user_id=user_id,
                           this_user=this_user)


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
    avoids = db.session.query(IngToAvoid).filter(IngToAvoid.user_id == user_id).all()

    return render_template("/add_ingredient_to_avoid.html", user_id=user_id, avoids=avoids)


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


@app.route('/loggedin', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if user:
        if user.password != password:
            flash("Incorrect password")
            return redirect("/login")
        elif user.password == password:
            session["user_id"] = user.user_id
            flash("Logged in")
            return redirect("/userprofile")
    elif not user:
        flash("You seem to be new here. Would you like to register? If not, please check your email address")
        return redirect("/register")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/userprofile', methods=['GET'])
def show_user_profile():
    """Show logged in user's profile"""

    user_id = session.get("user_id")
    this_user = db.session.query(User).filter(User.user_id == user_id).first()
    this_users_avoids = db.session.query(IngToAvoid).filter(IngToAvoid.user_id == user_id).all()
    this_users_diet = db.session.query(Diet).filter(this_user.diet_id == Diet.diet_id).first()
    this_users_parties = db.session.query(Party).filter(this_user.user_id == Party.host_id).all()

    return render_template("/user_profile_page.html",
                           user_id=user_id,
                           this_user=this_user,
                           this_users_avoids=this_users_avoids,
                           this_users_diet=this_users_diet,
                           this_users_parties=this_users_parties)


@app.route('/friendprofile', methods=['GET'])
def show_friend_profile():
    """Show logged in user's profile"""

    user_id = request.args.get("friends_id")
    this_user = db.session.query(User).filter(User.user_id == user_id).first()
    this_users_avoids = db.session.query(IngToAvoid).filter(IngToAvoid.user_id == user_id).all()
    this_users_diet = db.session.query(Diet).filter(this_user.diet_id == Diet.diet_id).first()

    return render_template("/friends_profile_page.html",
                           user_id=user_id,
                           this_user=this_user,
                           this_users_avoids=this_users_avoids,
                           this_users_diet=this_users_diet)


@app.route('/findafriend', methods=['GET'])
def get_a_friend():
    """Find a friend to add to the friends table"""

    user_id = session.get("user_id")
    this_user = User.query.get(user_id)

    return render_template("find_a_friend.html",
                           user_id=user_id,
                           this_user=this_user)


@app.route('/addafriend', methods=['POST'])
def add_a_friend():
    """Add a friend connections to the friends table"""

    user_id = session.get("user_id")
    email_address = request.form.get("email_address")

    in_database = db.session.query(User).filter(User.email == email_address).first()

    if in_database is not None:
        check_for_friend = db.session.query(Friends).filter(Friends.user_id == user_id, Friends.friend_id == in_database.user_id).first()
        if check_for_friend:
            flash("This person is already one of your friends. Would you like to add someone else?")
            return redirect("/findafriend")
        else:
            friend_id = in_database.user_id
            newfriend = Friends(user_id=user_id, friend_id=friend_id)
            db.session.add(newfriend)
            db.session.commit()
            flash("Friend added.")
            return redirect("/findafriend")
    else:
        flash("Looks like there is no profile yet for your friend. Would you like to create one?")
        return redirect("/createfriendsprofile")


@app.route('/addaparty', methods=['GET'])
def show_party_form():
    """Show the dinner party form"""

    user_id = session.get("user_id")

    return render_template("/add_a_party.html", user_id=user_id)


@app.route('/party_added', methods=['POST'])
def party_added():
    """Add a new dinner party to the dinner party table"""

    user_id = session.get("user_id")
    title = request.form.get("title")
    new_party = Party(host_id=user_id, title=title)
    db.session.add(new_party)
    db.session.commit()
    party = db.session.query(Party).filter(Party.title == title).first()

    return render_template("/party_profile.html", party=party)


@app.route('/party_profile/<int:party_id>')
def show_party_profile(party_id):
    """Show the party profile"""

    user_id = session.get("user_id")
    party = Party.query.get(party_id)

    return render_template("/party_profile.html", user_id=user_id,
                           party=party)


@app.route('/addaguest/<int:party_id>')
def register_guest(party_id):
    """Show form for adding a guest to a dinner party"""

    user_id = session.get("user_id")
    this_user = User.query.get(user_id)
    party = Party.query.get(party_id)
    party_guests = party.users

    return render_template("/add_a_guest.html",
                           party=party,
                           this_user=this_user,
                           party_guests=party_guests)


@app.route('/guest_added', methods=['POST'])
def guest_added():
    """Add a guest to a diner party"""

    party_id = request.form.get("party_id")
    guest = request.form.get("guest")
    new_guest = PartyGuest(party_id=party_id, user_id=guest)
    db.session.add(new_guest)
    db.session.commit()

    return redirect('/addaguest/' + party_id)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
