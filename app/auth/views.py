from flask import render_template, redirect, request, url_for, flash, session

from flask_login import login_user, logout_user, login_required


from . import auth

from .. import db

from ..models import Profile, User

from .forms import LoginForm


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
            session['session_token'] = user.session_token
            return redirect(url_for('main.index'), friends=user.friends,
                            parties=user.parties)
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
