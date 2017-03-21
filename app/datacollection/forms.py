'''WTForms forms for app data collection'''

from wtforms import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional, DataRequired
from wtforms import ValidationError
from ..models import Profile, Diet, User
from .. import db
from flask import flash, redirect, url_for

diets = Diet.query.order_by(Diet.diet_type).all()


class ExampleForm(Form):
    first_name = StringField('First name:', validators=[InputRequired(message="Please tell us what to you call you."),
                                                        Length(1, 64, message="Limit 64 characters")])
    last_name = StringField('Last name:', validators=[InputRequired(message="Please tell us a last name to use for you."),
                                                      Length(1, 64, message="Limit 64 characters")])
    diet = RadioField('Diet you follow:', choices=[(diet.diet_id, diet.diet_type) for diet in diets],
                      validators=[DataRequired(message='Please choose a diet')], default="10", coerce=int)
    diet_reason = StringField('Reason you follow this diet:', validators=[Length(1, 128, message="Limit 64 characters"),
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

    def validate_field_example(self, field):
        print "checking valid email"
        if db.session.query(Profile).join(User).filter(Profile.email == field.data, User.profile_id == Profile.owned_by_user_id).first():
            print "triggering the email validation but somehow not flashing"
            flash('Email address already registered. Please log in.')
            raise ValidationError('Email address already registered. Please log in.')
            return redirect(url_for('main.login'))