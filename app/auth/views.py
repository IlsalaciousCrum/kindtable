'''Views related to user management tasks'''

from flask import render_template, redirect, url_for, flash, session, request, jsonify

from flask_login import login_user, logout_user, login_required, current_user

from . import auth

from .. import db

from ..email import send_email

from ..models import Profile, User, Diet, ProfileIntolerance, IngToAvoid, Friend, Intolerance

from ..decorators import flash_errors

from .forms import (LoginForm,
                    RegistrationForm,
                    PasswordResetRequestForm,
                    PasswordResetForm,
                    ChangeEmailForm,
                    RegUpdateAvoidForm,
                    RegAddAvoidForm,
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
        if user is None:
            flash('You are not registered under that email address. Try again or register as a new user.')
            return redirect(request.args.get('next') or url_for('main.index'))
        elif user is not None and user.verify_password(login_form.password.data):
            login_user(user)
            session['timezone'] = str(login_form.timezone.data)
            session['session_token'] = user.session_token
            flash('You are now logged in', 'success')
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(request.args.get('next') or url_for('auth.login'))
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
    else:
        return render_template('auth/reset_password_from_email.html', form=form)


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

    session['intol_dict'] = {}
    print intol_form.intolerances.data
    intol_dict = session['intol_dict']
    print intol_dict
    if intol_form.validate():
        for intol in intol_form.intolerances.data:
            desc = Intolerance.query.get(intol)
            print desc
            intol_dict[intol] = {desc.intol_name: desc.intol_description}
            print intol_dict
    return jsonify(data={'message': 'Intols saved'})


@auth.route('/add_avoid.json', methods=['POST'])
def store_avoid():
    '''Store ingredients to avoid and the reason, for registration'''

    add_avoid_form = RegAddAvoidForm(request.form)
    if add_avoid_form.validate():
        avoid_dict = session['avoid_dict']
        avoid_dict[add_avoid_form.add_avoid_ingredient.data
                   ] = add_avoid_form.add_avoid_reason.data
        session.modified = True
        return jsonify(data={'message': 'avoid saved'})


@auth.route('/update_avoid.json', methods=['POST'])
def update_stored_avoid():
    '''Store ingredients to avoid and the reason, for registration'''

    update_avoid_form = RegUpdateAvoidForm(request.form)
    if update_avoid_form.validate():
        avoid_dict = session['avoid_dict']
        del avoid_dict[update_avoid_form.update_avoid_key.data]
        avoid_dict[update_avoid_form.update_avoid_key.data
                   ] = update_avoid_form.update_avoid_value.data
        session.modified = True
    return jsonify(data={'message': 'avoid updated'})


@auth.route('/delete_ingredient.json', methods=['POST'])
def delete_stored_ingredient():
    '''Delete ingredient to avoid, for registration'''

    update_avoid_form = RegUpdateAvoidForm(request.form)
    if update_avoid_form.validate():
        avoid_dict = session['avoid_dict']
        del avoid_dict[update_avoid_form.original_key.data]
        session.modified = True
    return jsonify(data={'message': 'avoid updated'})


@auth.route('/delete_reason.json', methods=['POST'])
def delete_stored_reason():
    '''Delete reason for avoiding ingredient, for registration'''

    update_avoid_form = RegUpdateAvoidForm(request.form)
    if update_avoid_form.validate():
        avoid_dict = session['avoid_dict']
        avoid_dict[update_avoid_form.original_key.data] = ""
        session.modified = True
    return jsonify(data={'message': 'avoid updated'})


@auth.route('/register', methods=['GET', 'POST'])
def register():
    '''Register a new user'''

    # existing user validation in the form

    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        profile = Profile.query.filter(Profile.owned_by_user_id == None, Profile.email == form.email.data).first()
        if profile:
            profile.first_name = form.first_name.data
            profile.last_name = form.last_name.data
            profile.diet_id = form.diet.data,
            profile.diet_reason = form.diet_reason.data
            db.session.commit()
        else:
            profile = Profile.create_record(email=email.lower(),
                                            first_name=form.first_name.data,
                                            last_name=form.last_name.data,
                                            diet_id=form.diet.data,
                                            diet_reason=form.diet_reason.data)
        user = User.create_record(profile_id=profile.profile_id,
                                  password=form.password.data)
        intolerances = session['intol_dict']
        if intolerances:
            for intol in intolerances:
                intol = ProfileIntolerance.create_record(profile_id=profile.profile_id,
                                                         intol_id=intol)
                print intol
        avoidances = session['avoid_dict']
        if avoidances:
            for key, value in session['avoid_dict'].iteritems():
                IngToAvoid.create_record(ingredient=key,
                                         reason=value,
                                         profile_id=profile.profile_id)
        user.make_session_token()
        profile.owned_by_user_id = user.id
        db.session.commit()
        token = profile.generate_confirmation_token()
        send_email(to=profile.email, subject=' Confirm Your Account',
                   template='auth/email/confirm', profile=profile, token=token)
        flash('Please check your email for instructions on completing\
              registration.', "success")
        return redirect(url_for('auth.login'))
    if request.method == 'POST' and not form.validate():
        flash_errors(form)
        return redirect(url_for('auth.register'))
    try:
        session['avoid_dict']
    except:
        session['avoid_dict'] = {}
    try:
        session['intol_dict']
    except:
        session['intol_dict'] = {}

    diets = Diet.query.order_by(Diet.diet_type).all()
    add_avoid_form = RegAddAvoidForm(request.form)
    update_avoid_form = RegUpdateAvoidForm(request.form)
    intol_form = IntoleranceForm(request.form)
    intol_dict = session['intol_dict']
    intol_form.intolerances.data = [(int(item)) for item in intol_dict]

    return render_template('auth/register.html',
                           form=form,
                           diets=diets,
                           add_avoid_form=add_avoid_form,
                           update_avoid_form=update_avoid_form,
                           intol_form=intol_form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):

    confirm = current_user.profile.confirm(token)
    currentuser = current_user

    if current_user.profile.email_verified:
        return redirect(url_for('main.index'))
    elif type(confirm) is dict:
        profile = Profile.query.get(confirm['profile_id'])
        if profile.email == confirm['email']:
            token = profile.generate_confirmation_token()
            send_email(to=profile.email, subject=' Confirm Your Account',
                       template='auth/email/confirm', profile=profile, token=token)
            flash('That confirmation email is more than 24 hours old. I just \
                sent you a new one. Please check your email account again and \
                follow the instructions in the email')
    elif currentuser == confirm:
        flash("Thank you for confirming your account, enjoy the app!")
        confirm.profile.email_verified = True
        db.session.commit()
    else:
        flash('The confirmation link is invalid.')
    return redirect(url_for('main.index'))


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email():
    """Takes an Ajax request and changes a user's email address, requires
    the user to reconfim their account"""

    form = ChangeEmailForm(request.form)
    if request.method == 'POST' and form.validate():
        if current_user.verify_password(form.password.data):
            profile = current_user.profile
            email = form.email.data
            profile.update({'email': email.lower(),
                            'email_verified': False,
                            'last_updated': datetime.utcnow()})
            token = profile.generate_confirmation_token()
            send_email(to=profile.email, subject=' Confirm your new email address',
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

    # TODO - this code sequence could potentially be shortened by using cascade="all,delete"
    # on the model but perfect is the enemy of done.

    this_user = current_user
    if this_user.friends:
        for friend in this_user.friend:
            friend.remove_friendship()

    friendship = Friend.query.filter(Friend.friend_profile_id == this_user.profile.profile_id).all()
    if friendship:
        for friend in friendship:
            friend.remove_friendship()

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
