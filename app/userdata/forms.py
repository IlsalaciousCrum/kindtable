from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField, TextAreaField, RadioField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, Required, Length
from ..models import Diet, Intolerance
from app import db

diet_query = db.session.query(Diet.diet_id, Diet.diet_type, Diet.description).all()
diet_options = []
for each in diet_query:
    display_text = each[1] + ": " + each[2]
    entry = (each[0], display_text)
    diet_options.append(entry)

intol_query = db.session.query(Intolerance.intol_id, Intolerance.intol.description).all()
intol_options = []
for each in intol_query:
    display_text = each[1] + ": " + each[2]
    entry = (each[0], display_text)
    intol_options.append(entry)


class ProfileData(Form):
    # email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    # password = PasswordField('Password', validators=[Required(), EqualTo('confirm', message='Passwords must match')])
    # confirm = PasswordField('Repeat Password')
    first_name = StringField('First name', nullable=True)
    last_name = StringField('Last name', nullable=True)
    diet_id = SelectField('Diet',
                          validators=[DataRequired()],
                          choices=diet_options)
    diet_reason = TextAreaField('Reason for following this diet')
    profile_notes = TextAreaField('Profile notes')
    intolerances = RadioField('Intolerances', choices=intol_options)
    avoid = StringField('Ingredients to avoid')
    reason = TextAreaField('Reason you would like to avoid this food')
    register = SubmitField('Register')
