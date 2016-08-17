"""Models for K(i)ndTable WebApp."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of K(i)nd website. Guests and hosts are stored in the same table."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=True)
    verified = db.Column(db.Boolean, default=False, nullable=False)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    diet_id = db.Column(db.Integer, db.ForeignKey("diets.diet_id"))
    diet_reason = db.Column(db.String(120), nullable=True)  # ie, ethical, religious, general health, specific health

    avoidances = db.relationship("IngToAvoid", backref=db.backref("users_a"))

    intolerances = db.relationship("Intolerance",
                                   secondary="userintolerances",
                                   backref="users")

    diet = db.relationship('Diet', backref='users')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s  first_name=%s last_name=%s>" % (self.user_id, self.email, self.first_name, self.last_name)


class Friends(db.Model):
    """Makes connections between the user and other users they know"""

    __tablename__ = "friends"

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    users = db.relationship("User", foreign_keys=[user_id], backref="friends")
    friends = db.relationship("User", foreign_keys=[friend_id], backref="users")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Friends record_id=%s user_id=%s  friend_id=%s>" % (self.record_id, self.user_id, self.friend_id)


class UserIntolerance(db.Model):
    """The intolerances that each user has."""

    __tablename__ = "userintolerances"

    user_intol_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    intol_id = db.Column(db.Integer, db.ForeignKey('intolerances.intol_id'), nullable=False)


class Intolerance(db.Model):
    """Spoonacular's list of possible intolerances."""

    __tablename__ = "intolerances"

    intol_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    intol_name = db.Column(db.String(64), nullable=False)
    intol_description = db.Column(db.String(120), nullable=False)  # Spoonacular's criteria for searching

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Intolerances int_id=%s int_name=%s int_description=%s>" % (self.intol_id, self.intol_name, self.intol_description)


class Diet(db.Model):
    """What diet a user follows."""

    __tablename__ = "diets"

    diet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    diet_type = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Diet diet_id=%s diet_type=%s description=%s>" % (self.diet_id, self.diet_type, self.description)


class IngToAvoid(db.Model):
    """Ingredients users would like to avoid."""

    __tablename__ = "avoid"

    avoid_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingredient = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    users = db.relationship('User', backref='ingredients')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<IngToAvoid avoid_id=%s user_id=%s ingredient=%s reason=%s>" % (self.avoid_id, self.user_id, self.ingredient, self.reason)


class PartyGuest(db.Model):
    """Associate users with a party"""

    #  this is a true association table now

    __tablename__ = "party_guests"

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey("parties.party_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)


class Party(db.Model):
    """Create a dinner party to store and link information about a party"""

    __tablename__ = "parties"

    party_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    users = db.relationship("User",
                            secondary="party_guests",
                            backref="parties")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Party party_id=%s title_id=%s host_id=%s>" % (self.party_id, self.title, self.host_id)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///kind'
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
