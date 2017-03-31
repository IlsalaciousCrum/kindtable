'''Views related to user management tasks'''

from flask import render_template, redirect, url_for, flash, session, request, current_app

from flask_login import login_user, logout_user, login_required, current_user

from . import auth

from .. import db

from ..email import send_email

from ..models import Profile, User, Diet

from .forms import LoginForm, RegistrationForm, PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm

from datetime import datetime


@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''Loads the login and password reset forms'''

    login_form = LoginForm(request.form, prefix="b")
    reset_password_request_form = PasswordResetRequestForm(request.form, prefix="a")

    if request.method == 'POST' and login_form.validate():
        email = login_form.email.data
        user = db.session.query(User).join(Profile).filter(Profile.email == email.lower(), User.profile_id == Profile.profile_id).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, remember=login_form.remember_me.data)
            session['session_token'] = user.session_token
            flash('You are now logged in', 'success')
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html',
                           login_form=login_form,
                           reset_password_request_form=reset_password_request_form)


@auth.route('/process_reset', methods=['POST'])
def process_reset():
    '''Starts the password reset process'''

    reset_password_request_form = PasswordResetRequestForm(request.form, prefix="a")
    if request.method == 'POST' and reset_password_request_form.validate():
        if not current_user.is_anonymous:
            print "a user is already logged in"
            return redirect(url_for('main.index'))
        email = reset_password_request_form.email.data
        user = db.session.query(User).join(Profile).filter(Profile.email == email.lower(), User.profile_id == Profile.profile_id).first()
        profile = user.profile
        if user:
            token = profile.generate_confirmation_token()
            send_email(to=profile.email, subject=' Reset your password',
                       template='auth/email/reset_password', profile=profile, token=token)
            flash('An email with instructions to reset your password has been sent to you.', "success")
            return redirect(url_for('auth.login'))
        else:
            flash('That email is not registered, please try another email address or register.')
            return redirect(url_for('auth.login'))
    else:
        flash('That email is not registered, please try another email address or register.')
        return redirect(url_for('auth.login'))


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        user = db.session.query(User).join(Profile).filter(Profile.email == email.lower(), User.profile_id == Profile.profile_id).first()
        if user is None:
            flash('You have entered an incorrect email address. Please follow the link from your email again')
            return redirect(url_for('main.index'))
        if user.reset_password(token=token, new_password=form.password.data):
            flash('Your password has been updated.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash("Something weird has happened")
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()

    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        email = form.email.data
        profile = Profile.create_record(email=email.lower(),
                                        first_name=form.first_name.data,
                                        last_name=form.last_name.data,
                                        diet_id=int(form.diet.data),
                                        diet_reason=form.diet_reason.data)

        user = User.create_record(profile_id=profile.profile_id,
                                  password=form.password.data)
        user.make_session_token()
        profile.owned_by_user_id = user.id
        db.session.commit()
        token = profile.generate_confirmation_token()
        send_email(to=profile.email, subject=' Confirm Your Account',
                   template='auth/email/confirm', profile=profile, token=token)
        flash('Please check your email for instructions on completing registration.', "success")
        return redirect(url_for('auth.login'))
    diets = Diet.query.order_by(Diet.diet_type).all()
    return render_template('auth/register.html', form=form, diets=diets)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):

    if current_user.profile.email_verified:
        print "thinks the user is already confirmed"
        return redirect(url_for('main.index'))
    elif current_user.profile.confirm(token):
        print "we passed the confirmation "
        flash('You have confirmed your account.Thanks!', 'success')
    else:
        flash('The confirmation link is invalid.', 'danger')

    return redirect(url_for('main.index'))


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email():
    """Takes an Ajax request and changes a user's email address, requires the user to reconfim their account"""

    form = ChangeEmailForm(request.form)
    if request.method == 'POST' and form.validate():
        print "The form validates"
        if current_user.verify_password(form.password.data):
            print "verified the password"
            profile = current_user.profile
            email = form.email.data
            profile.update({'email': email.lower(),
                            'email_verified': False,
                            'last_updated': datetime.utcnow()})
            token = profile.generate_confirmation_token()
            send_email(to=profile.email, subject='Confirm your new email address',
                       template='auth/email/confirm', profile=profile, token=token)
            session.clear()
            logout_user()
            flash('An email with instructions to reset your password has been sent to you.', "success")
            return redirect(url_for('auth.login'))
        else:
            flash('Incorrect password. Please reenter your password.')
            render_template('auth/change_email.html',
                            form=form,
                            profile_id=current_user.profile.profile_id)
    return render_template('auth/change_email.html',
                           form=form,
                           profile_id=current_user.profile.profile_id)
