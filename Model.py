"""Models for K(i)ndTable WebApp."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of K(i)nd website. Guests and hosts are stored in the same table."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    preferred_com = ********* Should this be another table?
    dairy = db.Column(db.Boolean)
    egg = db.Column(db.Boolean)
    gluten = db.Column(db.Boolean)
    peanut = db.Column(db.Boolean)
    sesame = db.Column(db.Boolean)
    seafood = db.Column(db.Boolean)
    shellfish = db.Column(db.Boolean)
    soy = db.Column(db.Boolean)
    diet_id = db.Column(db.Integer, ForeignKey("diets.diet_id")

    # def __repr__(self):
    #     """Provide helpful representation when printed."""

    #     return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class Diet(db.Model):
    """What diet a user follows."""

    __tablename__ = "diets"

    diet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    diet_type = db.Column(db.String(64))
    description = db.Column(db.String(120))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Diet diet_id=%s diet_type=%s description=%s>" % (self.diet_id, self.diet_type)


class IngToAvoid(db.Model):
    """Ingredients users would like to avoid."""

    __tablename__ = "avoid"

    avoid_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("users.user_id"))
    ingredient = db.Column(db.String(100))
    reason = db.Column(db.String(200))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<IngToAvoid avoid_id=%s user_id=%s ingredient=%s reason=%s>" % (self.avoid_id, self.user_id, self.ingredient, self.reason)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
