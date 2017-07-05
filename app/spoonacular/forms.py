'''WTForms forms for app data collection'''

from wtforms import Form, widgets
from wtforms import StringField, SubmitField, HiddenField, SelectMultipleField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import TextArea


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


class RecipeNotesForm(Form):
    recipe_id = HiddenField(validators=[InputRequired()])
    notes = StringField('Recipe notes',
                        widget=TextArea(), validators=[Length(1, 300)])
    submit = SubmitField('Update')


class DeleteRecipeForm(Form):
    recipe_id = HiddenField(validators=[InputRequired()])
    party_id = HiddenField(validators=[InputRequired()])
    submit = SubmitField('Update')


class EmailMenuForm(Form):
    party_id = HiddenField(validators=[InputRequired()])
    submit = SubmitField('Email Menu')
