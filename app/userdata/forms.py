from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import Required, Length, Email
from .models import Diet, Intolerances


class ProfileData(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Password', validators=[DataRequired()])

    *first_name = StringField('First name', nullable=True)
    *last_name = StringField('Last name', nullable=True)

    diet_id = SelectField('Diet', validators=[DataRequired()])

    diet_reason = TextAreaField('Reason for following this diet')

    profile_notes = TextAreaField('Profile notes')

    intolerances = RadioField('Intolerances')

    avoid = StringFielddb.Column(db.String(100), nullable=False)
    *reason = db.Column(db.String(200), nullable=True)
                           nullable=False)

*    register = SubmitField('Register')



        choices=[(10, 'omnivore: does not follow any particular diet'),
                 (1, 'vegan: does not eat an animal byproducts)'),
                 (2, 'ketogenic: high-fat, adequate-protein, low-carbohydrate diet'),
                 (3, 'vegetarian: does not eat meat'),
                 (4,'ovo vegetarian: vegetarian who eats eggs but not dairy products'),
                 (5, 'lacto vegetarian: vegetarian who eats dairy products but not meat or eggs'),
                 (6, 'pescatarian: eats fish and shellfish but not animal meat'),
                 (7, 'paleo: (it\s best to look this one up if you are not sure)'),
                 (8, 'primal: (it\s best to look this one up if you are not sure'),
                 (9, 'whole 30: (it\s best to look this one up if you are not sure')]