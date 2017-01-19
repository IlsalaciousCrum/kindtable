from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email


class ProfileData(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')

    is_user_profile = db.Column(db.Boolean, unique=False, default=False)
    email = db.Column(db.String(200), nullable=False, unique=False)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    diet_id = db.Column(db.Integer, db.ForeignKey('diets.diet_id'))
    # ie, ethical, religious, general health, specific health
    diet_reason = db.Column(db.String(120), nullable=True)
    profile_notes = db.Column(db.String(300), nullable=True)
    password
    profile intolerances
    avoiding ingredience = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(200), nullable=True)
                           nullable=False)
