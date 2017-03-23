'''WTForms forms for app data collection'''

from wtforms import Form, widgets, SelectMultipleField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional, DataRequired
from wtforms import ValidationError
from ..models import Profile, Diet, User, Intolerance
from .. import db
from flask import flash, redirect, url_for


class FirstNameForm(Form):
    first_name = StringField('First name:', validators=[InputRequired(message="Please tell us what to you call you."),
                                                        Length(1, 64, message="Limit 64 characters")])
    submit = SubmitField('Update')


class LastNameForm(Form):
    last_name = StringField('Last name:', validators=[InputRequired(message="Please tell us a last name to use for you."),
                                                      Length(1, 64, message="Limit 64 characters")])
    submit = SubmitField('Update')


class DietForm(Form):
    diets = Diet.query.order_by(Diet.diet_type).all()
    diet = RadioField('Diet you follow:', choices=[(diet.diet_id, diet.diet_type) for diet in diets],
                      validators=[DataRequired(message='Please choose a diet')], default="10", coerce=int)
    submit = SubmitField('Update')


class DietReasonForm(Form):
    diet_reason = StringField('Reason you follow this diet:', validators=[Length(1, 128, message="Limit 64 characters"),
                                                                          Optional(strip_whitespace=True)])
    submit = SubmitField('Register')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class IntoleranceForm(Form):

    intolerance_query = Intolerance.query.order_by(Intolerance.intol_name).all()
    intolerances = [(intol.name, intol.description) for intol in intolerance_query]
    example = MultiCheckboxField('Label', choices=intolerances)


class AvoidForm(Form):
    last_name = StringField('Last name:', validators=[InputRequired(message="Please tell us a last name to use for you."),
                                                      Length(1, 64, message="Limit 64 characters")])
    submit = SubmitField('Update')
