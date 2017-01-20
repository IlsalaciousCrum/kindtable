from flask import render_template, redirect, request, url_for, flash

from flask_login import login_user, logout_user, login_required

from . import auth

from .. import db

from ..models import Profile

from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print form.email.data
    print form.password.data
    if form.validate_on_submit():
        user_profile = Profile.query.filter_by(email=form.email.data, is_user_profile=True).first()
        # user_profile = db.session.query(Profile).filter(Profile.email == form.email.data, Profile.is_user_profile is True).first()
        user = user_profile.user
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
            flash('Invalid username or password.')
    else:
        return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
