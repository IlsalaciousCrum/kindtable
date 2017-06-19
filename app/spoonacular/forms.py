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


# placeholder for forms I have not created yet