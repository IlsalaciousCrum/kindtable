'''Views related to user management tasks'''

from flask import render_template, redirect, url_for, flash, session, request, jsonify

from flask_login import login_user, logout_user, login_required, current_user

from . import auth

from .. import db

from ..email import send_email

from ..models import Profile, User, Diet, ProfileIntolerance, IngToAvoid, PartyGuest, Friend

from ..decorators import flash_errors

from .forms import (LoginForm,
                    RegistrationForm,
                    PasswordResetRequestForm,
                    PasswordResetForm,
                    ChangeEmailForm,
                    UpdateAvoidForm,
                    AddAvoidForm,
                    IntoleranceForm)

from datetime import datetime


@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''Loads the login and password reset forms'''

    login_form = LoginForm(request.form, prefix="b")
    reset_password_request_form = PasswordResetRequestForm(request.form,
                                                           prefix="a")

    if request.method == 'POST' and login_form.validate():
        email = login_form.email.data
        user = db.session.query(User).join(Profile).filter(Profile.email ==
                                                           email.lower(),
                                                           User.profile_id ==
                                                           Profile.profile_id).first()
        if user is not None and user.verify_password(login_form.password.data):
            session['remember_me'] = login_form.remember_me.data
            login_user(user, remember=login_form.remember_me.data)
            session['timezone'] = str(login_form.timezone.data)
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

    reset_password_request_form = PasswordResetRequestForm(request.form,
                                                           prefix="a")
    if request.method == 'POST' and reset_password_request_form.validate():
        if not current_user.is_anonymous:
            print "a user is already logged in"
            return redirect(url_for('main.index'))
        email = reset_password_request_form.email.data
        user = db.session.query(User).join(Profile).filter(Profile.email ==
                                                           email.lower(),
                                                           User.profile_id ==
                                                           Profile.profile_id).first()
        profile = user.profile
        if user:
            token = profile.generate_confirmation_token()
            send_email(to=profile.email, subject=' Reset your password',
                       template='auth/email/reset_password',
                       profile=profile, token=token)
            flash('An email with instructions to reset your password\
             has been sent to you.', "success")
            return redirect(url_for('auth.login'))
        else:
            flash('That email is not registered, please try another email\
                   address or register.', "danger")
            return redirect(url_for('auth.login'))
    else:
        flash('That email is not registered, please try another email\
               address or register.', "danger")
        return redirect(url_for('auth.login'))


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        user = db.session.query(User).join(Profile
                                           ).filter(Profile.email ==
                                                    email.lower(),
                                                    User.profile_id ==
                                                    Profile.profile_id).first()
        if user is None:
            flash('You have entered an incorrect email address.\
                  Please follow the link from your email again')
            return redirect(url_for('main.index'))
        if user.reset_password(token=token, new_password=form.password.data):
            flash('Your password has been updated.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash("Something weird has happened", "danger")
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash("You are now logged out")
    return redirect(url_for('main.index'))


@auth.route('/add_intols.json', methods=['POST'])
def store_intols():
    '''Store allergies/intolerances for registration'''

    intol_form = IntoleranceForm(request.form)
    if intol_form.validate():
        session['intolerances'] = {'intols': intol_form.intolerances.data}
    return jsonify(data={'message': 'Intols saved'})


@auth.route('/add_avoid.json', methods=['POST'])
def store_avoid():
    '''Store ingredients to avoid and the reason, for registration'''

    add_avoid_form = AddAvoidForm(request.form)
    if add_avoid_form.validate():
        print add_avoid_form.add_avoid_ingredient.data
        print add_avoid_form.add_avoid_reason.data

        avoid_dict = session['avoid_dict']
        print avoid_dict

        avoid_dict[add_avoid_form.add_avoid_ingredient.data
                   ] = add_avoid_form.add_avoid_reason.data
        session.modified = True
        print avoid_dict
        print session['avoid_dict']
        return jsonify(data={'message': 'avoid saved'})


@auth.route('/update_avoid.json', methods=['POST'])
def update_stored_avoid():
    '''Store ingredients to avoid and the reason, for registration'''

    update_avoid_form = UpdateAvoidForm(request.form)
    if update_avoid_form.validate():
        print update_avoid_form.original_key.data
        print update_avoid_form.update_avoid_key.data
        print update_avoid_form.update_avoid_value.data

        avoid_dict = session['avoid_dict']
        del avoid_dict[update_avoid_form.update_avoid_key.data]
        avoid_dict[update_avoid_form.update_avoid_key.data
                   ] = update_avoid_form.update_avoid_value.data
        session.modified = True
    return jsonify(data={'message': 'avoid updated'})


@auth.route('/delete_ingredient.json', methods=['POST'])
def delete_stored_ingredient():
    '''Delete ingredient to avoid, for registration'''

    update_avoid_form = UpdateAvoidForm(request.form)
    if update_avoid_form.validate():
        print update_avoid_form.original_key.data
        print update_avoid_form.update_avoid_key.data
        print update_avoid_form.update_avoid_value.data

        avoid_dict = session['avoid_dict']
        del avoid_dict[update_avoid_form.original_key.data]
        session.modified = True
    return jsonify(data={'message': 'avoid updated'})


@auth.route('/delete_reason.json', methods=['POST'])
def delete_stored_reason():
    '''Delete reason for avoiding ingredient, for registration'''

    update_avoid_form = UpdateAvoidForm(request.form)
    if update_avoid_form.validate():
        print update_avoid_form.original_key.data
        print update_avoid_form.update_avoid_key.data
        print update_avoid_form.update_avoid_value.data

        avoid_dict = session['avoid_dict']
        avoid_dict[update_avoid_form.original_key.data] = ""
        session.modified = True
    return jsonify(data={'message': 'avoid updated'})


@auth.route('/register', methods=['GET', 'POST'])
def register():
    '''Register a new user'''

    print 1
    form = RegistrationForm(request.form)

    print 2

    if request.method == 'POST' and form.validate():
        print 3
        email = form.email.data
        print 4
        profile = Profile.create_record(email=email.lower(),
                                        first_name=form.first_name.data,
                                        last_name=form.last_name.data,
                                        diet_id=form.diet.data,
                                        diet_reason=form.diet_reason.data)
        print 5
        user = User.create_record(profile_id=profile.profile_id,
                                  password=form.password.data)
        print 6
        if session['intolerances']['intols']:
            for intolerance in session['intolerances']['intols']:
                ProfileIntolerance.create_record(profile_id=profile.profile_id,
                                                 intol_id=intolerance)
        print 7
        avoidances = session['avoid_dict']
        if avoidances:
            for key, value in session['avoid_dict'].iteritems():
                IngToAvoid.create_record(ingredient=key,
                                         reason=value,
                                         profile_id=profile.profile_id)
        print 8
        user.make_session_token()
        print 9
        profile.owned_by_user_id = user.id
        print 10
        db.session.commit()
        print 11
        token = profile.generate_confirmation_token()
        print 12
        send_email(to=profile.email, subject=' Confirm Your Account',
                   template='auth/email/confirm', profile=profile, token=token)
        print 13
        flash('Please check your email for instructions on completing\
              registration.', "success")
        print 14
        return redirect(url_for('auth.login'))
    if request.method == 'POST' and not form.validate():
        flash_errors(form)
        return redirect(url_for('auth.register'))
    try:
        session['avoid_dict']
        print 15
    except:
        session['avoid_dict'] = {}
        print 16
    try:
        session['intolerances']
        print 17
    except:
        session['intolerances'] = {}
        print 18

    print 19
    diets = Diet.query.order_by(Diet.diet_type).all()
    print 20
    add_avoid_form = AddAvoidForm(request.form)
    print 21
    update_avoid_form = UpdateAvoidForm(request.form)
    print 22
    intol_form = IntoleranceForm(request.form)
    print 23
    return render_template('auth/register.html',
                           form=form,
                           diets=diets,
                           add_avoid_form=add_avoid_form,
                           update_avoid_form=update_avoid_form,
                           intol_form=intol_form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):

    if current_user.profile.email_verified:
        print "thinks the user is already confirmed"
        return redirect(url_for('main.index'))
    elif current_user.profile.confirm(token):
        print "we passed the confirmation "
        flash('You have confirmed your account. Thanks!', 'success')
    else:
        flash('The confirmation link is invalid.', 'danger')

    return redirect(url_for('main.index'))


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email():
    """Takes an Ajax request and changes a user's email address, requires
    the user to reconfim their account"""

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
            flash('An email with instructions for confirming your new email address\
                  has been sent to you.', "success")
            return redirect(url_for('auth.login'))
        else:
            flash('Incorrect password. Please reenter your password.', "danger")
            render_template('auth/change_email.html',
                            form=form,
                            profile_id=current_user.profile.profile_id)
    return render_template('auth/change_email.html',
                           form=form,
                           profile_id=current_user.profile.profile_id)


@auth.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    """Deletes a user's account and all of their data"""

    this_user = current_user

    if this_user.friends:
        for friend in this_user.friends:
            friend.remove_friendship()

    friendship = Friend.query.filter(Friend.friend_profile_id == this_user.profile.profile_id).all()
    if friendship:
        for friend in friendship:
            friend.remove_friendship()

    private_profiles = Profile.query.filter(Profile.owned_by_user_id == this_user.id).all()
    if private_profiles:
        for profile in private_profiles:
            _intolerances = ProfileIntolerance.query.filter(ProfileIntolerance.profile_id == profile.profile_id).all()
            if _intolerances:
                for intolerance in _intolerances:
                    intolerance._delete_()
            if profile.avoidances:
                for ingredient in profile.avoidances:
                    ingredient._delete_()

            parties_invited = PartyGuest.query.filter(PartyGuest.friend_profile_id == profile.profile_id).all()
            if parties_invited:
                for party in parties_invited:
                    party.discard_party()
            if profile.avoidances:
                for ingredient in profile.avoidances:
                    ingredient._delete_()

    if this_user.parties:
        for party in this_user.parties:
            party.discard_party()

    user_id = this_user.id

    this_user._delete_()

    private_profiles = Profile.query.filter(Profile.owned_by_user_id == user_id).all()
    if private_profiles:
        for profile in private_profiles:
            profile.remove_profile()

    logout_user()
    session.clear()
    return redirect(url_for('main.index'))
