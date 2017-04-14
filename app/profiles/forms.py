'''WTForms forms for app data collection'''

from wtforms import Form, widgets, SelectMultipleField
from wtforms import StringField, SubmitField, RadioField, HiddenField, TextField, SelectField
from wtforms.validators import InputRequired, Length, Email, Optional, DataRequired
from wtforms import ValidationError
from wtforms.widgets import TextArea
from ..models import Profile, Diet, User, Intolerance
from .. import db
from flask import flash, redirect, url_for


class FirstNameForm(Form):
    profile_id = HiddenField(validators=[InputRequired()])
    first_name = StringField('Change first name to:',
                             widget=TextArea(),
                             validators=[InputRequired(message="Please tell us what to you call you."),
                                         Length(1, 64, message="Limit 64 characters")])
    submit = SubmitField('Update')


class LastNameForm(Form):
    profile_id = HiddenField(validators=[InputRequired()])
    last_name = StringField('Last name:',
                            widget=TextArea(),
                            validators=[InputRequired(message="Please tell us a last name to use for you."),
                                        Length(1, 64, message="Limit 64 characters")])
    submit = SubmitField('Update')


class DietForm(Form):
    profile_id = HiddenField(validators=[InputRequired()])
    diets = Diet.query.order_by(Diet.diet_type).all()
    diet = RadioField('Diet you follow:',
                      choices=[(diet.diet_id, '{} - <span class="text-muted small">{}</span>'.format(diet.diet_type, diet.description)) for diet in diets],
                      validators=[DataRequired(message='Please choose a diet')], default="10", coerce=int)
    submit = SubmitField('Update')


class DietReasonForm(Form):
    profile_id = HiddenField()
    diet_reason = TextField('Reason you follow this diet:',
                            widget=TextArea(),
                            validators=[Length(1, 128, message="Limit 64 characters"), DataRequired(message='Please enter a reason or exit the window')])
    submit = SubmitField('Update')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class IntoleranceForm(Form):
    profile_id = HiddenField()
    intol_query = Intolerance.query.order_by(Intolerance.intol_name).all()
    intolerances = SelectField('Select all allergies and intolerance groups that apply to you',
                               choices=[(intol.intol_id, '{} - <span class="text-muted small">{}</span>'.format(intol.intol_name, intol.intol_description)) for intol in intol_query],
                               validators=[DataRequired(message='Please choose a diet')], default="10", coerce=int)
    submit = SubmitField('Update')


class AddAvoidForm(Form):
    profile_id = HiddenField()
    avoid_id = HiddenField()
    add_avoid_ingredient = StringField('Ingredient to avoid:',
                                       widget=TextArea(),
                                       validators=[InputRequired(message="Please enter an ingredient to avoid."),
                                                   Length(1, 64, message="Limit 64 characters")])
    add_avoid_reason = TextField('Reason you would like to avoid this ingredient:',
                                 widget=TextArea(),
                                 validators=[Length(1, 128, message="Limit 128 characters"), Optional()])
    submit = SubmitField('Update')


class UpdateAvoidForm(Form):
    profile_id = HiddenField()
    avoid_id = HiddenField()
    update_avoid_ingredient = StringField('Change ingredient to avoid:',
                                          widget=TextArea(),
                                          validators=[InputRequired(message="Please click on 'delete ingredient' to remove this ingredient"),
                                                      Length(1, 64, message="Limit 64 characters")])
    update_avoid_reason = TextField('Change the reason you avoid this ingredient:',
                                    widget=TextArea(),
                                    validators=[Length(1, 128, message="Limit 128 characters"), Optional()])
    submit = SubmitField('Update')


class FriendEmailForm(Form):
    email = StringField('Email', validators=[InputRequired('Email address is a required field.'),
                                             Length(1, 64),
                                             Email('A valid email address is required.')])
    submit = SubmitField('Update')


class AddNewFriendForm(Form):
    first_name = StringField('First name:', validators=[InputRequired(message="Please tell us what to you call you."),
                                                        Length(1, 64, message="Limit 64 characters")])
    last_name = StringField('Last name:', validators=[InputRequired(message="Please tell us a last name to use for you."),
                                                      Length(1, 64, message="Limit 64 characters")])
    diets = Diet.query.order_by(Diet.diet_type).all()
    diet = RadioField('Diet you follow:', choices=[(diet.diet_id, diet.diet_type) for diet in diets],
                      validators=[DataRequired(message='Please choose a diet')], default="10", coerce=int)
    diet_reason = StringField('Reason you follow this diet:', validators=[Length(1, 128, message="Limit 64 characters"),
                                                                          Optional(strip_whitespace=True)])
    email = StringField('Email:',
                        validators=[InputRequired(message='We need an email address to register you with Kind Table.'),
                                    Length(1, 64, message="Limit 64 characters"),
                                    Email(message='Please provide a valid email address so that you can confirm your account.')])
    submit = SubmitField('Register')

    def validate_email(self, field):
        print "checking valid email"
        if db.session.query(Profile).join(User).filter(Profile.email == field.data, User.profile_id == Profile.owned_by_user_id).first():
            print "triggering the email validation but somehow not flashing"
            flash('Email address already registered. Please log in.')
            raise ValidationError('Email address already registered. Please log in.')
            return redirect(url_for('main.login'))
