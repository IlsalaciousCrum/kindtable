from flask import render_template, redirect, url_for, flash, session, request, jsonify

from . import profiles

from .. import db

from ..models import User, Profile, Diet, Intolerance, RecipeBox, Party, PartyGuest, IngToAvoid

from flask_login import login_required

from .forms import FirstNameForm, LastNameForm, DietForm, DietReasonForm, IntoleranceForm, AvoidForm, FriendEmailForm, AddNewFriendForm

from datetime import datetime

from ..decorators import email_confirmation_required


@profiles.route('/dashboard', methods=['GET'])
@login_required
@email_confirmation_required
def show_dashboard():
    """Show logged in user's profile"""

    first_name_form = FirstNameForm(request.form)
    last_name_form = LastNameForm(request.form)
    diet_form = DietForm(request.form)
    diet_reason_form = DietReasonForm(request.form)
    avoid_form = AvoidForm(request.form)
    session_token = session.get("session_token")
    user = User.query.filter_by(session_token=session_token).first()
    friends = user.friends
    parties = user.parties
    profile = user.profile
    diets = Diet.query.order_by(Diet.diet_type).all()
    intol_list = Intolerance.query.order_by(Intolerance.intol_name).all()
    recipes = RecipeBox.query.filter_by(user_id=user.id).all()
    return render_template("/profiles/dashboard.html",
                           friends=friends,
                           parties=parties,
                           profile=profile,
                           intol_list=intol_list,
                           diets=diets,
                           recipes=recipes,
                           first_name_form=first_name_form,
                           last_name_form=last_name_form,
                           diet_form=diet_form,
                           diet_reason_form=diet_reason_form,
                           avoid_form=avoid_form)


@profiles.route('/friendprofile/<int:friend_id>', methods=['GET'])
@login_required
@email_confirmation_required
def show_friend_profile(friend_id):
    """Show logged in user's friends profile"""

    session_token = session.get("session_token")
    user = User.query.filter_by(session_token=session_token).first()
    friends = user.friends
    parties = user.parties

    newfriend = Profile.query.get(friend_id)
    diets = Diet.query.order_by(Diet.diet_type).all()
    intol_list = Intolerance.query.order_by(Intolerance.intol_name).all()
    parties = db.session.query(Party).filter(Party.party_id == PartyGuest.party_id, PartyGuest.profile_id == newfriend.profile_id).all()
    return render_template("/profiles/friends_profile_page.html",
                           newfriend=newfriend,
                           diets=diets,
                           intol_list=intol_list,
                           parties=parties,
                           friends=friends
                           )


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
        return jsonify(data=form.errors)


@profiles.route('/addavoid.json', methods=['POST'])
@login_required
@email_confirmation_required
def addavoid():
    """Takes an Ajax request and changes ingredients to avoid"""

    form = AvoidForm(request.form)
    if form.validate():
        profile = Profile.query.get(form.profile_id.data)
        IngToAvoid.create_record(ingredient=form.avoidance.data,
                                 reason=form.reason.data,
                                 profile_id=profile.profile_id)
        profile.update({"last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Ingredients to avoid updated'})
    else:
        return jsonify(data=form.errors)


@profiles.route('/updateavoid.json', methods=['POST'])
@login_required
@email_confirmation_required
def updateavoid():
    """Takes an Ajax request and updates an existing ingredient to avoid"""

    form = AvoidForm(request.form)
    if form.validate():
        profile = Profile.query.get(form.profile_id.data)
        IngToAvoid.create_record(ingredient=form.avoidance.data,
                                 reason=form.reason.data,
                                 profile_id=profile.profile_id)
        profile.update({"last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Ingredients to avoid updated'})
    else:
        return jsonify(data=form.errors)


# @profiles.route('/changeintols.json', methods=['POST'])
# @login_required
# @email_confirmation_required
# def changeintols():
#     """Takes an Ajax request and changes diet reason"""

#     form = DietReasonForm(request.form)
#     if form.validate():
#         profile = Profile.query.get(form.profile_id.data)
#         profile.update({"diet_reason": form.diet_reason.data, "last_updated": datetime.utcnow()})
#         return jsonify(data={'message': 'Diet reason updated', 'diet_reason': profile.diet_reason})
#     else:
#         return jsonify(data=form.errors)