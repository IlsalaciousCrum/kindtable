'''Models for K(i)ndTable WebApp.'''

from datetime import datetime
from passlib.hash import bcrypt
from . import db, login_manager
from flask import flash
from flask_login import UserMixin, current_user
from itsdangerous import JSONWebSignatureSerializer, URLSafeTimedSerializer, URLSafeSerializer, BadSignature, SignatureExpired, BadData
import os
from sqlalchemy import and_, or_

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


class Diet(BaseMixin, db.Model):
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
    owned_by_user_id = db.Column(db.Integer)
    email = db.Column(db.String(200), unique=False)
    private_profile_title = db.Column(db.String(100), unique=False)
    email_verified = db.Column(db.Boolean, unique=False, default=False)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    diet_id = db.Column(db.Integer, db.ForeignKey('diets.diet_id'), default=10)
    diet_reason = db.Column(db.String(128), nullable=True)
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

        registration_serializer = URLSafeTimedSerializer(os.environ['APP_SECRET_KEY'])
        return registration_serializer.dumps({'profile_id': self.profile_id, 'email': self.email})

    def confirm(self, token):
        registration_serializer = URLSafeTimedSerializer(os.environ['APP_SECRET_KEY'])
        try:
            data = registration_serializer.loads(token, max_age=86400)
        except SignatureExpired, e:
            encoded_payload = e.payload
            if encoded_payload is not None:
                try:
                    decoded_payload = registration_serializer.load_payload(encoded_payload)
                    return decoded_payload
                except:
                    flash("There seems to be something wrong with your confirmation email. Please email kindtableapp@gmail.com for assistance.", 'danger')
                    return False
        except BadData:
            flash("There seems to be something wrong with your confirmation email. Please email kindtableapp@gmail.com for assistance.", 'danger')
            return False
        except BadSignature:
            # TODO: add functionality to email me an error log when this happens with all possible information
            flash("There seems to be something wrong with your confirmation email. Please email kindtableapp@gmail.com for assistance.", 'danger')
            return False

        if data['profile_id'] != self.profile_id and data['email'] != self.email:
            return False
        else:
            user = User.query.get(self.owned_by_user_id)
            return user

    def remove_profile(self):
        '''Deletes an unofficial profile and all affected records'''

        _intolerances = ProfileIntolerance.query.filter(ProfileIntolerance.profile_id == self.profile_id).all()
        if _intolerances:
            for intolerance in _intolerances:
                intolerance._delete_()

        if self.avoidances:
            for ingredient in self.avoidances:
                ingredient._delete_()

        parties_invited = PartyGuest.query.filter(PartyGuest.friend_profile_id == self.profile_id).all()
        if parties_invited:
            for party in parties_invited:
                party.disinvite_guest()

        friendship = Friend.query.filter(Friend.friend_profile_id == self.profile_id).all()
        if friendship:
            for friend in friendship:
                friend.remove_friendship()

        self._delete_()

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Profile profile_id=%s owned_by_user_id=%s email=%s \
        email_verified=%s first_name=%s last_name=%s diet_id=%s diet_reason=%s \
        last_updated=%s>' % (self.profile_id,
                             self.owned_by_user_id,
                             self.email,
                             self.email_verified,
                             self.first_name,
                             self.last_name,
                             self.diet_id,
                             self.diet_reason,
                             self.last_updated)


class User(BaseMixin, UserMixin, db.Model):
    '''Registered users of KindTable WebApp.'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    beta_approved = db.Column(db.Boolean, unique=False, default=False)
    session_token = db.Column(db.String(256))
    password_hash = db.Column(db.String(128))
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'),
                           nullable=False, unique=False)

    parties = db.relationship('Party', backref='user')

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

    def reset_password(self, token, new_password):
        registration_serializer = URLSafeTimedSerializer(os.environ['APP_SECRET_KEY'])
        try:
            data = registration_serializer.loads(str(token))
        except:
            return False

        if data['profile_id'] != self.profile.profile_id and data['email'] != self.profile.email:
            return False
        else:
            self.password = new_password
            db.session.commit()
            return True

    def make_session_token(self):
        '''Encode a secure token for a cookie'''

        login_serializer = JSONWebSignatureSerializer(os.environ['APP_SECRET_KEY'])
        self.session_token = login_serializer.dumps({'id': self.id})
        db.session.commit()

        return self.session_token

    @login_manager.user_loader
    def load_user(session_token):
        '''The request_loader function asks this function to take the token that was
        stored on the users computer, process it to check if its valid and then
        return a User Object if its valid or None if its not valid.'''

        login_serializer = JSONWebSignatureSerializer(os.environ['APP_SECRET_KEY'])
        data = login_serializer.loads(session_token)
        #Find the User
        user = User.query.get(data['id'])
        #Check Password and return user or None
        if user:
            return user
        else:
            return None

    def get_id(self):
        return unicode(self.session_token)

    def valid_friends(self):
        '''Returns a list with the profile objects of friends that have been confirmed'''

        # Sublime flags ' == True,' as a syntax error but in this case, for SQLAlchemy,
        # this is the correct syntax.

        return db.session.query(Profile).join(Friend).join(User).filter(and_(Friend.user_id == self.id),
                                                                       (or_(Friend.friendship_verified_by_email == True,
                                                                        (Friend.private_profile == True)))).all()

    def delete_user(self):
        '''deletes a user and all records in affected tables'''

        if self.friends:
            for friend in self.friends:
                friend.remove_friendship()

        if self.parties:
            for party in self.parties:
                party.discard_party()

        private_profiles = Profile.query.filter(Profile.owned_by_user_id == self.id).all()
        if private_profiles:
            for profile in private_profiles:
                profile.remove_profile()

        self._delete_()

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
    friend_request_sent = db.Column(db.Boolean, unique=False,
                                    default=False)
    friend_notes = db.Column(db.String(300), nullable=True)
    friendship_verified_by_email = db.Column(db.Boolean, unique=False,
                                             default=False)
    private_profile = db.Column(db.Boolean, unique=False,
                                default=False)
    friend_profile = db.relationship('Profile', backref='friend')
    user = db.relationship('User', backref='friends')

    @classmethod
    def process_email_token(self, token, responding_user):

        email_serializer = URLSafeSerializer(os.environ['APP_SECRET_KEY'])
        try:
            data = email_serializer.loads(token)
        except:
            flash("It looks like there is something wrong with your token. Please email kindtableapp@gmail.com")
            return False

        requesting_user = User.query.get(data['requesting_user_id'])

        # is the requesting user still logged in
        if data['requesting_user_id'] == responding_user.id:
            return "logout"

        # is the requesting_user from the token still a user:

        if not requesting_user:
            return "not found"

        # did you already become friends in another way
        existing_friendship = Friend.query.filter((Friend.user_id == requesting_user.id)
                                                  & (Friend.friend_profile_id ==
                                                     responding_user.profile_id)
                                                  & (Friend.friendship_verified_by_email == True)
                                                  | (Friend.private_profile == False)).first()

        if existing_friendship:
            return "already friends"
        else:
            requesting_friendship = Friend.create_record(user_id=requesting_user.id,
                                                         friend_profile_id=responding_user.profile_id,
                                                         friendship_verified_by_email=True)
            responding_friendship = Friend.create_record(user_id=responding_user.id,
                                                         friend_profile_id=requesting_user.profile_id,
                                                         friendship_verified_by_email=True)
            self._delete_()
            return responding_friendship

    def remove_friendship(self):
        '''Removes the friendship and all relevant records'''

        guest_at_party = PartyGuest.query.filter_by(friend_profile_id=self.friend_profile_id).all()
        if guest_at_party:
            for invite in guest_at_party:
                invite._delete_()

        self._delete_()

    @classmethod
    def already_friends(self, user, friend_user):
        friendship1 = Friend.query.filter(Friend.user_id == user.id, Friend.friend_profile_id == friend_user.profile_id).first()
        friendship2 = Friend.query.filter(Friend.user_id == friend_user.id, Friend.friend_profile_id == user.profile_id).first()

        if friendship1 and friendship2:
            return True
        else:
            return False

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Friend record_id=%s user_id=%s  friend_profile_id=%s \
        friendship_verified_by_email=%s>' % (self.record_id,
                                             self.user_id,
                                             self.friend_profile_id,
                                             self.friendship_verified_by_email)


class FriendRequest(BaseMixin, db.Model):
    '''Holds single use friend requests'''

    __tablename__ = 'friendrequests'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    requesting_user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                                   nullable=False)
    email_sent_to = db.Column(db.String(200), unique=False, nullable=True)
    token = db.Column(db.String(300), unique=False)

    user = db.relationship('User', backref='friend_requests')
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def generate_email_token(self, requesting_user_id, email_sent_to=None):
        '''Creates an encrypted token to send via email to new user'''

        email_serializer = URLSafeSerializer(os.environ['APP_SECRET_KEY'])
        new_token = email_serializer.dumps({'requesting_user_id': requesting_user_id})
        new_record = FriendRequest.create_record(requesting_user_id=requesting_user_id,
                                                 email_sent_to=email_sent_to,
                                                 token=new_token)
        print "new friend request record below"
        print new_record
        return new_token

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<FriendRequest record_id=%s requesting_user_id=%s  email_sent_to=%s \
        token=%s date_sent=%s>' % (self.record_id,
                                   self.requesting_user_id,
                                   self.email_sent_to,
                                   self.token,
                                   self.date_sent)


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

    def remove_intolerance(self):
        '''removes an intolerance for the profile'''

        self._delete_()
        db.session.commit()

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<ProfileIntolerance record_id=%s profile_id=%s \
        intol_id=%s>' % (self.record_id,
                         self.profile_id,
                         self.intol_id)


class Cuisine(BaseMixin, db.Model):
    '''Spoonacular cuisine types.'''

    __tablename__ = 'cuisines'

    cuisine_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cuisine_name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Cuisine cuisine_id=%s cuisine_name=%s>' % (self.cuisine_id,
                                                            self.cuisine_name)


class Course(BaseMixin, db.Model):
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

    def remove_avoidance(self):
        '''removes an ingredient to avoid for the profile'''

        self._delete_()
        db.session.commit()

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
    party_notes = db.Column(db.String(300), nullable=True)
    guests = db.relationship('PartyGuest', backref='party',
                             lazy='joined')
    party_recipes = db.relationship('PartyRecipes', backref='parties',
                                    lazy='joined')
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    def discard_party(self):
        '''Removes the party and any dependent records'''

        if self.guests:
            for invite in self.guests:
                invite._delete_()
        if self.party_recipes:
            for party_recipe in self.party_recipes:
                party_recipe._delete_()

        self._delete_()

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
    friend_profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'),
                                  nullable=False)

    profiles = db.relationship('Profile', backref='partyguest')

    def disinvite_guest(self):
        '''removes a guest from the party'''

        self._delete_()

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<PartyGuest record_id=%s party_id=%s friend_profile_id=%s>' % (self.record_id,
                                                                               self.party_id,
                                                                               self.friend_profile_id)


class RecipeCard(BaseMixin, db.Model):
    '''Saves a recipe from a Spoonacular query'''

    __tablename__ = 'recipecard'

    recipe_record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    recipe_image_url = db.Column(db.String(300), nullable=False)
    spoonacular_recipe_url = db.Column(db.String(300), nullable=False)
    source_recipe_url = db.Column(db.String(300), nullable=False)
    ingredients = db.Column(db.String(2000))
    instructions = db.Column(db.String(2000))

    party_recipes = db.relationship('PartyRecipes')

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<RecipeCard recipe_record_id=%s recipe_id=%s title=%s>' % (self.recipe_record_id,
                                                                           self.recipe_id,
                                                                           self.title)


class PartyRecipes(BaseMixin, db.Model):
    '''Associate a recipe with a party'''

    __tablename__ = 'partyrecipes'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    party_id = db.Column(db.Integer,
                         db.ForeignKey('parties.party_id'),
                         nullable=False)
    recipe_record_id = db.Column(db.Integer,
                                 db.ForeignKey('recipecard.recipe_record_id'),
                                 nullable=False)
    course_id = db.Column(db.Integer,
                          db.ForeignKey('courses.course_id'),
                          nullable=False)
    cuisine_id = db.Column(db.Integer,
                           db.ForeignKey('cuisines.cuisine_id'),
                           nullable=False)
    works_for = db.Column(db.String(2000), nullable=True)
    recipe_notes = db.Column(db.String(300), nullable=True)
    course = db.relationship('Course',
                             backref='party_recipes',
                             lazy='joined')
    cuisine = db.relationship('Cuisine',
                              backref='party_recipes',
                              lazy='joined')
    recipes = db.relationship('RecipeCard')

    def discard_recipe(self):
        '''Discards a recipe saved for a party'''

        self._delete_()

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<PartyRecipes record_id=%s party_id=%s \
        recipe_record_id=%s>' % (self.record_id,
                                 self.party_id,
                                 self.recipe_record_id)
