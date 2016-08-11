"""Utility file to store query functions"""

from sqlalchemy import func

from Model import connect_to_db, db, User, UserIntolerance, Intolerance, Diet, IngToAvoid, PartyGuest, Party
from server import app


def guest_diets(partyid):
    """Query that gets the diet of each guest coming to the party"""

    diet_list = []
    hostparty = Party.query.filter(Party.party_id == partyid).first()
    party_guests = hostparty.users

    for guest in party_guests:
        f = guest.user_id
        eachguest = User.query.filter(User.user_id == f).first()
        eachdiet = eachguest.diet
        diet_list.append(eachdiet.diet_type)
    return diet_list


def guest_avoidances(partyid):
    """Query that gets the avoidances of each guest coming to the party"""

    avoidance_list = []
    hostparty = Party.query.filter(Party.party_id == partyid).first()
    party_guests = hostparty.users

    for guest in party_guests:
        f = guest.user_id
        person = User.query.filter_by(user_id=f).one()
        person_avoidances = person.avoidances
        for each in person_avoidances:
            avoidance_list.append(each.ingredient)
    return avoidance_list


def guest_intolerances(partyid):
    """Query that gets the avoidances of each guest coming to the party"""

    intolerance_list = []
    hostparty = Party.query.filter(Party.party_id == partyid).first()
    party_guests = hostparty.users

    for guest in party_guests:
        f = guest.user_id
        person = User.query.filter_by(user_id=f).one()
        person_intolerances = person.intolerances
        for each in person_intolerances:
            intolerance_list.append(each.intol_name)
    return intolerance_list


def AllUserFoodInfo():
    """show food info for all users for testing purposes"""

    users = User.query.all()

    for user in users:
        print user.user_id
        print user.username
        print user.avoidances
        print user.intolerances
        print user.diet

    return

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
