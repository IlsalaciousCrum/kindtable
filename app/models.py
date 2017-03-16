'''Models for K(i)ndTable WebApp.'''

from datetime import datetime
from passlib.hash import bcrypt
from . import db, login_manager
from flask_login import UserMixin
import pytz
import os
from itsdangerous import URLSafeSerializer, JSONWebSignatureSerializer

login_serializer = URLSafeSerializer(os.environ['APP_SECRET_KEY'])
registration_serializer = JSONWebSignatureSerializer(os.environ['APP_SECRET_KEY'])


##############################################################################
# Model definitions


class BaseMixin(object):
    '''Adds basic db editing for all classes, with db mechanics abstracted from view'''

    @classmethod
    def create_record(cls, **kw):
        '''Creates a new instance of the class'''

        try:
            obj = cls(**kw)
            db.session.add(obj)
            db.session.commit()
            return obj
        except:
            pass

    def update(self, change_dict):
        '''Update any number of attributes on an instance'''

        for key, value in change_dict.iteritems():
            setattr(self, key, value)
        db.session.commit()
        return self

    def _delete_(self):
        '''Removes an instance from the database'''

        try:
            db.session.delete(self)
            db.session.commit()
        except:
            pass


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


class Profile(BaseMixin, db.Model):
    '''Information about users and their contacts'''

    __tablename__ = 'profiles'

    profile_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    owned_by_user = db.Column(db.Integer)
    email = db.Column(db.String(200), nullable=False, unique=False)
    email_verified = db.Column(db.Boolean, unique=False, default=False)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    diet_id = db.Column(db.Integer, db.ForeignKey('diets.diet_id'), default=10)
    diet_reason = db.Column(db.String(120), nullable=True)
    profile_notes = db.Column(db.String(300), nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    diet = db.relationship('Diet', backref='profiles', lazy='joined')

    avoidances = db.relationship('IngToAvoid', backref='profiles', lazy='joined')

    intolerances = db.relationship('Intolerance',
                                   secondary='profileintolerances',
                                   backref='profiles',
                                   lazy='joined')

    def generate_confirmation_token(self):
        '''Creates an encrypted token to send via email to new user'''

        return registration_serializer.dumps({'confirm': self.id})

    def confirm(self, token):
        try:
            data = registration_serializer.loads(token)
        except:
            return False

        if data.get('confirm') != self.id:
            return False
        else:
            self.email_verified = True
            db.session.commit()
            return True

    def remove_profile(self):
        '''Deletes an unofficial profile and all affected records'''

        if self.friends:
            for friend in self.friend:
                friend.remove_friendship()

        if self.intolerances:
            for intolerance in self.intolerances:
                intolerance._delete_()

        if self.avoidances:
            for ingredient in self.avoidances:
                ingredient._delete_()

        self._delete_()
        db.session.commit()

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


class User(BaseMixin, UserMixin, db.Model):
    '''Registered users of KindTable WebApp.'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    session_token = db.Column(db.String(256))
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

    def make_session_token(self):
        '''Encode a secure token for a cookie'''

        data = [str(self.id), self.password_hash]
        self.session_token = login_serializer.dumps(data)
        db.session.commit()

        return self.session_token

    @login_manager.user_loader
    def load_user(session_token):
        '''The request_loader function asks this function to take the token that was
        stored on the users computer, process it to check if its valid and then
        return a User Object if its valid or None if its not valid.'''

        data = login_serializer.loads(session_token)

        #Find the User
        user = User.query.get(data[0])

        #Check Password and return user or None
        if user and data[1] == user.password_hash:
            return user
        return None

    def get_id(self):
        return unicode(self.session_token)

    def delete_user(self):
        '''deletes a user and all records in affected tables'''

        if self.friends:
            for friend in self.friends:
                friend.remove_friendship()

        if self.parties:
            for party in self.parties:
                party.discard_party()

        if self.recipebox:
            for recipe in self.recipebox:
                recipe._delete_()

        user_profile = self.profile

        self._delete_()

        user_profile.remove_profile()

        db.session.commit()

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<User user_id=%s profile_id=%s>' % (self.id,
                                                    self.profile_id)


class Friend(BaseMixin, db.Model):
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

    friend_profile = db.relationship('Profile', backref='friend')
    user = db.relationship('User', backref='friends')

    def remove_friendship(self):
        '''Removes the friendship and all relevant records'''

        guest_at_party = PartyGuest.query.filter_by(profile_id=self.profile_id).all()
        if guest_at_party:
            for invite in guest_at_party:
                invite._delete_()

        bookmarked = RecipeWorksFor.query.filter_by(profile_id=self.profile_id).all()
        if bookmarked:
            for recipe in bookmarked:
                recipe._delete_()

        self._delete_()
        db.session.commit()

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Friend record_id=%s user_id=%s  friend_profile_id=%s \
        friendship_verified_by_email=%s \
        friendship_verified_by_facebook=%s>' % (self.record_id,
                                                self.user_id,
                                                self.friend_profile_id,
                                                self.friendship_verified_by_email,
                                                self.friendship_verified_by_facebook)


class Intolerance(BaseMixin, db.Model):
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


class ProfileIntolerance(BaseMixin, db.Model):
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


class IngToAvoid(BaseMixin, db.Model):
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


class Party(BaseMixin, db.Model):
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

    def discard_party(self):
        '''Removes the party and any dependent records'''

        if self.party_guests:
            for invite in self.party_guests:
                invite._delete_()
        if self.recipes:
            for party_recipe in self.recipes:
                party_recipe._delete_()

        self._delete_()
        db.session.commit()

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Party party_id=%s title_id=%s host_id=%s>' % (self.party_id,
                                                               self.title,
                                                               self.user_id)


class PartyGuest(BaseMixin, db.Model):
    '''Associate users with a party'''

    #  this is a true association table now

    __tablename__ = 'party_guests'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'),
                         nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'),
                           nullable=False)


class RecipeCard(BaseMixin, db.Model):
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


class RecipeBox(BaseMixin, db.Model):
    '''Recipes bookmarked by a user'''

    __tablename__ = 'recipebox'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_record_id = db.Column(db.Integer,
                                 db.ForeignKey('recipecard.recipe_record_id'),
                                 nullable=False)

    recipes = db.relationship('RecipeCard', lazy='joined')
    works_for = db.relationship('Profile',
                                secondary='worksfor',
                                backref='recipe_box',
                                lazy='joined')

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<RecipeBox record_id=%s user_id=%s \
        recipe_record_id=%s>' % (self.record_id,
                                 self.user_id,
                                 self.recipe_record_id)


class RecipeWorksFor(BaseMixin, db.Model):
    '''Party Guests that this recipe has worked for'''
    __tablename__ = 'worksfor'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_box_id = db.Column(db.Integer, db.ForeignKey('RecipeBox.record_id'), nullable=False)
    guest_profile_id = profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'),
                                              nullable=False)


class PartyRecipes(BaseMixin, db.Model):
    '''Associate a recipe with a party'''

    __tablename__ = 'partyrecipes'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'),
                         nullable=False)
    recipe_record_id = db.Column(db.Integer,
                                 db.ForeignKey('recipecard.recipe_record_id'),
                                 nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<PartyRecipes record_id=%s party_id=%s \
        recipe_record_id=%s works_for=%s>' % (self.record_id,
                                              self.party_id,
                                              self.recipe_record_id,
                                              self.works_for)
