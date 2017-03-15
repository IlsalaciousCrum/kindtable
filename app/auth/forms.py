from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError
from ..models import Profile


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired(),
                             EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Profile.query.filter(Profile.is_user_profile.is_(True),
                                Profile.email_verified.is_(True),
                                email=field.data):
            raise ValidationError('Email address already registered. Please log in.')


# class ChangePasswordForm(Form):
#     old_password = PasswordField('Old password', validators=[Required()])
#     password = PasswordField('New password', validators=[
#         Required(), EqualTo('password2', message='Passwords must match')])
#     password2 = PasswordField('Confirm new password', validators=[Required()])
#     submit = SubmitField('Update Password')


# class PasswordResetRequestForm(Form):
#     email = StringField('Email', validators=[Required(), Length(1, 64),
#                                              Email()])
#     submit = SubmitField('Reset Password')


# class PasswordResetForm(Form):
#     email = StringField('Email', validators=[Required(), Length(1, 64),
#                                              Email()])
#     password = PasswordField('New Password', validators=[
#         Required(), EqualTo('password2', message='Passwords must match')])
#     password2 = PasswordField('Confirm password', validators=[Required()])
#     submit = SubmitField('Reset Password')

#     def validate_email(self, field):
#         if User.query.filter_by(email=field.data).first() is None:
#             raise ValidationError('Unknown email address.')


# class ChangeEmailForm(Form):
#     email = StringField('New Email', validators=[Required(), Length(1, 64),
#                                                  Email()])
#     password = PasswordField('Password', validators=[Required()])
#     submit = SubmitField('Update Email Address')

#     def validate_email(self, field):
#         if User.query.filter_by(email=field.data).first():
#             raise ValidationError('Email already registered.')
