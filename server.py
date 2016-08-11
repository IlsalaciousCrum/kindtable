"""K(i)nd app"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from Model import connect_to_db, db, User, UserIntolerance, Intolerance, Diet, IngToAvoid, Party, PartyGuest

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


# @app.route('/')
# def index():
#     """Homepage."""

#     return render_template("homepage.html")


# @app.route('/register', methods=['GET'])
# def register_form():
#     """Show form for user signup."""

#     return render_template("register_form.html")


# @app.route('/register', methods=['POST'])
# def register_process():
#     """Process registration."""

#     # Get form variables
#     email = request.form["email"]
#     password = request.form["password"]

#     new_user = User(email=email, password=password, )

#     db.session.add(new_user)
#     db.session.commit()

#     flash("User %s added." % email)
#     return redirect("/users/%s" % new_user.user_id)


# @app.route('/login', methods=['GET'])
# def login_form():
#     """Show login form."""

#     return render_template("login_form.html")


# @app.route('/login', methods=['POST'])
# def login_process():
#     """Process login."""

#     # Get form variables
#     email = request.form["email"]
#     password = request.form["password"]

#     user = User.query.filter_by(email=email).first()

#     if not user:
#         flash("No such user")
#         return redirect("/login")

#     if user.password != password:
#         flash("Incorrect password")
#         return redirect("/login")

#     session["user_id"] = user.user_id

#     flash("Logged in")
#     return redirect("/users/%s" % user.user_id)


# @app.route('/logout')
# def logout():
#     """Log out."""

#     del session["user_id"]
#     flash("Logged Out.")
#     return redirect("/")


# @app.route("/users")
# def user_list():
#     """Show list of users."""

#     users = User.query.all()
#     return render_template("user_list.html", users=users)


# @app.route("/users/<int:user_id>")
# def user_detail(user_id):
#     """Show info about user."""

#     user = User.query.get(user_id)
#     return render_template("user.html", user=user)


# @app.route("/movies")
# def movie_list():
#     """Show list of movies."""

#     movies = Movie.query.order_by('title').all()
#     return render_template("movie_list.html", movies=movies)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
