from flask import render_template, redirect, url_for, flash, session

from flask_login import login_user, logout_user, login_required

from . import auth

from .. import db

from ..email import send_email

from ..models import Profile, User, Diet

from .forms import LoginForm, RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print form.email.data
    print form.password.data
    if form.validate_on_submit():
        print 1
        user = db.session.query(User).join(Profile).filter(Profile.email == form.email.data, Profile.is_user_profile.is_(True)).first()
        print 2
        if user is not None and user.verify_password(form.password.data):
            print 3
            login_user(user, form.remember_me.data)
            print 5
            session['session_token'] = user.session_token
            print 6
            return redirect(url_for('main.index'))
        else:
            print 4
            flash('Invalid username or password.')
            render_template('auth/login.html', form=form)
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    diets = Diet.query.order_by(Diet.diet_type).all()
    if form.validate_on_submit():
        profile = User.create(email=form.email.data,
                              first_name=form.first_name.data,
                              last_name=form.last_name.data,
                              diet_id=form.diet.data,
                              reason=form.diet_reason.data)
        user = User.create(profile_id=profile.profile_id,
                           password=form.password.data,
                           created_by_email_owner=True,
                           is_user_profile=True)
        token = user.generate_confirmation_token()
        send_email(to=profile.email, subject='Confirm Your Account',
                   template='auth/email/confirm', profile=profile, token=token)
        flash('Please check your email for instructions on completing registration.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, diets=diets)
