from flask import render_template, redirect, url_for, flash, session, request, jsonify

from . import profiles

from .. import db

from ..models import User, Profile, Diet, Intolerance, RecipeBox, Party, PartyGuest, IngToAvoid, ProfileIntolerance, Friend

from flask_login import login_required, current_user

from .forms import FirstNameForm, LastNameForm, DietForm, DietReasonForm, AddAvoidForm, UpdateAvoidForm, IntoleranceForm, AddToPartiesForm, DeleteFriendForm

from datetime import datetime

from ..decorators import email_confirmation_required


@profiles.route('/dashboard', methods=['GET'])
@login_required
@email_confirmation_required
def show_dashboard():
    """Show logged in user's profile"""

    session_token = session.get("session_token")
    user = User.query.filter_by(session_token=session_token).first()
    profile = user.profile

    first_name_form = FirstNameForm(request.form)
    first_name_form.first_name.data = profile.first_name
    last_name_form = LastNameForm(request.form)
    last_name_form.last_name.data = profile.last_name
    diet_form = DietForm(request.form)
    diet_reason_form = DietReasonForm(request.form)
    diet_reason_form.diet_reason.data = profile.diet_reason
    add_avoid_form = AddAvoidForm(request.form)
    update_avoid_form = UpdateAvoidForm(request.form)
    intol_form = IntoleranceForm(request.form)
    profile_intolerances = db.session.query(ProfileIntolerance).filter(Intolerance.intol_id == ProfileIntolerance.intol_id, ProfileIntolerance.profile_id == profile.profile_id).all()
    intol_form.intolerances.data = [(intol.intol_id) for intol in profile_intolerances]
    friends = user.friends
    past_parties = db.session.query(Party).filter(Party.user_id == current_user.id, Party.datetime_of_party < datetime.utcnow()).all()
    upcoming_parties = db.session.query(Party).filter(Party.user_id == current_user.id, Party.datetime_of_party >= datetime.utcnow()).all()
    diets = Diet.query.order_by(Diet.diet_type).all()
    recipes = RecipeBox.query.filter_by(user_id=user.id).all()
    return render_template("/profiles/dashboard.html",
                           friends=friends,
                           profile=profile,
                           intol_form=intol_form,
                           diets=diets,
                           recipes=recipes,
                           first_name_form=first_name_form,
                           last_name_form=last_name_form,
                           diet_form=diet_form,
                           diet_reason_form=diet_reason_form,
                           add_avoid_form=add_avoid_form,
                           update_avoid_form=update_avoid_form,
                           past_parties=past_parties,
                           upcoming_parties=upcoming_parties)


@profiles.route('/party_profile/<int:party_id>')
@login_required
@email_confirmation_required
def show_party_profile(party_id):
    """Show the party profile"""

    session_token = session.get("session_token")
    user = User.query.filter_by(session_token=session_token).first()
    this_user = user.profile
    friends = user.friends
    parties = user.parties
    session['party_id'] = party_id
    diets = Diet.query.order_by(Diet.diet_type).all()
    party = Party.query.get(party_id)
    intol_list = Intolerance.query.order_by(Intolerance.intol_name).all()

    return render_template("profiles/party_profile.html", party=party,
                           this_user=this_user,
                           diets=diets,
                           intol_list=intol_list,
                           friends=friends,
                           parties=parties)


@profiles.route('/changefirstname.json', methods=['POST'])
@login_required
@email_confirmation_required
def changefirstname():
    """Takes an Ajax request and changes a profiles first name"""

    form = FirstNameForm(request.form)
    if form.validate():
        profile = Profile.query.get(form.profile_id.data)
        profile.update({"first_name": form.first_name.data, "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'First name updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in the %s field - %s" % (
                  getattr(form, field).label.text,
                  error), 'danger')
        return jsonify(data=form.errors)


@profiles.route('/changelastname.json', methods=['POST'])
@login_required
@email_confirmation_required
def changelastname():
    """Takes an Ajax request and changes a profiles last name"""

    form = LastNameForm(request.form)
    if form.validate():
        profile = Profile.query.get(form.profile_id.data)
        profile.update({"last_name": form.last_name.data, "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Last name updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in the %s field - %s" % (
                  getattr(form, field).label.text,
                  error), 'danger')
        return jsonify(data=form.errors)


@profiles.route('/changediet.json', methods=['POST'])
@login_required
@email_confirmation_required
def changediet():
    """Takes an Ajax request and changes diet"""

    form = DietForm(request.form)
    if form.validate():
        profile = Profile.query.get(form.profile_id.data)
        profile.update({"diet_id": form.diet.data, "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Diet updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in the %s field - %s" % (
                  getattr(form, field).label.text,
                  error), 'danger')
        return jsonify(data=form.errors)


@profiles.route('/changedietreason.json', methods=['POST'])
@login_required
@email_confirmation_required
def changedietreason():
    """Takes an Ajax request and changes diet reason"""

    form = DietReasonForm(request.form)
    if form.validate():
        profile = Profile.query.get(form.profile_id.data)
        profile.update({"diet_reason": form.diet_reason.data, "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Diet reason updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in the %s field - %s" % (
                  getattr(form, field).label.text,
                  error), 'danger')
        return jsonify(data=form.errors)


@profiles.route('/intol.json', methods=['POST'])
@login_required
@email_confirmation_required
def intol():
    """Takes an Ajax request and updates intolerances"""

    form = IntoleranceForm(request.form)
    if form.validate():
        profile = Profile.query.get(form.profile_id.data)
        query = db.session.query(ProfileIntolerance).filter(ProfileIntolerance.profile_id == profile.profile_id).all()
        profile_intolerances = [(intol.intol_id) for intol in query]
        for intolerance in form.intolerances.data:
            if intolerance in profile_intolerances:
                pass
            elif intolerance not in profile_intolerances:
                ProfileIntolerance.create_record(profile_id=profile.profile_id, intol_id=intolerance)
                profile.update({"last_updated": datetime.utcnow()})
        for profile_intolerance in profile_intolerances:
            if profile_intolerance not in form.intolerances.data:
                intol = db.session.query(ProfileIntolerance).filter(ProfileIntolerance.intol_id == profile_intolerance, ProfileIntolerance.profile_id == profile.profile_id).one()
                intol.remove_intolerance()
                profile.update({"last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Intolerances updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in the %s field - %s" % (
                  getattr(form, field).label.text,
                  error), 'danger')
        return jsonify(data=form.errors)


@profiles.route('/addavoid.json', methods=['POST'])
@login_required
@email_confirmation_required
def addavoid():
    """Takes an Ajax request and adds an ingredient to avoid"""

    form = AddAvoidForm(request.form)
    if form.validate():
        already_added = db.session.query(IngToAvoid).filter(IngToAvoid.ingredient == form.add_avoid_ingredient.data).all()
        if already_added:
            flash("We already know about that ingredient to avoid. Would you like to add a different one?", "warning")
            return redirect(url_for('profiles.show_dashboard'))
        else:
            profile = Profile.query.get(form.profile_id.data)
            IngToAvoid.create_record(ingredient=form.add_avoid_ingredient.data,
                                     reason=form.add_avoid_reason.data,
                                     profile_id=profile.profile_id)
            profile.update({"last_updated": datetime.utcnow()})
            return jsonify(data={'message': 'Ingredients to avoid added'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in the %s field - %s" % (
                  getattr(form, field).label.text,
                  error), 'danger')
        return jsonify(data=form.errors)


@profiles.route('/getavoid.json', methods=['GET'])
@login_required
@email_confirmation_required
def getavoid():
    """Takes an Ajax request and returns avoidance information"""

    avoid_id = request.args.get("id")
    avoidance = IngToAvoid.query.get(avoid_id)
    return jsonify(data={'ingredient': avoidance.ingredient, 'reason': avoidance.reason})


@profiles.route('/updateavoid.json', methods=['POST'])
@login_required
@email_confirmation_required
def updateavoid():
    """Takes an Ajax request and updates an existing ingredient to avoid"""

    form = UpdateAvoidForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate():
        avoid = IngToAvoid.query.get(form.avoid_id.data)
        if form.update_avoid_ingredient:
            avoid.update({'ingredient': form.update_avoid_ingredient.data})
        if form.update_avoid_reason:
            avoid.update({'reason': form.update_avoid_reason.data})
        profile.update({"last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Ingredients to avoid updated'})
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error), 'danger')
        return jsonify(data={'errors': form.errors})


@profiles.route('/deleteavoid.json', methods=['POST'])
@login_required
@email_confirmation_required
def deleteavoid():
    """Takes an Ajax request and removes an existing ingredient to avoid"""

    form = UpdateAvoidForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate():
        avoid = IngToAvoid.query.get(form.avoid_id.data)
        avoid.remove_avoidance()
        profile.update({"last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Ingredients to avoid updated'})
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error), 'danger')
        return jsonify(data={'errors': form.errors})


@profiles.route('/friendprofile/<int:friend_id>', methods=['GET'])
@login_required
@email_confirmation_required
def show_friend_profile(friend_id):
    """Show logged in user's friends profile"""

    session_token = session.get("session_token")
    user = User.query.filter_by(session_token=session_token).first()
    friend_profile = Profile.query.get(friend_id)
    past_parties = db.session.query(Party).filter(Party.user_id == current_user.id, PartyGuest.friend_profile_id == friend_profile.profile_id, Party.datetime_of_party < datetime.utcnow()).all()
    upcoming_parties = db.session.query(Party).filter(Party.user_id == current_user.id, PartyGuest.friend_profile_id == friend_profile.profile_id, Party.datetime_of_party >= datetime.utcnow()).all()
    party_form = AddToPartiesForm(request.form)
    party_form.parties.choices = db.session.query(Party).filter(Party.user_id == current_user.id, PartyGuest.friend_profile_id != friend_profile.profile_id, Party.datetime_of_party >= datetime.utcnow()).all()
    delete_form = DeleteFriendForm(request.form)

    is_friend = db.session.query(Friend).filter(Friend.user_id == current_user.id, Friend.friend_profile_id == friend_profile.profile_id).first()

    if is_friend and friend_profile.owned_by_user_id == user.id:
        return render_template("/profiles/friend_profile_editable.html",
                               friend_profile=friend_profile,
                               past_parties=past_parties,
                               upcoming_parties=upcoming_parties,
                               invite_form=party_form,
                               profile=user.profile,
                               delete_form=delete_form)
    elif is_friend and is_friend.friendship_verified_by_email:
        return render_template("/profiles/friend_profile_fixed.html",
                               friend_profile=friend_profile,
                               past_parties=past_parties,
                               upcoming_parties=upcoming_parties,
                               invite_form=party_form,
                               profile=user.profile,
                               delete_form=delete_form)
    else:
        flash("Looks like you are not friends with that person. Do you want to add them as a friend or create a profile for them?", "danger")


@profiles.route('/addtoparty.json', methods=['POST'])
@login_required
@email_confirmation_required
def add_to_party():
    """Takes an Ajax request and adds a guest to parties"""

    form = AddToPartiesForm(request.form)
    if form.validate():
        pass
    else:
        for field, error in form.errors.items():
            flash(u"Error in the %s field - %s" % (
                  getattr(form, field).label.text,
                  error), 'danger')
        return jsonify(data=form.errors)


@profiles.route('/delete_friend.json', methods=['POST'])
@login_required
@email_confirmation_required
def delete_friend():
    """Takes an Ajax request and deletes a friend"""

    form = DeleteFriendForm(request.form)
    if form.validate():
        friend_profile = Profile.query.get(form.friend_profile_id.data)
        friendship = db.session.query(Friend).filter(Friend.user_id == current_user.id, Friend.friend_profile_id == form.friend_profile_id.data).all()
        if friend_profile.owned_by_user_id == current_user.id:
            friendship.remove_friendship()
            friend_profile.remove_profile()
        else:
            friendship.remove_friendship()
        flash("Friend removed from your account.")
        return redirect(url_for('profiles.show_dashboard'))
    else:
        for field, error in form.errors.items():
            flash(u"Error in the %s field - %s" % (
                  getattr(form, field).label.text,
                  error), 'danger')
        return jsonify(data=form.errors)
