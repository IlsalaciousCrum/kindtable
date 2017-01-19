from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField, TextAreaField, RadioField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, Required, Length
from ..models import Diet, Intolerance

diets = Diet.query.all()

intolerances = Intolerance.query.all()


class ProfileData(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    first_name = StringField('First name', nullable=True)
    last_name = StringField('Last name', nullable=True)
    diet_id = SelectField('Diet',
                          validators=[DataRequired()],
                          choices=[(10, 'omnivore: does not follow any particular diet'),
                                   (1, 'vegan: does not eat an animal byproducts)'),
                                   (2, 'ketogenic: high-fat, adequate-protein, low-carbohydrate diet'),
                                   (3, 'vegetarian: does not eat meat'),
                                   (4, 'ovo vegetarian: vegetarian who eats eggs but not dairy products'),
                                   (5, 'lacto vegetarian: vegetarian who eats dairy products but not meat or eggs'),
                                   (6, 'pescatarian: eats fish and shellfish but not animal meat'),
                                   (7, 'paleo: (it\s best to look this one up if you are not sure)'),
                                   (8, 'primal: (it\s best to look this one up if you are not sure'),
                                   (9, 'whole 30: (it\s best to look this one up if you are not sure')])
    diet_reason = TextAreaField('Reason for following this diet')
    profile_notes = TextAreaField('Profile notes')
    intolerances = RadioField('Intolerances')
    avoid = StringField('Ingredients to avoid')
    reason = TextAreaField('Reason you would like to avoid this food')
    register = SubmitField('Register')
