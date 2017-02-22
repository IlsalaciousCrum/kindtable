'''Models for K(i)ndTable WebApp.'''

from datetime import datetime
from passlib.hash import bcrypt
from . import db, login_manager
from flask_login import UserMixin
import pytz


##############################################################################
# Model definitions


class Diet(db.Model):
    '''Spoonacular's diet choices.'''

    __tablename__ = 'diets'

    diet_id = db.Column(db.Integer, primary_key=True)
    diet_type = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    ranking = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Diet diet_id=%s diet_type=%s description=%s \
        restrictive_ranking=%s>' % (self.diet_id,
                                    self.diet_type,
                                    self.description,
                                    self.ranking)


class Profile(db.Model):
    '''Information about users and their contacts'''

    __tablename__ = 'profiles'

    profile_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    is_user_profile = db.Column(db.Boolean, unique=False, default=False)
    created_by_email_owner = db.Column(db.Boolean, unique=False, default=False)
    email = db.Column(db.String(200), nullable=False, unique=False)
    email_verified = db.Column(db.Boolean, unique=False, default=False)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    diet_id = db.Column(db.Integer, db.ForeignKey('diets.diet_id'), default=10)
    # ie, ethical, religious, general health, specific health
    diet_reason = db.Column(db.String(120), nullable=True)
    profile_notes = db.Column(db.String(300), nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    diet = db.relationship('Diet', backref='profiles', lazy='joined')

    avoidances = db.relationship('IngToAvoid', backref='profiles', lazy='joined')

    intolerances = db.relationship('Intolerance',
                                   secondary='profileintolerances',
                                   backref='profiles',
                                   lazy='joined')

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Profile profile_id=%s is_user_profile=%s email=%s email_verified=%s \
        first_name=%s last_name=%s \
        diet_id=%s diet_reason=%s \
        profile_notes=%s last_updated=%s>' % (self.profile_id,
                                              self.is_user_profile,
                                              self.email,
                                              self.email_verified,
                                              self.first_name,
                                              self.last_name,
                                              self.diet_id,
                                              self.diet_reason,
                                              self.profile_notes,
                                              self.last_updated)


class User(UserMixin, db.Model):
    '''Registered users of KindTable WebApp.'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    password_hash = db.Column(db.String(128))
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'),
                           nullable=False, unique=False)

    parties = db.relationship('Party', backref='user')
    recipebox = db.relationship('RecipeBox', backref='user')

    profile = db.relationship("Profile",
                              uselist=False,
                              backref="user")

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, plaintext):
        """Encrypts a password for the user table."""

        self.password_hash = bcrypt.hash(plaintext)

    def verify_password(self, password):
        """Verifies a password from the user table."""

        if bcrypt.verify(password, self.password_hash) is True:
            return True
        else:
            return False

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<User user_id=%s profile_id=%s>' % (self.id,
                                                    self.profile_id)

    def friends_list(self):
        '''Returns a nested list of a users friends'''

        friends_query = Friend.query.filter_by(user_id=self.id).all()
        friends_list = []
        for friend in friends_query:
            friends_list.append([friend.profile.profile_id, friend.profile.email, friend.profile.first_name, friend.profile.last_name])
        return friends_list


class Friend(db.Model):
    '''Makes connection between the user and their contact'''

    __tablename__ = 'friends'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)
    friend_profile_id = db.Column(db.Integer,
                                  db.ForeignKey('profiles.profile_id'),
                                  nullable=False)
    friendship_verified_by_email = db.Column(db.Boolean, unique=False,
                                             default=False)
    friendship_verified_by_facebook = db.Column(db.Boolean, unique=False,
                                                default=False)

    profile = db.relationship('Profile', backref='friend')
    user = db.relationship('User', backref='friends')

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Friend record_id=%s user_id=%s  friend_profile_id=%s \
        friendship_verified_by_email=%s \
        friendship_verified_by_facebook=%s>' % (self.record_id,
                                                self.user_id,
                                                self.friend_profile_id,
                                                self.friendship_verified_by_email,
                                                self.friendship_verified_by_facebook)


class Intolerance(db.Model):
    '''Spoonacular's list of possible intolerances.'''

    __tablename__ = 'intolerances'

    intol_id = db.Column(db.Integer, primary_key=True)
    intol_name = db.Column(db.String(64), nullable=False)
    intol_description = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Intolerance int_id=%s int_name=%s \
        int_description=%s>' % (self.intol_id,
                                self.intol_name,
                                self.intol_description)


class ProfileIntolerance(db.Model):
    '''Associates the intolerances that each user has.'''

    __tablename__ = 'profileintolerances'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'),
                           nullable=False)
    intol_id = db.Column(db.Integer, db.ForeignKey('intolerances.intol_id'),
                         nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<ProfileIntolerance record_id=%s profile_id=%s \
        intol_id=%s>' % (self.record_id,
                         self.profile_id,
                         self.intol_id)


class Cuisine(db.Model):
    '''Spoonacular cuisine types.'''

    __tablename__ = 'cuisine'

    cuisine_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cuisine_name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Cuisine cuisine_id=%s cuisine_name=%s>' % (self.cuisine_id,
                                                            self.cuisine_name)


class Course(db.Model):
    '''Spoonacular course types'''

    __tablename__ = 'courses'

    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Course course_id=%s course_name=%s>' % (self.course_id,
                                                         self.course_name)


class IngToAvoid(db.Model):
    '''Ingredients users would like to avoid.'''

    __tablename__ = 'avoid'

    avoid_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingredient = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(200), nullable=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'),
                           nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<IngToAvoid avoid_id=%s profile_id=%s ingredient=%s \
        reason=%s>' % (self.avoid_id,
                       self.profile_id,
                       self.ingredient,
                       self.reason)


class Party(db.Model):
    '''Create a dinner party to store and link information about a party'''

    __tablename__ = 'parties'

    party_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)
    datetime_of_party = db.Column(db.DateTime(timezone=True), nullable=True)
    guest_profiles = db.relationship('Profile',
                                     secondary='party_guests',
                                     lazy='joined',
                                     backref='party')

    recipes = db.relationship('RecipeCard',
                              secondary='partyrecipes',
                              backref='parties',
                              lazy='joined')

    @property
    def date(self):
        raise AttributeError('This is UTC time. Use the class method')

    @date.setter
    def date(self, plaintext, local_timezone):
        """Converts a local time to a UTC time"""

        local = pytz.timezone(local_timezone)
        naive = datetime.datetime.strptime(plaintext, "%Y-%m-%d %H:%M:%S")
        local_dt = local.localize(naive, is_dst=None)
        self.datetime_of_party = local_dt.astimezone(pytz.utc)

    def party_in_local_time(self, local_timezone):
        """Converts the stored UTC time to the local time of the user"""

        fmt = fmt = '%A %B %s, %Y %H:%M %Z'
        UTC_dt = self.datetime_of_party
        local_date_time = UTC_dt.astimezone(local_timezone)
        return local_date_time.strftime(fmt)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Party party_id=%s title_id=%s host_id=%s>' % (self.party_id,
                                                               self.title,
                                                               self.user_id)


class PartyGuest(db.Model):
    '''Associate users with a party'''

    #  this is a true association table now

    __tablename__ = 'party_guests'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'),
                         nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'),
                           nullable=False)


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

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<RecipeCard recipe_record_id=%s recipe_id=%s title=%s \
        recipe_image_url=%s recipe_url=%s ingredients=%s \
        instructions=%s>' % (self.recipe_record_id,
                             self.recipe_id,
                             self.title,
                             self.recipe_image_url,
                             self.recipe_url,
                             self.ingredients,
                             self.instructions)


class RecipeBox(db.Model):
    '''Recipes bookmarked by a user'''

    __tablename__ = 'recipebox'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_record_id = db.Column(db.Integer,
                                 db.ForeignKey('recipecard.recipe_record_id'),
                                 nullable=False)

    recipes = db.relationship('RecipeCard', lazy='joined')

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<RecipeBox record_id=%s user_id=%s \
        recipe_record_id=%s>' % (self.record_id,
                                 self.user_id,
                                 self.recipe_record_id)


class PartyRecipes(db.Model):
    '''Associate a recipe with a party'''

    __tablename__ = 'partyrecipes'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'),
                         nullable=False)
    recipe_record_id = db.Column(db.Integer,
                                 db.ForeignKey('recipecard.recipe_record_id'),
                                 nullable=False)
    works_for = db.Column(db.String(1000), nullable=True)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<PartyRecipes record_id=%s party_id=%s \
        recipe_record_id=%s works_for=%s>' % (self.record_id,
                                              self.party_id,
                                              self.recipe_record_id,
                                              self.works_for)
