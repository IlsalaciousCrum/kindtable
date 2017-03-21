"""K(i)nd app views"""


from datetime import datetime
from flask import render_template, request, flash, redirect, session, json, url_for
from flask_moment import Moment
from . import main

# commented out because I have not made my forms yet, NameForm is a placeholder name, not a real form
# from .forms import NameForm

from app.models import User, Profile, Friend, ProfileIntolerance, Intolerance, Diet, Cuisine, Course, IngToAvoid, PartyGuest, Party, RecipeCard, RecipeBox, PartyRecipes
from .. import db
from flask_mail import Mail, Message
from flask_login import login_required


@main.route('/send-email')
def send_mail():
    """Testing sending email through Flask-Mail and the website"""

    try:
        msg = Message("Ilsa has sent you a Kind Table Request!",
                      recipients=["ilsalacious@gmail.com"])
        msg.body = "Ilsa (ilsalacious@gmail.com) would like you to fill out a brief dietary preference profile to make cooking for you easier."
        Mail.send(msg)
        return 'Mail sent!'
    except Exception, e:
        return(str(e))


# I got ahead of myself. Will have to wait until it's ready to deploy to add SSL.

# @main.route('/.well-known/acme-challenge/BopKRv96R-TjYAFzlJLgNzplFkgAFbD3Oqp3Ge4L5O8')
# def letsencryptSSL():
#     """Acme challenge for Let's Encrypt TLS certificate"""

#     html = "<html><body>BopKRv96R-TjYAFzlJLgNzplFkgAFbD3Oqp3Ge4L5O8.ecIxhAtF13SyMysgf2q8wrMZCcfF9-XUpp2Mpj1Wefk</body></html>"
#     return html


@main.route('/')
def index():
    """Homepage."""

    try:
        session_token = session.get("session_token")
        user = User.query.filter(session_token=session_token).first()
        if user:
            friends = user.friends
            parties = user.parties
            return render_template("kind_homepage.html", friends=friends, parties=parties)
    except:
        return render_template("kind_homepage.html", friends="", parties="")


@main.route('/userprofile', methods=['GET'])
@login_required
def show_user_profile():
    """Show logged in user's profile"""

    session_token = session.get("session_token")
    user = User.query.filter(session_token == session_token).first()
    if user:
        friends = user.friends
        parties = user.parties
    profile = db.session.query(Profile).filter(User.profile_id == Profile.owned_by_user_id, User.session_token == session_token).first()
    if profile:
        diets = Diet.query.order_by(Diet.diet_type).all()
        intol_list = Intolerance.query.order_by(Intolerance.intol_name).all()

        return render_template("/template/mixins/identity_and_diet_profile.html",
                               friends=friends,
                               parties=parties,
                               profile=profile,
                               intol_list=intol_list,
                               diets=diets)


# @main.route('/findfriend', methods=['GET'])
# @login_required
# def show_get_a_friend():
#     """Create a profile for a friend"""

#     user_id = session.get("user_id")
#     if user_id:
#         this_user = User.query.get(user_id)
#         return render_template("find_a_friend.html",
#                                this_user=this_user)
#     else:
#         return redirect("/login")


# @main.route('/findmanyfriends', methods=['GET'])
# @login_required
# def show_get_many_friends():
#     """Create a profile for a friend"""

#     user_id = session.get("user_id")
#     if user_id:
#         this_user = User.query.get(user_id)
#         return render_template("find_many_friends.html",
#                                this_user=this_user)
#     else:
#         return redirect("/login")


@main.route('/friendprofile/<int:friend_id>', methods=['GET'])
@login_required
def show_friend_profile(friend_id):
    """Show logged in user's friends profile"""

    session_token = session.get("session_token")
    user = User.query.filter_by(session_token=session_token).first()
    friends = user.friends
    parties = user.parties

    newfriend = Profile.query.get(friend_id)
    diets = Diet.query.order_by(Diet.diet_type).all()
    intol_list = Intolerance.query.order_by(Intolerance.intol_name).all()
    parties = db.session.query(Party).filter(Party.party_id == PartyGuest.party_id, PartyGuest.profile_id == newfriend.profile_id).all()
    return render_template("/friends_profile_page.html",
                           newfriend=newfriend,
                           diets=diets,
                           intol_list=intol_list,
                           parties=parties,
                           friends=friends
                           )


# @main.route('/addafriend', methods=['POST'])
# @login_required
# def add_a_friend():
#     """Add a friend connections to the friends table"""

#     user_id = session.get("user_id")
#     email_address = request.form.get("email_address")

#     if email_address:
#         in_database = db.session.query(User).filter(User.email == email_address).first()

#         if in_database is not None:
#             check_for_friend = db.session.query(Friends).filter(Friends.user_id == user_id, Friends.friend_id == in_database.user_id).first()
#             if check_for_friend:
#                 flash("%s is already one of your friends. Would you like to add someone else?" % email_address, "info")
#                 return redirect("/findfriend")
#             else:
#                 friend_id = in_database.user_id
#                 newfriend = Friends(user_id=user_id, friend_id=friend_id)
#                 db.session.add(newfriend)
#                 db.session.commit()
#                 flash("%s is now in your friend's list" % email_address, "success")
#                 return redirect("/userprofile")
#         else:
#             make_user(email_address, diet_id=6)
#             newfriend = db.session.query(User).filter(User.email == email_address).first()
#             make_friendship(user_id, newfriend.user_id)
#             flash("This person is not yet in our system. Please update their profile", "info")
#             return redirect("/friendprofile/%s" % newfriend.user_id)
#     else:
#         flash("You need to enter a valid email address", "warning")
#         return redirect("/findfriend")


# @main.route('/addmanyfriends', methods=['POST'])
# @login_required
# def add_many_friends():
#     """Add multiple friends connections to the friends table"""

#     user_id = session.get("user_id")
#     email_address = request.form.get("email_address")

#     if email_address:
#         in_database = db.session.query(User).filter(User.email == email_address).first()

#         if in_database is not None:
#             check_for_friend = db.session.query(Friends).filter(Friends.user_id == user_id, Friends.friend_id == in_database.user_id).first()
#             if check_for_friend:
#                 flash("%s is already one of your friends. Would you like to add someone else?" % email_address, "info")
#                 return redirect("/findmanyfriends")
#             else:
#                 friend_id = in_database.user_id
#                 newfriend = Friends(user_id=user_id, friend_id=friend_id)
#                 db.session.add(newfriend)
#                 db.session.commit()
#                 flash("%s is now in your friend's list" % email_address, "success")
#                 return redirect("/findmanyfriends")
#         else:
#             make_user(email_address, diet_id=6)
#             newfriend = db.session.query(User).filter(User.email == email_address).first()
#             make_friendship(user_id, newfriend.user_id)
#             flash("This new friend is not yet in our system. Please remember to update their profile page.", "info")
#             return redirect("/findmanyfriends")
#     else:
#         flash("Please enter a valid email address", "warning")
#         return redirect("/findmanyfriends")


# @main.route('/addafriendasguest', methods=['POST'])
# @login_required
# def add_a_friend_as_guest():
#     """Add a friend connections to the friends table"""

#     user_id = session.get("user_id")
#     party_id = session.get("party_id")
#     email_address = request.form.get("email_address")

#     in_database = db.session.query(User).filter(User.email == email_address).first()
#     if email_address:
#         if in_database is not None:
#             check_for_friend = db.session.query(Friends).filter(Friends.user_id == user_id, Friends.friend_id == in_database.user_id).first()
#             check_for_guest = db.session.query(PartyGuest).filter(PartyGuest.user_id == in_database.user_id, PartyGuest.party_id == party_id).first()
#             if check_for_guest:
#                 flash("This friend is already guest at this party", "info")
#                 return redirect('/party_profile/%s' % party_id)
#             elif check_for_friend:
#                 new_guest = PartyGuest(party_id=party_id, user_id=in_database.user_id)
#                 db.session.add(new_guest)
#                 db.session.commit()
#                 flash("%s is already one of your friends but they have now been added as a guest at this party." % email_address, "info")
#                 return redirect('/party_profile/%s' % party_id)
#             else:
#                 friend_id = in_database.user_id
#                 make_friendship(user_id, friend_id)
#                 new_guest = PartyGuest(party_id=party_id, user_id=friend_id)
#                 db.session.add(new_guest)
#                 db.session.commit()
#                 flash("Success! %s is now a guest at this party and added to your friend's list" % email_address, "success")
#                 return redirect('/party_profile/%s' % party_id)
#         else:
#             make_user(email_address, diet_id=6)
#             newfriend = db.session.query(User).filter(User.email == email_address).first()
#             make_friendship(user_id, newfriend.user_id)
#             new_guest = PartyGuest(party_id=party_id, user_id=newfriend.user_id)
#             db.session.add(new_guest)
#             db.session.commit()
#             flash("Success! Please add any dietary restrictions by clicking the info button. You can also update any information about your guests by finding them in My Friends from the menu above", "success", )
#             return redirect('/party_profile/%s' % party_id)
#     else:
#             return redirect('/party_profile/%s' % party_id)


# @main.route('/update_user_from_party_profile', methods=['POST'])
# @login_required
# def change_friend_at_party():
#     """Update the friend basic profile at party"""

#     party_id = session.get("party_id")
#     friend_id = request.form.get("friend_id")
#     first_name = request.form.get("first_name")
#     last_name = request.form.get("last_name")
#     email = request.form.get("email")
#     diet_id = request.form.get("diet_type")
#     diet_reason = request.form.get("diet_reason")
#     user_change(friend_id, email, first_name, last_name, diet_id, diet_reason)
#     flash("Information updated", "success")
#     return redirect('/party_profile/%s' % party_id)


# @main.route('/update_user', methods=['POST'])
# @login_required
# def change_user_basic_info():
#     """Update the current users basic profile at party"""

#     user_id = session.get("user_id")
#     first_name = request.form.get("first_name")
#     last_name = request.form.get("last_name")
#     email = request.form.get("email")
#     diet_id = request.form.get("diet_type")
#     diet_reason = request.form.get("diet_reason")
#     user_change(user_id, email, first_name, last_name, diet_id, diet_reason)
#     flash("Information updated", "success")
#     return redirect('/userprofile')


# @main.route('/partyfriendintol', methods=['POST'])
# @login_required
# def add_friends_intolerance_from_party():
#     """Add a friend intolerance to the their profile from the party page"""

#     friend_id = request.form.get("friend_id")
#     party_id = session.get("party_id")
#     intol_ids = request.form.getlist("intol_ids")
#     if intol_ids:
#         make_intolerances(friend_id, intol_ids)

#     return redirect("/party_profile/%s" % party_id)


# @main.route('/partyfriendingredientadded', methods=['POST'])
# @login_required
# def add_friends_ingredient_from_party():
#     """Add an user's ingredient to avoid to the user profile from the party page"""

#     friend_id = request.form.get("friend_id")
#     party_id = session.get("party_id")
#     ingredient = request.form.get("ingredient")
#     if ingredient:
#         reason = request.form.get("reason")
#         make_avoidance(user_id=friend_id, ingredient=ingredient, reason=reason)

#     return redirect("/party_profile/%s" % party_id)


# @main.route('/changefrienduserinfo', methods=['POST'])
# @login_required
# def add_friend_profile_registered():
#     """Instantiate unverified User and make connection on friends table."""

#     first_name = request.form.get("first_name")
#     last_name = request.form.get("last_name")
#     email = request.form.get("email")
#     diet_id = request.form.get("diet_type")
#     diet_reason = request.form.get("diet_reason")
#     newfriend = db.session.query(User).filter(User.email == email).first()
#     user_change(newfriend.user_id, email, first_name, last_name, diet_id, diet_reason)

#     flash("Information updated", "success")

#     return redirect("/friendprofile/%s" % newfriend.user_id)


@main.route('/party_profile/<int:party_id>')
@login_required
def show_party_profile(party_id):
    """Show the party profile"""

    session_token = session.get("session_token")
    user = User.query.filter_by(session_token=session_token).first()
    this_user = user.profile
    friends = user.friends
    parties = user.parties
    session['party_id'] = party_id
    diets = Diet.query.order_by(Diet.diet_type).all()
    party = Party.query.get(party_id)
    intol_list = Intolerance.query.order_by(Intolerance.intol_name).all()

    return render_template("/party_profile.html", party=party,
                           this_user=this_user,
                           diets=diets,
                           intol_list=intol_list,
                           friends=friends,
                           parties=parties)


# @main.route('/addaparty', methods=['GET'])
# @login_required
# def show_party_form():
#     """Show the dinner party form"""

#     check_id = session.get("user_id")
#     if check_id:
#         this_user = User.query.get(check_id)
#         return render_template("/add_a_party.html", this_user=this_user)
#     else:
#         return redirect("/login")


# @main.route('/searchrecipes')
# @login_required
# def show_search_spoonacular():
#     """Collate party information, query spoonacular and show results."""

#     user_id = session.get("user_id")
#     if user_id:
#         this_user = User.query.get(user_id)
#         party_id = session.get("party_id")
#         party = Party.query.get(party_id)
#         responses = spoonacular_request(party_id)
#         get_avoid = (guest_avoidances(party_id)).split(", ")
#         get_intolerance = (guest_intolerances(party_id)).split(", ")
#         cuisine_list = Cuisine.query.order_by(Cuisine.cuisine_name).all()
#         course_list = Course.query.order_by(Course.course_name).all()
#         party_diets = (all_guest_diets(party_id)).split(", ")
#         session["diets"] = party_diets
#         session["intols"] = get_intolerance
#         session["avoids"] = get_avoid

#         return render_template("recipe_search.html", party=party,
#                                responses=responses,
#                                avoids=get_avoid,
#                                intols=get_intolerance,
#                                this_user=this_user,
#                                party_diets=party_diets,
#                                cuisine_list=cuisine_list,
#                                course_list=course_list,
#                                party_avoids=get_avoid,
#                                party_intols=get_intolerance,
#                                cuisine=25,
#                                course=1,
#                                newdiets=party_diets)
#     else:
#         return redirect("/login")


# @main.route('/reloadsearchrecipes', methods=["POST"])
# @login_required
# def show_re_search_spoonacular():
#     """Collate party information, query spoonacular and show results."""

#     user_id = session.get("user_id")
#     if user_id:
#         this_user = User.query.get(user_id)
#         party_id = session.get("party_id")
#         party = Party.query.get(party_id)
#         cuisine = request.form.get("cuisine")
#         session["cuisine"] = cuisine
#         course = request.form.get("course")
#         session["course"] = course
#         newdiets = request.form.getlist("diets")
#         diets = []
#         for each in newdiets:
#             diets.append(str(each))
#         session["diets"] = diets
#         newintols = request.form.getlist("intols")
#         intols = []
#         for each in newintols:
#             intols.append(str(each))
#         session["intols"] = intols

#         newavoids = request.form.getlist("avoids")
#         avoids = []

#         for each in newavoids:
#             avoids.append(str(each))
#         session["avoids"] = avoids

#         new_diet = new_guest_diet(newdiets)

#         party_diets = (all_guest_diets(party_id)).split(", ")
#         responses = new_spoonacular_request(diet=new_diet, intols=intols, avoids=avoids, cuisine=cuisine, course=course)
#         # print responses
#         get_avoid = guest_avoidances(party_id).split(", ")
#         get_intolerance = guest_intolerances(party_id).split(", ")
#         # ---------------
#         cuisine_list = Cuisine.query.order_by(Cuisine.cuisine_name).all()
#         course_list = Course.query.order_by(Course.course_name).all()

#         return render_template("recipe_search.html", party=party,
#                                responses=responses,
#                                this_user=this_user,
#                                party_diets=party_diets,
#                                cuisine_list=cuisine_list,
#                                course_list=course_list,
#                                party_avoids=get_avoid,
#                                party_intols=get_intolerance,
#                                avoids=avoids,
#                                intols=intols,
#                                cuisine=cuisine,
#                                course=course,
#                                newdiets=diets)

#     else:
#         return redirect("/login")


# @main.route('/show_recipe/<int:record_id>')
# @login_required
# def preview_saved_recipe(record_id):
#     """Show a recipe preview of recipes saved in the RecipeBox from the party page"""

#     check_id = session.get("user_id")
#     if check_id:
#         this_user = User.query.get(check_id)
#         this_recipe = RecipeBox.query.get(record_id)
#         recipe_id = this_recipe.recipe_id
#         works_for = json.loads(this_recipe.works_for)
#         ingredients = spoonacular_recipe_ingredients(recipe_id)
#         instructions = spoonacular_recipe_instructions(recipe_id)
#         party = Party.query.get(this_recipe.party_id)

#         avoid = guest_avoidances(party.party_id)
#         intolerances = guest_intolerances(party.party_id)

#         return render_template("recipe_preview.html",
#                                this_user=this_user,
#                                this_recipe=this_recipe,
#                                party=party,
#                                avoid=avoid,
#                                intolerances=intolerances,
#                                works_for=works_for,
#                                ingredients=ingredients,
#                                instructions=instructions)


# @main.route('/recipe/<int:record_id>')
# @login_required
# def show_saved_recipe(record_id):
#     """Show a recipe saved in the RecipeBox in it's own page, from the recipe preview, on the party page"""

#     check_id = session.get("user_id")
#     if check_id:
#         this_user = User.query.get(check_id)
#         this_recipe = RecipeBox.query.get(record_id)
#         recipe_id = this_recipe.recipe_id
#         works_for = json.loads(this_recipe.works_for)
#         ingredients = spoonacular_recipe_ingredients(recipe_id)
#         instructions = spoonacular_recipe_instructions(recipe_id)
#         party = Party.query.get(this_recipe.party_id)

#         avoid = guest_avoidances(party.party_id)
#         intolerances = guest_intolerances(party.party_id)
#         return render_template("recipe_profile.html",
#                                this_user=this_user,
#                                this_recipe=this_recipe,
#                                party=party,
#                                avoid=avoid,
#                                intolerances=intolerances,
#                                works_for=works_for,
#                                ingredients=ingredients,
#                                instructions=instructions)


# @main.route('/see_recipe', methods=['POST'])
# @login_required
# def show_recipe():
#     """Preview a recipe not yet saved, from the recipe search page"""

#     check_id = session.get("user_id")
#     if check_id:
#         this_user = User.query.get(check_id)
#         party_id = session.get("party_id")
#         recipe_id = request.form.get("recipe_id")
#         avoids = session.get("avoids")
#         intols = session.get("intols")
#         cuisine = request.form.get("cuisine")
#         course = request.form.get("course")
#         newdiets = session.get("diets")
#         title = request.form.get("title")
#         recipe_image_url = request.form.get("recipe_image_url")
#         recipe_url = request.form.get("recipe_url")
#         ingredients = spoonacular_recipe_ingredients(recipe_id)
#         instructions = spoonacular_recipe_instructions(recipe_id)

#         return render_template("view_recipe.html",
#                                recipe_id=recipe_id,
#                                party_id=party_id,
#                                title=title,
#                                recipe_image_url=recipe_image_url,
#                                recipe_url=recipe_url,
#                                this_user=this_user,
#                                ingredients=ingredients,
#                                instructions=instructions,
#                                avoids=avoids,
#                                intols=intols,
#                                cuisine=cuisine,
#                                course=course,
#                                newdiets=newdiets)
#     else:
#         return redirect("/login")



# @main.route('/intolerance_added', methods=['POST'])
# @login_required
# def add_an_intolerance():
#     """Add a user intolerance to the user profile"""

#     user_id = session.get("user_id")
#     intol_ids = request.form.getlist("intol_ids")
#     if intol_ids:
#         make_intolerances(user_id, intol_ids)
#     else:
#         pass
#     return redirect("/userprofile")


# @main.route('/ingredientadded', methods=['POST'])
# @login_required
# def add_an_ingredient():
#     """Add an user's ingredient to avoid to the user profile"""

#     user_id = session.get("user_id")
#     ingredient = request.form.get("ingredient")
#     reason = request.form.get("reason")
#     if ingredient:
#         make_avoidance(user_id, ingredient, reason)
#     else:
#         pass

#     return redirect("/userprofile")


# @main.route('/friendintolerance_added', methods=['POST'])
# @login_required
# def add_friends_intolerance():
#     """Add a friend intolerance to the their profile"""

#     friend_id = request.form.get("friend_id")
#     intol_ids = request.form.getlist("intol_ids")
#     if intol_ids:
#         make_intolerances(friend_id, intol_ids)

#     return redirect("friendprofile/%s" % friend_id)


# @main.route('/friendingredientadded', methods=['POST'])
# @login_required
# def add_friends_ingredient():
#     """Add an user's ingredient to avoid to the user profile"""

#     friend_id = request.form.get("friend_id")
#     ingredient = request.form.get("ingredient")
#     if ingredient:
#         reason = request.form.get("reason")
#         make_avoidance(friend_id, ingredient, reason)

#     return redirect("friendprofile/%s" % friend_id)


# @main.route('/party_added', methods=['POST'])
# @login_required
# def add_party():
#     """Add a new dinner party to the dinner party table"""

#     user_id = session.get("user_id")
#     title = request.form.get("title")
#     if title:
#         new_party = Party(host_id=user_id, title=title)
#         db.session.add(new_party)
#         db.session.commit()
#         party = db.session.query(Party).filter(Party.title == title).first()
#         new_guest = PartyGuest(party_id=party.party_id, user_id=user_id)
#         db.session.add(new_guest)
#         db.session.commit()
#         return redirect("/party_profile/%s" % party.party_id)
#     else:
#         flash("You need to enter a party name", "warning")
#         return redirect("/addaparty")


# @main.route('/guest_added', methods=['POST'])
# @login_required
# def add_guest():
#     """Add a guest to a diner party"""

#     party_id = request.form.get("party_id")
#     guests = request.form.getlist("guests")
#     for guest in guests:
#         new_guest = PartyGuest(party_id=party_id, user_id=guest)
#         db.session.add(new_guest)
#         db.session.commit()

#     return redirect('/party_profile/' + party_id)


# @main.route('/addtorecipebox', methods=['POST'])
# @login_required
# def add_recipe_box():
#     """Add a recipe to the recipe box"""

#     check_id = session.get("user_id")
#     party_id = session.get("party_id")
#     title = request.form.get("title")

#     # Creates the -workfor- json
#     party_diets = session.get("diets")
#     party_intols = session.get("intols")
#     party_avoids = session.get("avoids")
#     food_dict = {}
#     food_dict["Diets"] = party_diets
#     food_dict["Intolerances/Allergies"] = party_intols
#     food_dict["Ingredients to omit"] = party_avoids
#     food_dump = (json.dumps(food_dict))

#     if check_id:
#         recipe_id = request.form.get("recipe_id")
#         this_recipe = RecipeBox.query.filter(recipe_id == recipe_id).first()
#         if this_recipe:
#             party_recipe = PartyRecipes.query.filter(recipe_id == recipe_id, party_id == party_id).first()
#             if party_recipe:
#                 flash("This recipe is already saved to your Recipe Box.", "danger")
#                 return redirect("/searchrecipes")
#             else:
#                 recipe_added = PartyRecipes(party_id=party_id,
#                                             recipe_id=recipe_id,
#                                             works_for=food_dump)
#                 db.session.add(recipe_added)
#                 db.session.commit()
#                 flash("The recipe for %s has been saved to your recipe box." % title, "success")
#                 return redirect("/searchrecipes")
#         else:
#             recipe_image_url = request.form.get("recipe_image_url")
#             recipe_url = request.form.get("recipe_url")

#             instruction_listA = request.form.get("instructions")
#             ingredient_listA = request.form.get("ingredients")
#             raise Exception

#             instruction_list = []
#             for each in instruction_listA:
#                 instruction_list.append(each)

#             ingredient_list = []
#             for each in ingredient_listA:
#                 instruction_list.append(each)

#             instructions = {}
#             instructions["Instructions"] = instruction_list
#             ingredients = {}
#             ingredients["Ingredients"] = ingredient_list

#             ingredient_dump = (json.dumps(ingredient_list))
#             instruction_dump = (json.dumps(instruction_list))

#             new_recipe = RecipeBox(party_id=party_id,
#                                    recipe_id=recipe_id,
#                                    title=title,
#                                    recipe_image_url=recipe_image_url,
#                                    recipe_url=recipe_url,
#                                    ingredients=ingredient_dump,
#                                    instruction_dump=instruction_dump)
#             db.session.add(new_recipe)
#             db.session.commit()
#             recipe_added = PartyRecipes(party_id=party_id,
#                                         recipe_id=new_recipe.recipe_id,
#                                         works_for=food_dump)
#             db.session.add(recipe_added)
#             db.session.commit()
#             flash("The recipe for %s has been saved to your recipe box." % title, "success")
#             return redirect("/searchrecipes")
#     else:
#         return redirect("/login")
