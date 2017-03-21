'''Views related to user management tasks'''

from flask import render_template, redirect, url_for, flash, session, request

from flask_login import login_user, logout_user, login_required

from . import auth

from .. import db

from ..email import send_email

from ..models import Profile, User, Diet

from .forms import LoginForm, RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''Loads the login form on GET and processes the form on POST'''
    login_form = LoginForm(request.form)
    print login_form.email.data
    print login_form.password.data

    if request.method == 'POST' and login_form.validate():
        print 1
        # user = db.session.query(User).join(Profile).filter(Profile.email == login_form.email.data, Profile.owned_by_user_id == User.profile_id).first()

        user = db.session.query(User).join(Profile).filter(Profile.email == login_form.email.data, User.profile_id == Profile.profile_id).first()

        print user
        print 2
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember_me.data)
            print 5
            user.make_session_token()
            print "Session token is " + str(user.session_token)
            session['session_token'] = user.session_token
            print 6
            flash('You are now logged in', 'success')
            return redirect(url_for('main.index'))
        else:
            print 4
            flash('Invalid username or password.', 'danger')
            return render_template('auth/login.html', form=login_form)
    else:
        return render_template('auth/login.html', form=login_form)


@auth.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()

    return redirect(url_for('main.index'))


@auth.route('/update')
def temp():
    try:
        my_profile = Profile.query.get('1').first()
        my_profile.update(Profile.email, "me@me.com")
        html = "<html><body>success</body></html>"
        return html
    except:
        html = "<html><body>Nope, no good</body></html>"
        return html


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    print 12

    if request.method == 'POST' and form.validate():
        print form.first_name.data
        print form.last_name.data
        print form.email.data
        print form.diet.data
        print form.diet_reason.data
        print form.password.data

        profile = Profile.create_record(email=form.email.data,
                                        first_name=form.first_name.data,
                                        last_name=form.last_name.data,
                                        diet_id=int(form.diet.data),
                                        diet_reason=form.diet_reason.data)

        user = User.create_record(profile_id=profile.profile_id,
                                  password=form.password.data)
        profile.owned_by_user_id = user.id
        db.session.commit()
        print 15
        token = profile.generate_confirmation_token()
        print 16

        send_email(to=profile.email, subject=' Confirm Your Account',
                   template='auth/email/confirm', profile=profile, token=token)
        print 17
        flash('Please check your email for instructions on completing registration.', "success")
        return redirect(url_for('auth.login'))
    diets = Diet.query.order_by(Diet.diet_type).all()
    return render_template('auth/register.html', form=form, diets=diets)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):

    if Profile.confirm(token):
        flash('You have confirmed your account.Thanks!', 'success')
    return redirect(url_for('main.index'))
