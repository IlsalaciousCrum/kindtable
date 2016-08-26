"""Utility file to store query functions"""

from sqlalchemy import func

from Model import connect_to_db, db, User, UserIntolerance, Intolerance, Diet, IngToAvoid, PartyGuest, Party
from server import app


def guest_diets(partyid):
    """Query that gets the diet of each guest coming to the party"""

    diet_set = set()
    hostparty = Party.query.get(partyid)
    party_guests = hostparty.users

    for guest in party_guests:
        diet = guest.diet
        diet_set.add(diet.diet_type)
    return diet_set


def guest_avoidances(partyid):
    """Query that gets the avoidances of each guest coming to the party"""

    avoidance_set = set()
    hostparty = Party.query.get(partyid)
    party_guests = hostparty.users

    for guest in party_guests:
        avoids = guest.avoidances
        for each in avoids:
            avoidance_set.add(each.ingredient)
    return avoidance_set


def guest_intolerances(partyid):
    """Query that gets the avoidances of each guest coming to the party"""

    intolerance_set = set()
    hostparty = Party.query.get(partyid)
    party_guests = hostparty.users

    for guest in party_guests:
        f = guest.user_id
        person = User.query.get(f)
        person_intolerances = person.intolerances  # this is where it goes awry
        for each in person_intolerances:
            intolerance_set.add(each.intol_name)
    return intolerance_set


############################################################################

# Views for testing that SQLAlchemy functions are working correctly


# CREATE VIEW user_intolerances AS
# SELECT users.user_id, users.username, intolerances.intol_name
# FROM userintolerances
# JOIN users ON users.user_id = userintolerances.user_id
# JOIN intolerances ON userintolerances.intol_id = intolerances.intol_id
# ORDER BY users.user_id;


# CREATE VIEW partyavoids AS
# SELECT partyguests.party_id, partyguests.title, partyguests.user_id, partyguests.username, user_avoidances.ingredient
# FROM partyguests
# # JOIN user_avoidances on partyguests.user_id = user_avoidances.user_id;

# CREATE VIEW partydiets AS
# SELECT partyguests.party_id, partyguests.title, partyguests.user_id, partyguests.username, user_diets.diet_type
# FROM partyguests
# JOIN user_diets on partyguests.user_id = user_diets.user_id;


# CREATE VIEW partyintolerances AS
# SELECT partyguests.party_id, partyguests.title, partyguests.user_id, partyguests.username, user_intolerances.intol_name
# FROM partyguests
# JOIN user_intolerances on partyguests.user_id = user_intolerances.user_id;



# CREATE VIEW User_Diets AS SELECT user_id, username, diets.diet_type
# FROM users
#   JOIN diets
#     ON users.diet_id = diets.diet_id
#     ORDER BY user_id;


# CREATE VIEW User_Intolerances AS SELECT user_id, username, diets.diet_type
# FROM users
#   JOIN diets
#     ON users.diet_id = diets.diet_id
#     ORDER BY user_id;



# CREATE VIEW User_Diets AS SELECT user_id, username, diets.diet_type
# FROM users
#   JOIN diets
#     ON users.diet_id = diets.diet_id
#     ORDER BY user_id;

# CREATE VIEW user_avoidances AS SELECT users.user_id, users.username, avoid.ingredient
# FROM users
#   JOIN avoid
#     ON users.user_id = avoid.user_id
#      ORDER BY users.user_id;


# CREATE VIEW partyguests AS
# SELECT parties.party_id, parties.title, users.user_id, users.username
# FROM party_guests
# JOIN users ON users.user_id = party_guests.user_id
# JOIN parties ON parties.party_id = party_guests.party_id
# ORDER BY parties.party_id;






#############################################################################


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
