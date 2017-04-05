'''WTForms forms for user management'''

from wtforms import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional, DataRequired, ValidationError
from wtforms.widgets import TextArea
from ..models import Profile, Diet, User
from .. import db
from flask import flash, redirect, url_for


class LoginForm(Form):
    email = StringField('Email', validators=[InputRequired('Email address is a required field.'),
                                             Length(1, 64),
                                             Email('A valid email address is required.')])
    password = PasswordField('Password',
                             validators=[InputRequired('Please enter a valid password or reset password')])
    remember_me = BooleanField('Keep me logged in')
    submit1 = SubmitField('Log in')


class RegistrationForm(Form):
    first_name = StringField('First name:', validators=[InputRequired(message="Please tell us what to you call you."),
                                                        Length(1, 64, message="Limit 64 characters")])
    last_name = StringField('Last name:', validators=[InputRequired(message="Please tell us a last name to use for you."),
                                                      Length(1, 64, message="Limit 64 characters")])
    diets = Diet.query.order_by(Diet.diet_type).all()
    diet = RadioField('Diet you follow:', choices=[(diet.diet_id, diet.diet_type) for diet in diets],
                      validators=[DataRequired(message='Please choose a diet')], default="10", coerce=int)
    diet_reason = TextField('Reason you follow this diet:', widget=TextArea(), validators=[Length(1, 128, message="Limit 64 characters"),
                            Optional(strip_whitespace=True)])
    email = StringField('Email:',
                        validators=[InputRequired(message='We need an email address to register you with Kind Table.'),
                                    Length(1, 64, message="Limit 64 characters"),
                                    Email(message='Please provide a valid email address so that you can confirm your account.')])
    password = PasswordField('Password:',
                             validators=[InputRequired(message='Please provide a strong password'),
                                         Length(1, 64, message="Limit 64 characters"),
                                         EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password:', validators=[InputRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        print "checking valid email"

        if db.session.query(User).join(Profile).filter(Profile.email == field.data, User.profile_id == Profile.profile_id).first():
            print "triggering the email validation but somehow not flashing"
            flash('Email address already registered. Please log in.')
            raise ValidationError('Email address already registered. Please log in.')
            return redirect(url_for('main.login'))


class PasswordChangeForm(Form):
    old_password = PasswordField('Old password:', validators=[InputRequired('Please enter your current password'),
                                                              Length(1, 64)])
    password = PasswordField('Password:',
                             validators=[InputRequired(message='Please provide a strong password'),
                                         Length(1, 64, message="Limit 64 characters"),
                                         EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password:', validators=[InputRequired()])
    submit = SubmitField('Change Password')


class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[InputRequired(), Length(1, 64),
                                             Email()])
    submit2 = SubmitField('Reset Password')


class PasswordResetForm(Form):
    email = StringField('Email',
                        validators=[InputRequired(), Length(1, 64),
                                    Email()])
    password = PasswordField('New Password',
                             validators=[InputRequired(),
                                         EqualTo('password2',
                                                 message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        print "checking valid email/user/profile"
        if db.session.query(User).join(Profile).filter(Profile.email == field.data, User.profile_id == Profile.profile_id).first() is None:
            raise ValidationError('Unknown email address.')


class ChangeEmailForm(Form):
    email = StringField('New Email:', validators=[InputRequired(),
                                                  Length(1, 64),
                                                  Email(),
                                                  EqualTo('email2',
                                                          message='Email addresses must match')])
    email2 = StringField('Confirm new email:',
                         validators=[InputRequired(),
                                     Length(1, 64),
                                     Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if db.session.query(User).join(Profile).filter(Profile.email == field.data, User.profile_id == Profile.profile_id).first():
            raise ValidationError('That email address is already registered.')
