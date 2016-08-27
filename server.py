"""K(i)nd app"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session

from Model import (connect_to_db, db, Diet, User,
                   Intolerance, Friends, Party, PartyGuest, RecipeBox)

# import os

from functions import (guest_diets, guest_intolerances, guest_avoidances,
                       spoonacular_request, make_user, make_friendship,
                       make_intolerances, make_avoidance)


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


#  The main profile pages are now appearing first due to ease of programming

@app.route('/userprofile', methods=['GET'])
def show_user_profile():
    """Show logged in user's profile"""

    user_id = session.get("user_id")
    if user_id:
        this_user = User.query.get(user_id)
        return render_template("/user_profile_page.html",
                               this_user=this_user)
    else:
        return redirect("/login")


@app.route('/friendprofile', methods=['GET'])
def show_friend_profile():
    """Show logged in user's friends profile"""

    check_id = session.get("user_id")
    if check_id:
        this_user = User.query.get(check_id)
        user_id = request.args.get("friends_id")
        newfriend = User.query.get(user_id)
        return render_template("/friends_profile_page.html",
                               newfriend=newfriend,
                               this_user=this_user)
    else:
        return redirect("/login")


@app.route('/party_profile/<int:party_id>')
def show_party_profile(party_id):
    """Show the party profile"""

    user_id = session.get("user_id")
    if user_id:
        session['party_id'] = party_id
        this_user = User.query.get(user_id)
        party = Party.query.get(party_id)
        return render_template("/party_profile.html", user_id=user_id,
                               party=party,
                               this_user=this_user)
    else:
        return redirect("/login")


@app.route('/searchrecipes')
def show_search_spoonacular():
    """Collate party information, query spoonacular and show results."""

    user_id = session.get("user_id")
    if user_id:
        this_user = User.query.get(user_id)
        party_id = session.get("party_id")
        party = Party.query.get(party_id)
        responses = spoonacular_request(party_id)
        get_diets = guest_diets(party_id)
        get_avoid = guest_avoidances(party_id)
        get_intolerance = guest_intolerances(party_id)

        return render_template("recipe_search_page.html", party=party,
                               responses=responses,
                               get_diets=get_diets,
                               get_avoid=get_avoid,
                               get_intolerance=get_intolerance,
                               this_user=this_user)
    else:
        return redirect("/login")


@app.route('/see_recipe', methods=['POST'])
def show_recipe():
    """Show a recipe to the recipe box"""

    check_id = session.get("user_id")
    if check_id:
        this_user = User.query.get(check_id)
        party_id = session.get("party_id")
        recipe_id = request.form.get("recipe_id")
        title = request.form.get("title")
        recipe_image_url = request.form.get("recipe_image_url")
        recipe_url = request.form.get("recipe_url")

        return render_template("view_recipe.html",
                               recipe_id=recipe_id,
                               party_id=party_id,
                               title=title,
                               recipe_image_url=recipe_image_url,
                               recipe_url=recipe_url,
                               this_user=this_user)
    else:
        return redirect("/login")

# ----------------

# User routes


@app.route('/')
def index():
    """Homepage."""

    user_id = session.get("user_id")
    if user_id:
        return redirect("/userprofile")
    else:
        return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def show_register_form():
    """Show form for user signup."""

    diets = Diet.query.order_by(Diet.diet_type).all()

    return render_template("register_form.html", diets=diets)


@app.route('/registered', methods=['POST'])
def add_register_users():
    """Process registration."""

    password = request.form.get("password")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    diet_id = request.form.get("diet_type")
    diet_reason = request.form.get("diet_reason")
    verified = True

    session["user_id"] = make_user(email, first_name, last_name, diet_id,
                                   diet_reason, verified, password)

    flash("Welcome to Kind Table, %s." % first_name)
    return redirect("/userprofile")


@app.route('/login', methods=['GET'])
def show_login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/loggedin', methods=['POST'])
def add_login_process():
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
def add_logout():
    """Log out."""

    check_id = session.get("user_id")
    if check_id:
        del session["user_id"]
        flash("Logged Out.")
        return redirect("/")
    else:
        return redirect("/login")

# ------------------------------


# These will be AJAX calls

@app.route('/addintoleranceform', methods=['GET'])
def show_an_intolerance():
    """Get information about a user intolerance"""

    user_id = session.get("user_id")
    if user_id:
        intol_list = Intolerance.query.order_by(Intolerance.intol_name).all()
        this_user = User.query.get(user_id)
        return render_template("/add_food_intolerance.html",
                               intol_list=intol_list,
                               this_user=this_user)
    else:
        return redirect("/login")


@app.route('/intolerance_added', methods=['POST'])
def add_an_intolerance():
    """Add a user intolerance to the user profile"""

    user_id = session.get("user_id")
    intol_ids = request.form.getlist("intol_ids")
    make_intolerances(intol_ids, user_id)

    return redirect("/userprofile")


@app.route('/addingredienttoavoid', methods=['GET'])
def show_an_ingredient():
    """Get a user's ingredient to avoid"""

    user_id = session.get("user_id")
    if user_id:
        this_user = User.query.get(user_id)
        return render_template("add_ingredient_to_avoid.html",
                               this_user=this_user)
    else:
        return redirect("/login")


@app.route('/ingredientadded', methods=['POST'])
def add_an_ingredient():
    """Add an user's ingredient to avoid to the user profile"""

    user_id = session.get("user_id")
    ingredient = request.form.get("ingredient")
    reason = request.form.get("reason")

    print ingredient
    print reason
    print user_id

    make_avoidance(user_id, ingredient, reason)

    flash("Ingredient added.")

    return redirect("/addingredienttoavoid")


@app.route('/findafriend', methods=['GET'])
def show_get_a_friend():
    """Find a friend to add to the friends table"""

    user_id = session.get("user_id")
    if user_id:
        this_user = User.query.get(user_id)
        return render_template("find_a_friend.html",
                               this_user=this_user)
    else:
        return redirect("/login")


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
        diets = Diet.query.order_by(Diet.diet_type).all()
        flash("Looks like there is no profile yet for your friend. Would you like to create one?")
        return render_template("create_friends_profile_form.html",
                               email_address=email_address,
                               diets=diets)


@app.route('/createfriendsprofile', methods=['GET'])
def show_register_friend_form():
    """Show form for adding a profile for a friend."""

    check_id = session.get("user_id")
    if check_id:
        diets = Diet.query.order_by(Diet.diet_type).all()
        return render_template("create_friends_profile_form.html", diets=diets)
    else:
        return redirect("/login")


@app.route('/friendregistered', methods=['POST'])
def add_friend_profile_registered():
    """Instantiate unverified User and make connection on friends table."""

    user_id = session.get("user_id")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    diet_id = request.form.get("diet_type")
    diet_reason = request.form.get("diet_reason")

    friend_id = make_user(email, first_name, last_name, diet_id, diet_reason)
    make_friendship(user_id, friend_id)
    newfriend = User.query.get(friend_id)

    flash("A profile has been created for your friend: %s." % first_name)

    return render_template("/friends_profile_page.html",
                           newfriend=newfriend)


@app.route('/addfriendintoleranceform', methods=['POST'])
def show_friends_intolerance():
    """Show the form to get information about a friends intolerances"""

    check_id = session.get("user_id")
    if check_id:
        user_id = request.form.get("user_id")
        newfriend = User.query.get(user_id)
        intol_list = Intolerance.query.order_by(Intolerance.intol_name).all()
        return render_template("/add_friends_food_intolerance.html",
                               intol_list=intol_list,
                               newfriend=newfriend)
    else:
        return redirect("/login")


@app.route('/friendintolerance_added', methods=['POST'])
def add_friends_intolerance():
    """Add a friend intolerance to the their profile"""

    user_id = request.form.get("user_id")
    newfriend = User.query.get(user_id)
    intol_ids = request.form.getlist("intol_ids")

    make_intolerances(intol_ids, user_id)

    return render_template("/friends_profile_page.html",
                           newfriend=newfriend)


@app.route('/addingfriendsinredienttoavoid', methods=['POST'])
def show_friends_ingredient():
    """Get a friends ingredient to avoid"""

    user_id = request.form.get("user_id")
    newfriend = User.query.get(user_id)

    return render_template("/add_friends_ingredient_to_avoid.html",
                           newfriend=newfriend)


@app.route('/friendingredientadded', methods=['POST'])
def add_friends_ingredient():
    """Add an user's ingredient to avoid to the user profile"""

    user_id = request.form.get("user_id")
    ingredient = request.form.get("ingredient")
    reason = request.form.get("reason")

    make_avoidance(user_id, ingredient, reason)

    newfriend = User.query.get(user_id)

    flash("Ingredient added.")

    return render_template("/add_friends_ingredient_to_avoid.html",
                           newfriend=newfriend)


@app.route('/addaparty', methods=['GET'])
def show_party_form():
    """Show the dinner party form"""

    check_id = session.get("user_id")
    if check_id:
        this_user = User.query.get(check_id)
        return render_template("/add_a_party.html", this_user=this_user)
    else:
        return redirect("/login")


@app.route('/party_added', methods=['POST'])
def add_party():
    """Add a new dinner party to the dinner party table"""

    user_id = session.get("user_id")
    this_user = User.query.get(user_id)
    title = request.form.get("title")
    new_party = Party(host_id=user_id, title=title)
    db.session.add(new_party)
    db.session.commit()
    party = db.session.query(Party).filter(Party.title == title).first()
    new_guest = PartyGuest(party_id=party.party_id, user_id=user_id)
    db.session.add(new_guest)
    db.session.commit()

    return render_template("/party_profile.html", party=party,
                           this_user=this_user)


@app.route('/addaguest/<int:party_id>')
def show_register_guest(party_id):
    """Show form for adding a guest to a dinner party"""

    user_id = session.get("user_id")
    if user_id:
        this_user = User.query.get(user_id)
        party = Party.query.get(party_id)
        party_guests = party.users

        return render_template("/add_a_guest.html",
                               party=party,
                               this_user=this_user,
                               party_guests=party_guests)
    else:
        return redirect("/login")


@app.route('/guest_added', methods=['POST'])
def add_guest():
    """Add a guest to a diner party"""

    party_id = request.form.get("party_id")
    guests = request.form.getlist("guests")
    for guest in guests:
        new_guest = PartyGuest(party_id=party_id, user_id=guest)
        db.session.add(new_guest)
        db.session.commit()

    return redirect('/addaguest/' + party_id)


@app.route('/addtorecipebox', methods=['POST'])
def add_recipe_box():
    """Add a recipe to the recipe box"""

    check_id = session.get("user_id")

    if check_id:
        recipe_id = request.form.get("recipe_id")
        this_recipe = RecipeBox.query.filter_by(recipe_id=recipe_id).first()
        if this_recipe:
            flash("This recipe is already saved to your Recipe Box.")
            return redirect("/searchrecipes")
        else:
            party_id = request.form.get("party_id")
            title = request.form.get("title")
            recipe_image_url = request.form.get("recipe_image_url")
            recipe_url = request.form.get("recipe_url")
            raise Exception
            new_recipe = RecipeBox(party_id=party_id,
                                   recipe_id=recipe_id,
                                   title=title,
                                   recipe_image_url=recipe_image_url,
                                   recipe_url=recipe_url)
            db.session.add(new_recipe)
            db.session.commit()
            flash("The recipe for %s has been saved to your recipe box." % title)
            return redirect("/searchrecipes")
    else:
        return redirect("/login")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
