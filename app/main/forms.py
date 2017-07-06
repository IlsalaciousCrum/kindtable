'''WTForms forms for app data collection'''

from wtforms import Form
from wtforms import StringField
from wtforms.validators import InputRequired, Length, Email
from wtforms.widgets import TextArea


class BetaAccessForm(Form):
    full_name = StringField('Full name',
                            validators=[InputRequired(message="Please tell us who you are."),
                                        Length(1, 64, message="Limit 64 characters")])
    email_address = StringField('Email',
                                validators=[InputRequired('Email address is a required field.'),
                                            Length(1, 64),
                                            Email('A valid email address is required.')])
    reason = StringField('Reason for access',
                         widget=TextArea(),
                         validators=[Length(1, 300, message="Limit 300 characters")])
