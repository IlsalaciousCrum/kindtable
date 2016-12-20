"""K(i)nd app"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, json

from Model import (connect_to_db, db, Diet, User,
                   Intolerance, Friends, Party, PartyGuest, RecipeBox, Course, Cuisine, PartyRecipes)

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from flask_mail import Mail, Message

import os

from functions import (guest_intolerances, guest_avoidances,
                       spoonacular_request, make_user, make_friendship,
                       make_intolerances, make_avoidance, user_change,
                       spoonacular_recipe_instructions, all_guest_diets,
                       new_guest_diet, new_spoonacular_request, spoonacular_recipe_ingredients)

app = Flask(__name__)

# config variables for Flask-Mail

app.config.update(
    DEBUG=True,
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.environ['KIND_TABLE_EMAIL'],
    MAIL_PASSWORD=os.environ['KIND_TABLE_EMAIL_PASSWORD'],
    )
mail = Mail(app)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ['APP_SECRET_KEY']

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

# handles schema migration
migrate = Migrate(app, db)
manager = Manager(app)
server = Server(host="0.0.0.0", port=5000, use_debugger=True, use_reloader=True)
manager.add_command("runserver", server)
manager.add_command('db', MigrateCommand)


@app.route('/send-email')
def send_mail():
    """Testing sending email through Flask-Mail and the website"""

    try:
        msg = Message("Send Mail Tutorial!",
                      sender="kindtableapp@gmail.com",
                      recipients=["ilsalacious@gmail.com"])
        msg.body = "Yo!\nHave you heard the good word of Python???"
        mail.send(msg)
        return 'Mail sent!'
    except Exception, e:
        return(str(e))


@app.route('/')
def index():
    """Homepage."""

    user_id = session.get("user_id")
    if user_id:
        return redirect("/userprofile")
    else:
        return render_template("kind_homepage.html")


@app.route('/login', methods=['GET'])
def show_login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/logout')
def add_logout():
    """Log out."""

    check_id = session.get("user_id")
    if check_id:
        del session["user_id"]
        flash("Logged Out.", "danger")
        return redirect("/")
    else:
        return redirect("/login")


@app.route('/register', methods=['GET'])
def show_register_form():
    """Show form for user signup."""

    diets = Diet.query.order_by(Diet.diet_type).all()

    return render_template("register_form.html", diets=diets)


@app.route('/userprofile', methods=['GET'])
def show_user_profile():
    """Show logged in user's profile"""

    user_id = session.get("user_id")
    if user_id:
        this_user = User.query.get(user_id)
        diets = Diet.query.order_by(Diet.diet_type).all()
        intol_list = Intolerance.query.order_by(Intolerance.intol_name).all()

        return render_template("/user_profile_page.html",
                               this_user=this_user,
                               intol_list=intol_list,
                               diets=diets)

    else:
        return redirect("/login")


@app.route('/findfriend', methods=['GET'])
def show_get_a_friend():
    """Create a profile for a friend"""

    user_id = session.get("user_id")
    if user_id:
        this_user = User.query.get(user_id)
        return render_template("find_a_friend.html",
                               this_user=this_user)
    else:
        return redirect("/login")


@app.route('/findmanyfriends', methods=['GET'])
def show_get_many_friends():
    """Create a profile for a friend"""

    user_id = session.get("user_id")
    if user_id:
        this_user = User.query.get(user_id)
        return render_template("find_many_friends.html",
                               this_user=this_user)
    else:
        return redirect("/login")


@app.route('/friendprofile/<int:friend_id>', methods=['GET'])
def show_friend_profile(friend_id):
    """Show logged in user's friends profile"""

    check_id = session.get("user_id")
    if check_id:
        this_user = User.query.get(check_id)
        newfriend = User.query.get(friend_id)
        diets = Diet.query.order_by(Diet.diet_type).all()
        intol_list = Intolerance.query.order_by(Intolerance.intol_name).all()
        parties = db.session.query(Party).filter(Party.party_id == PartyGuest.party_id, PartyGuest.user_id == newfriend.user_id).all()
        return render_template("/friends_profile_page.html",
                               newfriend=newfriend,
                               diets=diets,
                               this_user=this_user,
                               intol_list=intol_list,
                               parties=parties
                               )
    else:
        return redirect("/login")


@app.route('/addafriend', methods=['POST'])
def add_a_friend():
    """Add a friend connections to the friends table"""

    user_id = session.get("user_id")
    email_address = request.form.get("email_address")

    if email_address:
        in_database = db.session.query(User).filter(User.email == email_address).first()

        if in_database is not None:
            check_for_friend = db.session.query(Friends).filter(Friends.user_id == user_id, Friends.friend_id == in_database.user_id).first()
            if check_for_friend:
                flash("%s is already one of your friends. Would you like to add someone else?" % email_address, "info")
                return redirect("/findfriend")
            else:
                friend_id = in_database.user_id
                newfriend = Friends(user_id=user_id, friend_id=friend_id)
                db.session.add(newfriend)
                db.session.commit()
                flash("%s is now in your friend's list" % email_address, "success")
                return redirect("/userprofile")
        else:
            make_user(email_address, diet_id=6)
            newfriend = db.session.query(User).filter(User.email == email_address).first()
            make_friendship(user_id, newfriend.user_id)
            flash("This person is not yet in our system. Please update their profile", "info")
            return redirect("/friendprofile/%s" % newfriend.user_id)
    else:
        flash("You need to enter a valid email address", "warning")
        return redirect("/findfriend")


@app.route('/addmanyfriends', methods=['POST'])
def add_many_friends():
    """Add multiple friends connections to the friends table"""

    user_id = session.get("user_id")
    email_address = request.form.get("email_address")

    if email_address:
        in_database = db.session.query(User).filter(User.email == email_address).first()

        if in_database is not None:
            check_for_friend = db.session.query(Friends).filter(Friends.user_id == user_id, Friends.friend_id == in_database.user_id).first()
            if check_for_friend:
                flash("%s is already one of your friends. Would you like to add someone else?" % email_address, "info")
                return redirect("/findmanyfriends")
            else:
                friend_id = in_database.user_id
                newfriend = Friends(user_id=user_id, friend_id=friend_id)
                db.session.add(newfriend)
                db.session.commit()
                flash("%s is now in your friend's list" % email_address, "success")
                return redirect("/findmanyfriends")
        else:
            make_user(email_address, diet_id=6)
            newfriend = db.session.query(User).filter(User.email == email_address).first()
            make_friendship(user_id, newfriend.user_id)
            flash("This new friend is not yet in our system. Please remember to update their profile page.", "info")
            return redirect("/findmanyfriends")
    else:
        flash("Please enter a valid email address", "warning")
        return redirect("/findmanyfriends")


@app.route('/addafriendasguest', methods=['POST'])
def add_a_friend_as_guest():
    """Add a friend connections to the friends table"""

    user_id = session.get("user_id")
    party_id = session.get("party_id")
    email_address = request.form.get("email_address")

    in_database = db.session.query(User).filter(User.email == email_address).first()
    if email_address:
        if in_database is not None:
            check_for_friend = db.session.query(Friends).filter(Friends.user_id == user_id, Friends.friend_id == in_database.user_id).first()
            check_for_guest = db.session.query(PartyGuest).filter(PartyGuest.user_id == in_database.user_id, PartyGuest.party_id == party_id).first()
            if check_for_guest:
                flash("This friend is already guest at this party", "info")
                return redirect('/party_profile/%s' % party_id)
            elif check_for_friend:
                new_guest = PartyGuest(party_id=party_id, user_id=in_database.user_id)
                db.session.add(new_guest)
                db.session.commit()
                flash("%s is already one of your friends but they have now been added as a guest at this party." % email_address, "info")
                return redirect('/party_profile/%s' % party_id)
            else:
                friend_id = in_database.user_id
                make_friendship(user_id, friend_id)
                new_guest = PartyGuest(party_id=party_id, user_id=friend_id)
                db.session.add(new_guest)
                db.session.commit()
                flash("Success! %s is now a guest at this party and added to your friend's list" % email_address, "success")
                return redirect('/party_profile/%s' % party_id)
        else:
            make_user(email_address, diet_id=6)
            newfriend = db.session.query(User).filter(User.email == email_address).first()
            make_friendship(user_id, newfriend.user_id)
            new_guest = PartyGuest(party_id=party_id, user_id=newfriend.user_id)
            db.session.add(new_guest)
            db.session.commit()
            flash("Success! Please add any dietary restrictions by clicking the info button. You can also update any information about your guests by finding them in My Friends from the menu above", "success", )
            return redirect('/party_profile/%s' % party_id)
    else:
            return redirect('/party_profile/%s' % party_id)


@app.route('/update_user_from_party_profile', methods=['POST'])
def change_friend_at_party():
    """Update the friend basic profile at party"""

    party_id = session.get("party_id")
    friend_id = request.form.get("friend_id")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    diet_id = request.form.get("diet_type")
    diet_reason = request.form.get("diet_reason")
    user_change(friend_id, email, first_name, last_name, diet_id, diet_reason)
    flash("Information updated", "success")
    return redirect('/party_profile/%s' % party_id)


@app.route('/update_user', methods=['POST'])
def change_user_basic_info():
    """Update the current users basic profile at party"""

    user_id = session.get("user_id")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    diet_id = request.form.get("diet_type")
    diet_reason = request.form.get("diet_reason")
    user_change(user_id, email, first_name, last_name, diet_id, diet_reason)
    flash("Information updated", "success")
    return redirect('/userprofile')


@app.route('/partyfriendintol', methods=['POST'])
def add_friends_intolerance_from_party():
    """Add a friend intolerance to the their profile from the party page"""

    friend_id = request.form.get("friend_id")
    party_id = session.get("party_id")
    intol_ids = request.form.getlist("intol_ids")
    if intol_ids:
        make_intolerances(friend_id, intol_ids)

    return redirect("/party_profile/%s" % party_id)


@app.route('/partyfriendingredientadded', methods=['POST'])
def add_friends_ingredient_from_party():
    """Add an user's ingredient to avoid to the user profile from the party page"""

    friend_id = request.form.get("friend_id")
    party_id = session.get("party_id")
    ingredient = request.form.get("ingredient")
    if ingredient:
        reason = request.form.get("reason")
        make_avoidance(user_id=friend_id, ingredient=ingredient, reason=reason)

    return redirect("/party_profile/%s" % party_id)


@app.route('/changefrienduserinfo', methods=['POST'])
def add_friend_profile_registered():
    """Instantiate unverified User and make connection on friends table."""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    diet_id = request.form.get("diet_type")
    diet_reason = request.form.get("diet_reason")
    newfriend = db.session.query(User).filter(User.email == email).first()
    user_change(newfriend.user_id, email, first_name, last_name, diet_id, diet_reason)

    flash("Information updated", "success")

    return redirect("/friendprofile/%s" % newfriend.user_id)


@app.route('/party_profile/<int:party_id>')
def show_party_profile(party_id):
    """Show the party profile"""

    user_id = session.get("user_id")
    if user_id:
        session['party_id'] = party_id
        diets = Diet.query.order_by(Diet.diet_type).all()
        this_user = User.query.get(user_id)
        party = Party.query.get(party_id)
        intol_list = Intolerance.query.order_by(Intolerance.intol_name).all()

        return render_template("/party_profile.html", user_id=user_id,
                               party=party,
                               this_user=this_user,
                               diets=diets,
                               intol_list=intol_list)
    else:
        return redirect("/login")


@app.route('/addaparty', methods=['GET'])
def show_party_form():
    """Show the dinner party form"""

    check_id = session.get("user_id")
    if check_id:
        this_user = User.query.get(check_id)
        return render_template("/add_a_party.html", this_user=this_user)
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
        get_avoid = (guest_avoidances(party_id)).split(", ")
        get_intolerance = (guest_intolerances(party_id)).split(", ")
        cuisine_list = Cuisine.query.order_by(Cuisine.cuisine_name).all()
        course_list = Course.query.order_by(Course.course_name).all()
        party_diets = (all_guest_diets(party_id)).split(", ")
        session["diets"] = party_diets
        session["intols"] = get_intolerance
        session["avoids"] = get_avoid

        return render_template("recipe_search.html", party=party,
                               responses=responses,
                               avoids=get_avoid,
                               intols=get_intolerance,
                               this_user=this_user,
                               party_diets=party_diets,
                               cuisine_list=cuisine_list,
                               course_list=course_list,
                               party_avoids=get_avoid,
                               party_intols=get_intolerance,
                               cuisine=25,
                               course=1,
                               newdiets=party_diets)
    else:
        return redirect("/login")


@app.route('/reloadsearchrecipes', methods=["POST"])
def show_re_search_spoonacular():
    """Collate party information, query spoonacular and show results."""

    user_id = session.get("user_id")
    if user_id:
        this_user = User.query.get(user_id)
        party_id = session.get("party_id")
        party = Party.query.get(party_id)
        cuisine = request.form.get("cuisine")
        session["cuisine"] = cuisine
        course = request.form.get("course")
        session["course"] = course
        newdiets = request.form.getlist("diets")
        diets = []
        for each in newdiets:
            diets.append(str(each))
        session["diets"] = diets
        newintols = request.form.getlist("intols")
        intols = []
        for each in newintols:
            intols.append(str(each))
        session["intols"] = intols

        newavoids = request.form.getlist("avoids")
        avoids = []

        for each in newavoids:
            avoids.append(str(each))
        session["avoids"] = avoids

        new_diet = new_guest_diet(newdiets)

        party_diets = (all_guest_diets(party_id)).split(", ")
        responses = new_spoonacular_request(diet=new_diet, intols=intols, avoids=avoids, cuisine=cuisine, course=course)
        # print responses
        get_avoid = guest_avoidances(party_id).split(", ")
        get_intolerance = guest_intolerances(party_id).split(", ")
        # ---------------
        cuisine_list = Cuisine.query.order_by(Cuisine.cuisine_name).all()
        course_list = Course.query.order_by(Course.course_name).all()

        return render_template("recipe_search.html", party=party,
                               responses=responses,
                               this_user=this_user,
                               party_diets=party_diets,
                               cuisine_list=cuisine_list,
                               course_list=course_list,
                               party_avoids=get_avoid,
                               party_intols=get_intolerance,
                               avoids=avoids,
                               intols=intols,
                               cuisine=cuisine,
                               course=course,
                               newdiets=diets)

    else:
        return redirect("/login")


@app.route('/show_recipe/<int:record_id>')
def preview_saved_recipe(record_id):
    """Show a recipe preview of recipes saved in the RecipeBox from the party page"""

    check_id = session.get("user_id")
    if check_id:
        this_user = User.query.get(check_id)
        this_recipe = RecipeBox.query.get(record_id)
        recipe_id = this_recipe.recipe_id
        works_for = json.loads(this_recipe.works_for)
        ingredients = spoonacular_recipe_ingredients(recipe_id)
        instructions = spoonacular_recipe_instructions(recipe_id)
        party = Party.query.get(this_recipe.party_id)

        avoid = guest_avoidances(party.party_id)
        intolerances = guest_intolerances(party.party_id)

        return render_template("recipe_preview.html",
                               this_user=this_user,
                               this_recipe=this_recipe,
                               party=party,
                               avoid=avoid,
                               intolerances=intolerances,
                               works_for=works_for,
                               ingredients=ingredients,
                               instructions=instructions)


@app.route('/recipe/<int:record_id>')
def show_saved_recipe(record_id):
    """Show a recipe saved in the RecipeBox in it's own page, from the recipe preview, on the party page"""

    check_id = session.get("user_id")
    if check_id:
        this_user = User.query.get(check_id)
        this_recipe = RecipeBox.query.get(record_id)
        recipe_id = this_recipe.recipe_id
        works_for = json.loads(this_recipe.works_for)
        ingredients = spoonacular_recipe_ingredients(recipe_id)
        instructions = spoonacular_recipe_instructions(recipe_id)
        party = Party.query.get(this_recipe.party_id)

        avoid = guest_avoidances(party.party_id)
        intolerances = guest_intolerances(party.party_id)
        return render_template("recipe_profile.html",
                               this_user=this_user,
                               this_recipe=this_recipe,
                               party=party,
                               avoid=avoid,
                               intolerances=intolerances,
                               works_for=works_for,
                               ingredients=ingredients,
                               instructions=instructions)


@app.route('/see_recipe', methods=['POST'])
def show_recipe():
    """Preview a recipe not yet saved, from the recipe search page"""

    check_id = session.get("user_id")
    if check_id:
        this_user = User.query.get(check_id)
        party_id = session.get("party_id")
        recipe_id = request.form.get("recipe_id")
        avoids = session.get("avoids")
        intols = session.get("intols")
        cuisine = request.form.get("cuisine")
        course = request.form.get("course")
        newdiets = session.get("diets")
        title = request.form.get("title")
        recipe_image_url = request.form.get("recipe_image_url")
        recipe_url = request.form.get("recipe_url")
        ingredients = spoonacular_recipe_ingredients(recipe_id)
        instructions = spoonacular_recipe_instructions(recipe_id)

        return render_template("view_recipe.html",
                               recipe_id=recipe_id,
                               party_id=party_id,
                               title=title,
                               recipe_image_url=recipe_image_url,
                               recipe_url=recipe_url,
                               this_user=this_user,
                               ingredients=ingredients,
                               instructions=instructions,
                               avoids=avoids,
                               intols=intols,
                               cuisine=cuisine,
                               course=course,
                               newdiets=newdiets)
    else:
        return redirect("/login")


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
    user = User.query.filter_by(email=email).first()
    if user:
        flash("You are already registered here, please log in.", "info")
        return redirect("/login")
    else:
        make_user(email, password, diet_id, first_name, last_name,
                  diet_reason, verified)

        user = User.query.filter_by(email=email).first()
        user_id = user.user_id
        session["user_id"] = user_id

        flash("Welcome to Kind Table, %s." % first_name, "success")
        return redirect("/userprofile")


@app.route('/loggedin', methods=['POST'])
def add_login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if user:
        if user.verify_password(password) is False:
            flash("Incorrect password", "danger")
            return redirect("/login")
        else:
            session["user_id"] = user.user_id
            flash("Logged in", "success")
            return redirect("/userprofile")
    elif not user:
        flash("You seem to be new here. Would you like to register? If not, please check your email address", "info")
        return redirect("/register")


@app.route('/intolerance_added', methods=['POST'])
def add_an_intolerance():
    """Add a user intolerance to the user profile"""

    user_id = session.get("user_id")
    intol_ids = request.form.getlist("intol_ids")
    if intol_ids:
        make_intolerances(user_id, intol_ids)
    else:
        pass
    return redirect("/userprofile")


@app.route('/ingredientadded', methods=['POST'])
def add_an_ingredient():
    """Add an user's ingredient to avoid to the user profile"""

    user_id = session.get("user_id")
    ingredient = request.form.get("ingredient")
    reason = request.form.get("reason")
    if ingredient:
        make_avoidance(user_id, ingredient, reason)
    else:
        pass

    return redirect("/userprofile")


@app.route('/friendintolerance_added', methods=['POST'])
def add_friends_intolerance():
    """Add a friend intolerance to the their profile"""

    friend_id = request.form.get("friend_id")
    intol_ids = request.form.getlist("intol_ids")
    if intol_ids:
        make_intolerances(friend_id, intol_ids)

    return redirect("friendprofile/%s" % friend_id)


@app.route('/friendingredientadded', methods=['POST'])
def add_friends_ingredient():
    """Add an user's ingredient to avoid to the user profile"""

    friend_id = request.form.get("friend_id")
    ingredient = request.form.get("ingredient")
    if ingredient:
        reason = request.form.get("reason")
        make_avoidance(friend_id, ingredient, reason)

    return redirect("friendprofile/%s" % friend_id)


@app.route('/party_added', methods=['POST'])
def add_party():
    """Add a new dinner party to the dinner party table"""

    user_id = session.get("user_id")
    title = request.form.get("title")
    if title:
        new_party = Party(host_id=user_id, title=title)
        db.session.add(new_party)
        db.session.commit()
        party = db.session.query(Party).filter(Party.title == title).first()
        new_guest = PartyGuest(party_id=party.party_id, user_id=user_id)
        db.session.add(new_guest)
        db.session.commit()
        return redirect("/party_profile/%s" % party.party_id)
    else:
        flash("You need to enter a party name", "warning")
        return redirect("/addaparty")


@app.route('/guest_added', methods=['POST'])
def add_guest():
    """Add a guest to a diner party"""

    party_id = request.form.get("party_id")
    guests = request.form.getlist("guests")
    for guest in guests:
        new_guest = PartyGuest(party_id=party_id, user_id=guest)
        db.session.add(new_guest)
        db.session.commit()

    return redirect('/party_profile/' + party_id)


@app.route('/addtorecipebox', methods=['POST'])
def add_recipe_box():
    """Add a recipe to the recipe box"""

    check_id = session.get("user_id")
    party_id = session.get("party_id")
    title = request.form.get("title")

    # Creates the -workfor- json
    party_diets = session.get("diets")
    party_intols = session.get("intols")
    party_avoids = session.get("avoids")
    food_dict = {}
    food_dict["Diets"] = party_diets
    food_dict["Intolerances/Allergies"] = party_intols
    food_dict["Ingredients to omit"] = party_avoids
    food_dump = (json.dumps(food_dict))

    if check_id:
        recipe_id = request.form.get("recipe_id")
        this_recipe = RecipeBox.query.filter(recipe_id == recipe_id).first()
        if this_recipe:
            party_recipe = PartyRecipes.query.filter(recipe_id == recipe_id, party_id == party_id).first()
            if party_recipe:
                flash("This recipe is already saved to your Recipe Box.", "danger")
                return redirect("/searchrecipes")
            else:
                recipe_added = PartyRecipes(party_id=party_id,
                                            recipe_id=recipe_id,
                                            works_for=food_dump)
                db.session.add(recipe_added)
                db.session.commit()
                flash("The recipe for %s has been saved to your recipe box." % title, "success")
                return redirect("/searchrecipes")
        else:
            recipe_image_url = request.form.get("recipe_image_url")
            recipe_url = request.form.get("recipe_url")

            instruction_listA = request.form.get("instructions")
            ingredient_listA = request.form.get("ingredients")
            raise Exception

            instruction_list = []
            for each in instruction_listA:
                instruction_list.append(each)

            ingredient_list = []
            for each in ingredient_listA:
                instruction_list.append(each)

            instructions = {}
            instructions["Instructions"] = instruction_list
            ingredients = {}
            ingredients["Ingredients"] = ingredient_list

            ingredient_dump = (json.dumps(ingredient_list))
            instruction_dump = (json.dumps(instruction_list))

            new_recipe = RecipeBox(party_id=party_id,
                                   recipe_id=recipe_id,
                                   title=title,
                                   recipe_image_url=recipe_image_url,
                                   recipe_url=recipe_url,
                                   ingredients=ingredient_dump,
                                   instruction_dump=instruction_dump)
            db.session.add(new_recipe)
            db.session.commit()
            recipe_added = PartyRecipes(party_id=party_id,
                                        recipe_id=new_recipe.recipe_id,
                                        works_for=food_dump)
            db.session.add(recipe_added)
            db.session.commit()
            flash("The recipe for %s has been saved to your recipe box." % title, "success")
            return redirect("/searchrecipes")
    else:
        return redirect("/login")

# ___________________________________________________________________________

if __name__ == "__main__":

    connect_to_db(app, os.environ.get("DATABASE_URL"))

    #  remove app.debug = True before demoing

    # app.debug = True

    # app.run(host="0.0.0.0")
    
    manager.run()
