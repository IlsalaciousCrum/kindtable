from flask import render_template, redirect, url_for, flash, session, request

from . import profiles

from .. import db

from ..models import User, Profile, Diet, Intolerance, RecipeBox, Party, PartyGuest

from flask_login import login_required


@profiles.route('/userprofile', methods=['GET'])
@login_required
def show_user_profile():
    """Show logged in user's profile"""

    print 1
    session_token = session.get("session_token")
    print session_token
    user = User.query.filter(session_token == session_token).first()
    print user
    friends = user.friends
    print friends
    parties = user.parties
    print parties
    profile = Profile.query.filter(Profile.owned_by_user_id == user.id).first()
    print profile
    diets = Diet.query.order_by(Diet.diet_type).all()
    print diets
    intol_list = Intolerance.query.order_by(Intolerance.intol_name).all()
    print intol_list
    recipes = RecipeBox.query.filter_by(user_id=user.id).all()
    return render_template("/profiles/user_profile.html",
                           friends=friends,
                           parties=parties,
                           profile=profile,
                           intol_list=intol_list,
                           diets=diets,
                           recipes=recipes)


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
