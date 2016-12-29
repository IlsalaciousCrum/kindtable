'''Models for K(i)ndTable WebApp.'''
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from passlib.hash import bcrypt

# from seed import load_testdata

db = SQLAlchemy()

##############################################################################
# Model definitions


class User(db.Model):
    '''Registered users of KindTable WebApp.'''

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'), nullable=False)
    _password = db.Column(db.String(128))
    email_verified = db.Column(db.Boolean, unique=False, default=False)

    parties = db.relationship('Party')
    friend_profiles = db.relationship('Profile',
                                      secondary='friends')

    saved_recipes = db.relationship('RecipeCard',
                                    secondary='recipebox',
                                    backref='users')

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        """Encrypts a password for the user table."""

        h = bcrypt.encrypt(plaintext)
        self._password = h

    def verify_password(self, password):
        """Verifies a password from the user table."""

        if bcrypt.verify(password, self._password) is True:
            return True
        else:
            return False

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<User user_id=%s profile_id=%s validated=%s>' % (self.user_id, self.profile_id, self.validated)


class Profile(db.Model):
    '''Information about users and their contacts'''

    __tablename__ = 'profiles'

    profile_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    is_user_profile = db.Column(db.Boolean, unique=False, default=False)
    email = db.Column(db.String(200), nullable=False, unique=False)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    diet_id = db.Column(db.Integer, db.ForeignKey('diets.diet_id'))
    diet_reason = db.Column(db.String(120), nullable=True)  # ie, ethical, religious, general health, specific health
    profile_notes = db.Column(db.String(300), nullable=True)
    last_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    diet = db.relationship('Diet', backref='profiles')

    avoidances = db.relationship('IngToAvoid', backref='profiles')

    intolerances = db.relationship('Intolerance',
                                   secondary='userintolerances',
                                   backref='profiles')

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Profile profile_id=%s user_id=%s user_id=%s is_user_profile=%s email=%s first_name=%s last_name=%s diet_id=%s diet_reason=%s>' % (self.profile_id, self.user_id, self.is_user_profile, self.email, self.first_name, self.last_name, self.diet_id, self.diet_reason)


class Friend(db.Model):
    '''Makes connection between the user and their contact'''

    __tablename__ = 'friends'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    friend_profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'), nullable=False)
    friendship_verified_by_email = db.Column(db.Boolean, unique=False, default=False)
    friendship_verified_by_facebook = db.Column(db.Boolean, unique=False, default=False)

    profile = db.relationship('Profile', backref='friends')

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Friend record_id=%s user_id=%s  profile_id=%s friendship_verified_by_email=%s friendship_verified_by_facebook=%s>' % (self.record_id, self.user_id, self.profile_id, self.friendship_verified_by_email, self.friendship_verified_by_facebook)


class UserIntolerance(db.Model):
    '''Associates the intolerances that each user has.'''

    __tablename__ = 'userintolerances'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'), nullable=False)
    intol_id = db.Column(db.Integer, db.ForeignKey('intolerances.intol_id'), nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<UserIntolerance record_id=%s profile_id=%s intol_id=%s>' % (self.record_id, self.profile_id, self.intol_id)


class Intolerance(db.Model):
    '''Spoonacular's list of possible intolerances.'''

    __tablename__ = 'intolerances'

    intol_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    intol_name = db.Column(db.String(64), nullable=False)
    intol_description = db.Column(db.String(120), nullable=False)  # Spoonacular's criteria for searching

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Intolerance int_id=%s int_name=%s int_description=%s>' % (self.intol_id, self.intol_name, self.intol_description)


class Diet(db.Model):
    '''Spoonacular's diet choices.'''

    __tablename__ = 'diets'

    diet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    diet_type = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    ranking = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Diet diet_id=%s diet_type=%s description=%s restrictive_ranking=%s>' % (self.diet_id, self.diet_type, self.description, self.restrictive_ranking)


class Cuisine(db.Model):
    '''Spoonacular cuisine types.'''

    __tablename__ = 'cuisine'

    cuisine_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cuisine_name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Cuisine cuisine_id=%s cuisine_name=%s>' % (self.cuisine_id, self.cuisine_name)


class Course(db.Model):
    '''Spoonacular course types'''

    __tablename__ = 'courses'

    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Course course_id=%s course_name=%s>' % (self.course_id, self.course_name)


class IngToAvoid(db.Model):
    '''Ingredients users would like to avoid.'''

    __tablename__ = 'avoid'

    avoid_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingredient = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(200), nullable=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'), nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<IngToAvoid avoid_id=%s profile_id=%s ingredient=%s reason=%s>' % (self.avoid_id, self.profile_id, self.ingredient, self.reason)


class PartyGuest(db.Model):
    '''Associate users with a party'''

    #  this is a true association table now

    __tablename__ = 'party_guests'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'), nullable=False)


class Party(db.Model):
    '''Create a dinner party to store and link information about a party'''

    __tablename__ = 'parties'

    party_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date_of_party = db.Column(db.Date, nullable=True)
    time_of_party = db.Column(db.Time(timezone=True), nullable=True)

    guest_profiles = db.relationship('Profile',
                                     secondary='party_guests')

    recipes = db.relationship('RecipeCard',
                              secondary='partyrecipes',
                              backref='parties')

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Party party_id=%s title_id=%s host_id=%s date=%s time=%s>' % (self.party_id, self.title, self.host_id, self.date, self.time)


class RecipeCard(db.Model):
    '''Add a recipe to a users recipe box'''

    __tablename__ = 'recipecard'

    recipe_record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    recipe_image_url = db.Column(db.String(300), nullable=False)
    recipe_url = db.Column(db.String(300), nullable=False)
    ingredients = db.Column(db.String(2000), nullable=True)
    instructions = db.Column(db.String(2000), nullable=True)


class RecipeBox(db.Model):
    '''Recipes bookmarked by a user'''

    __tablename__ = 'recipebox'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    recipe_record_id = db.Column(db.Integer, db.ForeignKey('recipecard.recipe_record_id'), nullable=False)


class PartyRecipes(db.Model):
    '''Associate a recipe with a party'''

    __tablename__ = 'partyrecipes'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'), nullable=False)
    recipe_record_id = db.Column(db.Integer, db.ForeignKey('recipecard.recipe_record_id'), nullable=False)
    works_for = db.Column(db.String(1000), nullable=True)


##############################################################################
# Helper functions

def connect_to_db(app, db_uri=None):
    '''Connect the database to our Flask app.'''

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgresql:///kind'
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

##############################################################################
# For testing:

    #  TODO: DOh! These should all be class methods. Move them up under each Class

    # def example_data():
    #     '''Create some sample data.'''

    #     goldilocks = User(email='goldilocks@gmail.com',
    #                       diet_id=7,
    #                       first_name='Goldy',
    #                       last_name='Locks',
    #                       diet_reason='It\'s what works for me',
    #                       verified='True',
    #                       password='FakeyFakey')
    #     goldilocks_avoid = IngToAvoid(user_id=1,
    #                                   ingredient='cinnamon',
    #                                   reason='too spicy')
    #     goldilocks_intol = UserIntolerance(user_id=1,
    #                                        intol_id=11)

    #     mama_bear = User(email='mama@bears.com',
    #                      diet_id=4,
    #                      first_name='Mama',
    #                      last_name='Bears',
    #                      diet_reason='Weight loss',
    #                      verified='False',
    #                      password='Ihatekids')
    #     mama_bear_avoid = IngToAvoid(user_id=2,
    #                                  ingredient='rutabegas',
    #                                  reason='gas')
    #     mama_bear_friendship = Friends(user_id=1,
    #                                    friend_id=2)

    #     papa_bear = User(email='papa@bear.com',
    #                      diet_id=10,
    #                      first_name='Papa',
    #                      last_name='Bear',
    #                      diet_reason='I\'m a bear',
    #                      verified='False',
    #                      password='Rawr')
    #     papa_bear_friendship = Friends(user_id=1,
    #                                    friend_id=3)

    #     baby_bear = User(email='baby@bear.com',
    #                      diet_id=8,
    #                      first_name='Baby',
    #                      last_name='Bear',
    #                      diet_reason='Growing bear',
    #                      verified='False',
    #                      password='FakeyFakey')
    #     baby_bear_avoid = IngToAvoid(user_id=4,
    #                                  ingredient='jalapenos',
    #                                  reason='too spicy')
    #     baby_bear_intol = UserIntolerance(user_id=4,
    #                                       intol_id=4)
    #     baby_bear_friendship = Friends(user_id=1,
    #                                    friend_id=4)

    #     teddy_bear_picnic = Party(title='Teddy Bear\'s Picnic',
    #                               host_id=1, )

    #     picnic_guest1 = PartyGuest(party_id=1,
    #                                user_id=2)
    #     picnic_guest2 = PartyGuest(party_id=1,
    #                                user_id=3)
    #     picnic_guest3 = PartyGuest(party_id=1,
    #                                user_id=4)

    #     test_recipe = RecipeBox(party_id=1,
    #                             recipe_id=472678,
    #                             title='Paleo honey cake',
    #                             recipe_image_url='https://webknox.com/recipeImages/472678-556x370.jpg',
    #                             recipe_url='https://spoonacular.com/recipes/paleo-honey-cake-472678',
    #                             works_for='{"Diets": ["any", "paleo" "primal"], "Ingredients to omit": ["jalapenos", "rutabegas"], "Intolerances/Allergies": ["wheat", "peanuts"]}',
    #                             ingredients='2 1/2 cup blanched almond flour, 1/2 teaspoon celtic sea salt, 4 eggs, 1 tablespoon ground cinnamon, 1/4 teaspoon ground cloves, 1/2 cup honey, 1/2 cup palm oil, 1/2 cup raisins',
    #                             instructions=('Add all the ingredients to a large blender or food processor and puree until smooth.',
    #                                           'Scrape down the sides of the bowl when necessary. Give it a taste and add more stevia or salt to taste. Be sure to puree the mixture as much as possible, you don\'t lose anything by overblending but you sacrifice texture and flavor by underblending!',
    #                                           'Pour into serving bowls and serve immediately.', 'If not serving right away, cover with plastic wrap and refrigerate',
    #                                           'Top the mousse with chopped, salted peanuts and some mini dark chocolate chips if you\'re feeling extra indulgent!'))

    #     db.session.add_all([goldilocks,
    #                         goldilocks_avoid,
    #                         goldilocks_intol,
    #                         mama_bear,
    #                         mama_bear_avoid,
    #                         mama_bear_friendship,
    #                         papa_bear,
    #                         papa_bear_friendship,
    #                         baby_bear,
    #                         baby_bear_avoid,
    #                         baby_bear_intol,
    #                         baby_bear_friendship,
    #                         teddy_bear_picnic,
    #                         picnic_guest1,
    #                         picnic_guest2,
    #                         picnic_guest3,
    #                         test_recipe])
    #     db.session.commit()

##############################################################################

if __name__ == '__main__':
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print 'Connected to DB.'
