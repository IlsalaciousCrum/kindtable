'''WTForms forms for app data collection'''

from wtforms import Form, widgets
from wtforms import StringField, SubmitField, RadioField, HiddenField, TextField, SelectMultipleField, DateField
from wtforms.validators import InputRequired, Length, Email, Optional, DataRequired, EqualTo
from wtforms import ValidationError
from wtforms.widgets import TextArea
from ..models import Profile, Diet, User, Intolerance, Party, Friend, Party
from .. import db
from flask import flash, redirect, url_for, request
from flask_login import current_user
from datetime import datetime, date
from wtforms_components import DateRange


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SearchForm(Form):
    party_id = HiddenField(validators=[InputRequired()])
    submit = SubmitField('Update')


class RecipeSearch(Form):
    intols = HiddenField(validators=[InputRequired()])
    cuisine = HiddenField(validators=[InputRequired()])
    course = HiddenField(validators=[InputRequired()])
    newdiets = HiddenField(validators=[InputRequired()])
    avoids = HiddenField(validators=[InputRequired()])
    recipe_id = HiddenField(validators=[InputRequired()])


class SeeRecipe(Form):
    recipe_id = HiddenField(validators=[InputRequired()])
    submit = SubmitField('Update')


class SaveRecipe(Form):
    
    recipe_id = HiddenField(validators=[InputRequired()])
    notes = StringField('Recipe notes',
                        widget=TextArea())
    submit = SubmitField('Update')
