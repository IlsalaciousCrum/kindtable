from flask import render_template, redirect, url_for, flash, session, request, jsonify

from . import profiles

from .. import db

from ..models import User, Profile, Diet, Intolerance, RecipeBox, Party, PartyGuest

from flask_login import login_required

from .forms import FirstNameForm, LastNameForm, DietForm, DietReasonForm, IntoleranceForm, AvoidForm, FriendEmailForm, AddNewFriendForm

from datetime import datetime


@profiles.route('/dashboard', methods=['GET'])
@login_required
def show_dashboard():
    """Show logged in user's profile"""

    first_name_form = FirstNameForm(request.form)
    last_name_form = LastNameForm(request.form)
    session_token = session.get("session_token")
    user = User.query.filter_by(session_token=session_token).first()
    friends = user.friends
    parties = user.parties
    profile = user.profile
    diets = Diet.query.order_by(Diet.diet_type).all()
    intol_list = Intolerance.query.order_by(Intolerance.intol_name).all()
    recipes = RecipeBox.query.filter_by(user_id=user.id).all()
    return render_template("/profiles/user_profile.html",
                           friends=friends,
                           parties=parties,
                           profile=profile,
                           intol_list=intol_list,
                           diets=diets,
                           recipes=recipes,
                           first_name_form=first_name_form,
                           last_name_form=last_name_form)


@profiles.route('/friendprofile/<int:friend_id>', methods=['GET'])
@login_required
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
def changefirstname():
    """Takes an Ajax request and changes a profiles first name"""

    form = FirstNameForm(request.form)
    if form.validate():
        profile = Profile.query.get(form.profile_id.data)
        profile.update({"first_name": form.first_name.data, "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'First name updated', 'first_name': profile.first_name})
    else:
        return jsonify(data=form.errors)


@profiles.route('/changelastname.json', methods=['POST'])
@login_required
def changelastname():
    """Takes an Ajax request and changes a profiles last name"""

    form = LastNameForm(request.form)
    if form.validate():
        profile = Profile.query.get(form.profile_id.data)
        profile.update({"last_name": form.last_name.data, "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Last name updated', 'last_name': profile.last_name})
    else:
        return jsonify(data=form.errors)
