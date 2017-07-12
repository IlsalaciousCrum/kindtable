"""K(i)nd app views for the 'profiles' blueprint"""


from flask import (render_template, redirect, url_for, flash, session,
                   request, jsonify, abort)

from . import profiles

from .. import db

from ..models import (User, Profile, Intolerance, Party, PartyGuest,
                      IngToAvoid, ProfileIntolerance, Friend)

from flask_login import login_required, current_user

from .forms import (FirstNameForm, LastNameForm, DietForm, DietReasonForm,
                    AddAvoidForm, UpdateAvoidForm, IntoleranceForm,
                    AddNewPartyForm, DeleteFriendForm, ChangeFriendEmailForm,
                    FriendNotesForm, FindaFriendForm,
                    ManageGuestListForm, PartyTitleForm, PartyDatetimeForm,
                    PartyNotesForm, DeletePartyForm, InviteForm,
                    ChangePrivateProfileTitleForm, PrivateProfileTitleForm,
                    DeletePrivateProfileForm)

from datetime import datetime

from ..decorators import email_confirmation_required, flash_errors

from ..functions import (guest_avoidances, guest_intolerances)

from ..email import send_email

import pytz

import json

from pytz import timezone


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
    diet_form.diet.data = profile.diet_id
    diet_reason_form = DietReasonForm(request.form)
    diet_reason_form.diet_reason.data = profile.diet_reason
    add_avoid_form = AddAvoidForm(request.form)
    update_avoid_form = UpdateAvoidForm(request.form)
    intol_form = IntoleranceForm(request.form)
    profile_intolerances = db.session.query(ProfileIntolerance
                                            ).filter(Intolerance.intol_id ==
                                                     ProfileIntolerance.intol_id,
                                                     ProfileIntolerance.profile_id ==
                                                     profile.profile_id).all()
    intol_form.intolerances.data = [(intol.intol_id)
                                    for intol in profile_intolerances]
    past_parties = db.session.query(Party).filter(Party.user_id ==
                                                  current_user.id,
                                                  Party.datetime_of_party
                                                  < datetime.utcnow()).order_by(Party.datetime_of_party).all()
    upcoming_parties = db.session.query(Party).filter(Party.user_id ==
                                                      current_user.id,
                                                      Party.datetime_of_party >=
                                                      datetime.utcnow()).order_by(Party.datetime_of_party).all()

    return render_template("/profiles/dashboard.html",
                           profile=profile,
                           intol_form=intol_form,
                           first_name_form=first_name_form,
                           last_name_form=last_name_form,
                           diet_form=diet_form,
                           diet_reason_form=diet_reason_form,
                           add_avoid_form=add_avoid_form,
                           update_avoid_form=update_avoid_form,
                           past_parties=past_parties,
                           upcoming_parties=upcoming_parties)


@profiles.route('/friendprofile/<int:friend_id>', methods=['GET'])
@login_required
@email_confirmation_required
def show_friend_profile(friend_id):
    """Show logged in user's friends profile"""

    user = current_user

    is_friend = Friend.query.filter(Friend.user_id ==
                                    user.id,
                                    Friend.friend_profile_id ==
                                    friend_id).first()

    friend_profile = Profile.query.get(friend_id)

    parties = Party.query.filter(Party.user_id == current_user.id).all()

    inviteform = InviteForm(request.form)

    upcoming_parties = db.session.query(Party).filter(Party.user_id == current_user.id,
                                                      Party.datetime_of_party >= datetime.utcnow()).all()

    upcoming_parties_invited_to = db.session.query(Party).join(PartyGuest).filter(Party.user_id == current_user.id,
                                                                                  Party.datetime_of_party >= datetime.utcnow(),
                                                                                  PartyGuest.friend_profile_id == friend_id).order_by(Party.datetime_of_party).all()

    inviteform.parties.choices = [(party.party_id, party.title) for party in upcoming_parties]

    inviteform.parties.data = [party.party_id for party in upcoming_parties_invited_to]

    if is_friend:
        parties_invited = db.session.query(Party).join(PartyGuest).filter(Party.user_id == current_user.id,
                                                                          PartyGuest.friend_profile_id == friend_id).all()
        email_form = ChangeFriendEmailForm(request.form)
        notes_form = FriendNotesForm(request.form)
        notes_form.notes.data = is_friend.friend_notes

        if friend_profile.owned_by_user_id == current_user.id:
            diet_form = DietForm(request.form)
            deleteppform = DeletePrivateProfileForm(request.form)
            diet_reason_form = DietReasonForm(request.form)
            diet_reason_form.diet_reason.data = friend_profile.diet_reason
            add_avoid_form = AddAvoidForm(request.form)
            update_avoid_form = UpdateAvoidForm(request.form)
            intol_form = IntoleranceForm(request.form)
            title_form = ChangePrivateProfileTitleForm(request.form)
            title_form.title.data = friend_profile.private_profile_title
            profile_intolerances = db.session.query(ProfileIntolerance
                                                    ).filter(Intolerance.intol_id ==
                                                             ProfileIntolerance.intol_id,
                                                             ProfileIntolerance.profile_id ==
                                                             friend_profile.profile_id).all()
            intol_form.intolerances.data = [(intol.intol_id) for intol in profile_intolerances]

            now = datetime.now(pytz.utc)

            return render_template("/profiles/friend_profile_editable.html",
                                   profile_id=current_user.profile.profile_id,
                                   friend_profile=friend_profile,
                                   parties_invited=parties_invited,
                                   profile=current_user.profile,
                                   deleteppform=deleteppform,
                                   intol_form=intol_form,
                                   diet_form=diet_form,
                                   diet_reason_form=diet_reason_form,
                                   add_avoid_form=add_avoid_form,
                                   update_avoid_form=update_avoid_form,
                                   email_form=email_form,
                                   friend_profile_notes=is_friend.friend_notes,
                                   notes_form=notes_form,
                                   now=now,
                                   parties=parties,
                                   inviteform=inviteform,
                                   upcoming_parties=upcoming_parties,
                                   title_form=title_form)
        elif is_friend and is_friend.friendship_verified_by_email:
            now = datetime.now(pytz.utc)
            delete_form = DeleteFriendForm(request.form)
            return render_template("/profiles/friend_profile_fixed.html",
                                   profile_id=current_user.profile.profile_id,
                                   friend_profile=friend_profile,
                                   parties_invited=parties_invited,
                                   profile=current_user.profile,
                                   delete_form=delete_form,
                                   notes_form=notes_form,
                                   friend_profile_notes=is_friend.friend_notes,
                                   now=now,
                                   parties=parties,
                                   inviteform=inviteform,
                                   upcoming_parties=upcoming_parties)
    else:
        flash("Looks like you are trying to view the profile of someone you are not\
              friends with. Do you want to create your own profile for a friend?", "danger")
        return redirect(request.referrer)


@profiles.route('/connect_friends', methods=['GET', 'POST'])
@login_required
@email_confirmation_required
def connect_friends():
    """Processes a request to send a friend request"""

    find_friend_form = FindaFriendForm(request.form)
    if request.method == 'POST' and find_friend_form.validate():
        this_user = current_user
        existing_user = db.session.query(User
                                         ).join(Profile
                                                ).filter(Profile.email ==
                                                         find_friend_form.friend_email.data,
                                                         Profile.profile_id ==
                                                         User.profile_id).first()

        if find_friend_form.friend_email.data == this_user.profile.email:
            flash("You just tried to friend yourself. :) Would you like to add someone else?")
            return redirect(request.referrer)
        elif existing_user:
            friend_request = Friend.query.filter(Friend.user_id == this_user.id,
                                                 Friend.friend_profile_id ==
                                                 existing_user.profile_id).first()
            if Friend.already_friends(this_user, existing_user):
                flash("Looks like you are already connected to that person, would you like to add someone else?")
                return redirect(request.referrer)
            elif friend_request and friend_request.friend_request_sent:
                flash("Looks like you have already sent this person a friend request. Maybe check with them personally or create a friend profile for them yourself?")
                return redirect(request.referrer)
            else:
                friendship = Friend.create_record(user_id=this_user.id,
                                                  friend_profile_id=existing_user.profile_id)
                token = friendship.generate_email_token()
                send_email(to=existing_user.profile.email,
                           subject=' {0} {1}({2}) wants to connect\
                           on KindTable'.format(this_user.profile.first_name,
                                                this_user.profile.last_name,
                                                this_user.profile.email),
                           template='profiles/email/friend_existing_user',
                           profile=existing_user.profile,
                           friend=this_user.profile,
                           token=token)
                friendship.update({"friend_request_sent": True})
                flash('A connection request email has been sent to %s.' % existing_user.profile.email, "success")
                return redirect(url_for('profiles.show_dashboard'))
        else:
            new_friend_profile = Profile.create_record(email=find_friend_form.friend_email.data)
            friendship = Friend.create_record(user_id=current_user.id,
                                              friend_profile_id=new_friend_profile.profile_id)
            token = friendship.generate_email_token()
            send_email(to=new_friend_profile.email,
                       subject='{0} {1} wants to connect on KindTable'.format(this_user.profile.first_name,
                                                                              this_user.profile.last_name,
                                                                              this_user.profile.email),
                       template='profiles/email/friend_new_user',
                       friend=this_user.profile, token=token)
            flash('A connection request email has been sent to %s.'
                  % new_friend_profile.email, "success")
            return redirect(url_for('profiles.show_dashboard'))
    elif request.method == 'POST' and not find_friend_form.validate():
        flash_errors(find_friend_form)
        return redirect(request.referrer)
    else:
        return render_template("profiles/find_a_friend.html",
                               find_friend_form=find_friend_form)


@profiles.route('/add_friend_profile', methods=['GET', 'POST'])
@login_required
@email_confirmation_required
def add_friend_profile():
    """Loads the add_friend_profile modal contents and processes a request to
    make a private profile"""

    private_profile_title_form = PrivateProfileTitleForm(request.form)
    this_user = current_user
    if request.method == 'POST' and private_profile_title_form.validate():
        existing_profile = Profile.query.filter(Profile.private_profile_title == private_profile_title_form.title.data, Profile.owned_by_user_id == this_user.id).first()
        if existing_profile:
            flash("Looks like you already have a private profile for this person. Would you like to edit this one?")
            return redirect('profiles/friendprofile/%s' % existing_profile.profile_id)
        else:
            new_friend_profile = Profile.create_record(private_profile_title=private_profile_title_form.title.data,
                                                       owned_by_user_id=this_user.id)
            Friend.create_record(user_id=current_user.id,
                                 friend_profile_id=new_friend_profile.profile_id,
                                 private_profile=True)
            flash("Success! You can start editing information about your friend here.")
            return redirect('profiles/friendprofile/%s' % new_friend_profile.profile_id)
    else:
        return render_template("profiles/add_friend_profile.html",
                               private_profile_title_form=private_profile_title_form)


@profiles.route('/confirm_friendship_existing_user/<token>', methods=['GET'])
@login_required
@email_confirmation_required
def confirm_friendship_with_existing_user(token):
    """Validates an email token and confirms friendship between
    two existing users"""

    current_user_id = current_user.id

    friendship = Friend.process_email_token(token=token,
                                            current_user_id=current_user_id)
    if friendship == "logout":
        flash("Oops! Looks likes another user was still logged in on this computer. We have logged them out. Please follow the link from your email again.")
        return redirect(url_for('auth.logout'))
    elif friendship == "false":
        flash("There seems to be an error. Please email kindtableapp@gmail.com with what you were doing when the error happened. Thank you.")
    elif not friendship:
        abort(404)
    else:
        friend = User.query.get(friendship.user_id)

        Friend.create_record(user_id=current_user_id,
                             friend_profile_id=friend.profile.profile_id,
                             friendship_verified_by_email=True)
        flash("Congratulations! You are now friends with %s!" % str(friend.profile.first_name), "success")
        return redirect('profiles/friendprofile/%s' % friend.profile.profile_id)


@profiles.route('/confirm_friendship_new_user/<token>', methods=['GET'])
@login_required
@email_confirmation_required
def confirm_friendship_with_new_user(token):
    """Validates an email token and registers a new user"""

    user_id = current_user.id
    friendship = Friend.process_email_token(token, current_user_id=user_id)
    if friendship == "logout":
        flash("Oops! Looks likes another user was still logged in on this computer. We have logged them out. Please follow the link from your email again.")
        return redirect(url_for('auth.logout'))
    elif friendship == "false":
        flash("There seems to be an error. Please email kindtableapp@gmail.com with what you were doing when the error happened. Thank you.")
    elif not friendship:
        abort(404)
    else:
        new_friend = friendship.user.profile
        flash("Congratulations! You are now friends!", "success")
        return redirect('profiles/friendprofile/%s' % new_friend.profile_id)


@profiles.route('/party_profile/<int:party_id>')
@login_required
@email_confirmation_required
def show_party_profile(party_id):
    """Show the party profile"""

    is_your_party = Party.query.filter(Party.user_id ==
                                       current_user.id).first()
    if is_your_party:
        session['party_id'] = party_id
        party = Party.query.get(party_id)
        manage_guests_form = ManageGuestListForm(request.form)
        titleform = PartyTitleForm(request.form)
        datetimeform = PartyDatetimeForm(request.form)
        partynotesform = PartyNotesForm(request.form)
        partynotesform.notes.data = party.party_notes
        _datetime_ = party.datetime_of_party

        party_date = _datetime_.astimezone(timezone(session['timezone']))

        naive = party_date.replace(tzinfo=None)

        deletepartyform = DeletePartyForm(request.form)

        party_date_date = naive
        party_date_time = naive.time()

        datetimeform.date.data = party_date_date
        datetimeform.hour.data = party_date_time

        session['cuisine'] = 1
        session['course'] = 1

        get_avoid = guest_avoidances(party_id)
        get_intolerance = guest_intolerances(party_id)
        party_guests = PartyGuest.query.filter(PartyGuest.party_id == party_id).all()
        party_diets = list(set(guest.profiles.diet.diet_type for guest in party_guests))

        session['diets'] = party_diets
        session['intols'] = get_intolerance
        session['avoids'] = get_avoid
        session['offset'] = 0

        friends = current_user.valid_friends()
        manage_guests_form.friends.choices = [(friend.profile_id, ("{0} {1} ({2})").format(friend.first_name, friend.last_name, friend.email)) if friend.private_profile_title is None else (friend.profile_id, friend.private_profile_title) for friend in friends]
        titleform.title.data = party.title
        party_guests = party.guests
        manage_guests_form.friends.data = [guest.friend_profile_id for guest in party_guests]

        collated_recipes = []
        recipe_dict = {}
        if party.party_recipes:
            for recipe in party.party_recipes:
                works_for = json.loads(recipe.works_for)
                works = []
                for guest in party.guests:
                    add = True
                    if guest.profiles.avoidances:
                        for avoid in guest.profiles.avoidances:
                            if avoid.ingredient in works_for['avoids']:
                                pass
                            else:
                                add = False
                    if guest.profiles.diet.diet_type in works_for['diets']:
                        pass
                    else:
                        add = False
                    if guest.profiles.intolerances:
                        for intol in guest.profiles.intolerances:
                            if intol.intol_name in works_for['intols']:
                                pass
                            else:
                                add = False
                    if add is True:
                        if guest.profiles.private_profile_title:
                            name = guest.profiles.private_profile_title
                        elif guest.profiles.first_name and guest.profiles.last_name:
                            name = guest.profiles.first_name + " " + guest.profiles.last_name
                        elif guest.profiles.first_name:
                            name = guest.profiles.first_name + " (" + guest.profiles.email + ")"
                        else:
                            name = guest.profiles.email
                        works.append(name)
                    else:
                        continue
                recipe_dict = {'title': recipe.recipes.title,
                               'record_id': recipe.record_id,
                               'image_url': recipe.recipes.recipe_image_url,
                               'works_for': json.loads(recipe.works_for),
                               'notes': recipe.recipe_notes,
                               'works_for_guests': works,
                               'course': recipe.course.course_name,
                               'cuisine': recipe.cuisine.cuisine_name}
                collated_recipes.append(recipe_dict)
        else:
            collated_recipes = ""
        return render_template("profiles/party_profile.html", party=party,
                               manage_guests_form=manage_guests_form,
                               titleform=titleform,
                               datetimeform=datetimeform,
                               partynotesform=partynotesform,
                               collated_recipes=collated_recipes,
                               deletepartyform=deletepartyform)
    else:
        flash("At this time, you may only view your own parties. What a neat feature to add, though!")
        return redirect(request.referrer)


@profiles.route('/add_new_party', methods=['GET', 'POST'])
@login_required
@email_confirmation_required
def add_new_party():
    """Serves the template and processes the form to add a new party"""

    add_party_form = AddNewPartyForm(request.form)

    if request.method == 'POST' and add_party_form.validate():
        session_timezone = session['timezone']
        _datetime_ = datetime.combine(add_party_form.date.data, add_party_form.hour.data)
        tz = timezone(session_timezone)
        party_date = tz.localize(_datetime_)
        new_party = Party.create_record(title=add_party_form.party_name.data,
                                        datetime_of_party=party_date,
                                        user_id=current_user.id,
                                        party_notes=add_party_form.notes.data)
        PartyGuest.create_record(party_id=new_party.party_id,
                                 friend_profile_id=current_user.profile_id)
        flash("Success! Who would you like to invite to your party?", "success")
        return redirect("profiles/party_profile/%s" % new_party.party_id)
    elif request.method == 'POST' and not add_party_form.validate():
        flash_errors(add_party_form)
        return redirect(request.referrer)
    else:
        return render_template("profiles/add_a_party.html",
                               add_party_form=add_party_form)


@profiles.route('/delete_private_profile', methods=['GET', 'POST'])
@login_required
@email_confirmation_required
def deleteprivateprofile():
    """Deletes a private profile"""

    deleteppform = DeletePrivateProfileForm(request.form)

    if request.method == 'POST' and deleteppform.validate():
        friend = Profile.query.get(deleteppform.private_profile_id.data)
        friend.remove_profile()
        flash("Private profile removed.")
        return redirect(url_for('profiles.show_dashboard'))
    else:
        return redirect(request.referrer)


# Only JSON routes below for AJAX calls

@profiles.route('/changeprivateprofiletitle.json', methods=['POST'])
@login_required
@email_confirmation_required
def changeprivateprofiletitle():
    """Takes an Ajax request and changes a private profiles title"""

    form = ChangePrivateProfileTitleForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        profile = Profile.query.get(form.profile_id.data)
        profile.update({"private_profile_title": form.title.data,
                        "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Title updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/changefirstname.json', methods=['POST'])
@login_required
@email_confirmation_required
def changefirstname():
    """Takes an Ajax request and changes a profiles first name"""

    form = FirstNameForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        profile = Profile.query.get(form.profile_id.data)
        profile.update({"first_name": form.first_name.data,
                        "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'First name updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/changelastname.json', methods=['POST'])
@login_required
@email_confirmation_required
def changelastname():
    """Takes an Ajax request and changes a profiles last name"""

    form = LastNameForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        profile = Profile.query.get(form.profile_id.data)
        profile.update({"last_name": form.last_name.data,
                        "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Last name updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/changediet.json', methods=['POST'])
@login_required
@email_confirmation_required
def changediet():
    """Takes an Ajax request and changes diet"""

    form = DietForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        profile.update({"diet_id": form.diet.data,
                        "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Diet updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/changedietreason.json', methods=['POST'])
@login_required
@email_confirmation_required
def changedietreason():
    """Takes an Ajax request and changes diet reason"""

    form = DietReasonForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        profile.update({"diet_reason": form.diet_reason.data,
                        "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Diet reason updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/cleardietreason.json', methods=['POST'])
@login_required
@email_confirmation_required
def cleardietreason():
    """Takes an Ajax request and clear's the diet reason"""

    form = DietReasonForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        profile.update({"diet_reason": None, "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Diet reason updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/intol.json', methods=['POST'])
@login_required
@email_confirmation_required
def intol():
    """Takes an Ajax request and updates intolerances"""

    form = IntoleranceForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        query = db.session.query(ProfileIntolerance
                                 ).filter(ProfileIntolerance.profile_id ==
                                          profile.profile_id).all()
        profile_intolerances = [(intol.intol_id) for intol in query]
        for intolerance in form.intolerances.data:
            if intolerance in profile_intolerances:
                pass
            elif intolerance not in profile_intolerances:
                ProfileIntolerance.create_record(profile_id=profile.profile_id,
                                                 intol_id=intolerance)
                profile.update({"last_updated": datetime.utcnow()})
        for profile_intolerance in profile_intolerances:
            if profile_intolerance not in form.intolerances.data:
                intol = db.session.query(ProfileIntolerance
                                         ).filter(ProfileIntolerance.intol_id ==
                                                  profile_intolerance,
                                                  ProfileIntolerance.profile_id ==
                                                  profile.profile_id).one()
                intol.remove_intolerance()
                profile.update({"last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Intolerances updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/addavoid.json', methods=['POST'])
@login_required
@email_confirmation_required
def addavoid():
    """Takes an Ajax request and adds an ingredient to avoid"""
    form = AddAvoidForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        already_added = db.session.query(IngToAvoid
                                         ).filter(IngToAvoid.profile_id == profile.profile_id, IngToAvoid.ingredient ==
                                                  form.add_avoid_ingredient.data).all()
        if already_added:
            flash("We already know about that ingredient to avoid.\
                  Would you like to add a different one?", "warning")
            return redirect(request.referrer)
        else:
            IngToAvoid.create_record(ingredient=form.add_avoid_ingredient.data,
                                     reason=form.add_avoid_reason.data,
                                     profile_id=profile.profile_id)
            profile.update({"last_updated": datetime.utcnow()})
            return jsonify(data={'message': 'Avoid added'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/getavoid.json', methods=['GET'])
@login_required
@email_confirmation_required
def getavoid():
    """Takes an Ajax request and returns avoidance information"""

    avoid_id = request.args.get("id")
    avoidance = IngToAvoid.query.get(avoid_id)
    return jsonify(data={'ingredient': avoidance.ingredient,
                         'reason': avoidance.reason})


@profiles.route('/updateavoid.json', methods=['POST'])
@login_required
@email_confirmation_required
def updateavoid():
    """Takes an Ajax request and updates an existing ingredient to avoid"""

    form = UpdateAvoidForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        avoid = IngToAvoid.query.get(form.avoid_id.data)
        if form.update_avoid_ingredient:
            avoid.update({'ingredient': form.update_avoid_ingredient.data})
        if form.update_avoid_reason:
            avoid.update({'reason': form.update_avoid_reason.data})
        profile.update({"last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Ingredients to avoid updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/deleteavoidreason.json', methods=['POST'])
@login_required
@email_confirmation_required
def deleteavoidreason():
    """Takes an Ajax request and removes an existing ingredient to avoid"""

    form = UpdateAvoidForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        avoid = IngToAvoid.query.get(form.avoid_id.data)
        avoid.update({'reason': None})
        profile.update({"last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Ingredients to avoid updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/deleteavoid.json', methods=['POST'])
@login_required
@email_confirmation_required
def deleteavoid():
    """Takes an Ajax request and removes an existing ingredient to avoid"""

    form = UpdateAvoidForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        avoid = IngToAvoid.query.get(form.avoid_id.data)
        avoid.remove_avoidance()
        profile.update({"last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Ingredients to avoid updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/delete_friend.json', methods=['POST'])
@login_required
@email_confirmation_required
def delete_friend():
    """Takes an Ajax request and deletes a friend"""

    form = DeleteFriendForm(request.form)
    friend_profile = Profile.query.get(form.friend_profile_id.data)
    friendship1 = db.session.query(Friend).filter(Friend.user_id ==
                                                  current_user.id,
                                                  Friend.friend_profile_id ==
                                                  form.friend_profile_id.data).first()
    if request.method == 'POST' and form.validate():
        if friend_profile.owned_by_user_id == current_user.id:
            friend_profile.remove_profile()
        else:
            friendship2 = db.session.query(Friend).filter(Friend.user_id ==
                                                          friend_profile.owned_by_user_id,
                                                          Friend.friend_profile_id ==
                                                          current_user.profile_id).first()
            friendship2.remove_friendship()

        friendship1.remove_friendship()
        flash("Friend removed from your account.")
        return redirect(url_for('profiles.show_dashboard'))
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/changefriendemail.json', methods=['POST'])
@login_required
@email_confirmation_required
def changefriendemail():
    """Takes an Ajax request and changes a friend's email address"""

    form = ChangeFriendEmailForm(request.form)
    profile = Profile.query.get(form.friend_profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        profile = Profile.query.get(form.friend_profile_id.data)
        profile.update({"email": form.email.data,
                        "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'First name updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/changefriendnotes.json', methods=['POST'])
@login_required
@email_confirmation_required
def changefriendnotes():
    """Takes an Ajax request and changes the note on the Friend table"""

    form = FriendNotesForm(request.form)
    profile = Profile.query.get(form.friend_profile_id.data)
    friendship = Friend.query.filter(Friend.friend_profile_id ==
                                     profile.profile_id, Friend.user_id ==
                                     current_user.id).one()
    if form.validate():
        friendship.update({"friend_notes": form.notes.data,
                           "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Notes updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/clearfriendnote.json', methods=['POST'])
@login_required
@email_confirmation_required
def clearfriendnotes():
    """Takes an Ajax request and clears the note on the Friend table"""

    form = FriendNotesForm(request.form)
    profile = Profile.query.get(form.friend_profile_id.data)
    friendship = Friend.query.filter(Friend.friend_profile_id ==
                                     profile.profile_id, Friend.user_id ==
                                     current_user.id).one()
    if form.validate():
        friendship.update({"friend_notes": None,
                           "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Notes updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/findafriend.json', methods=['POST'])
@login_required
@email_confirmation_required
def findafriend():
    """Takes an Ajax request and sends friend requests"""

    form = FindaFriendForm(request.form)
    friendship = db.session.query(Friend).join(Profile
                                               ).filter(Profile.email ==
                                                        form.email.data,
                                                        Friend.user_id ==
                                                        current_user.id).first()
    if form.validate():
        friendship.update({"friend_notes": None,
                           "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Notes updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/manageguestlist.json', methods=['POST'])
@login_required
@email_confirmation_required
def manageguestlist():
    """Takes an Ajax request and updates PartyGuest table"""

    form = ManageGuestListForm(request.form)
    friends = current_user.friends
    form.friends.choices = [(friend.friend_profile_id,
                            ("{0} {1} ({2})").format(friend.friend_profile.first_name,
                                                     friend.friend_profile.last_name,
                                                     friend.friend_profile.email)) for friend in friends]
    party = Party.query.get(int(form.party_id.data))

    if request.method == 'POST' and form.validate():
        query = db.session.query(PartyGuest
                                 ).filter(PartyGuest.party_id ==
                                          party.party_id).all()
        party_guests = [(guest.friend_profile_id) for guest in query]

        for guest in form.friends.data:
            if guest in party_guests:
                pass
            elif guest not in party_guests:
                PartyGuest.create_record(party_id=party.party_id,
                                         friend_profile_id=guest)
                party.update({"last_updated": datetime.utcnow()})
        for guest in party_guests:
            if guest not in form.friends.data:
                if guest == current_user.profile_id:
                    pass
                else:
                    guest = db.session.query(PartyGuest
                                             ).filter(PartyGuest.party_id ==
                                                      party.party_id,
                                                      PartyGuest.friend_profile_id ==
                                                      guest).one()
                    guest.disinvite_guest()
                    party.update({"last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Guests updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/changetitle.json', methods=['POST'])
@login_required
@email_confirmation_required
def changetitle():
    """Takes an Ajax request and changes a party's title"""

    form = PartyTitleForm(request.form)
    party = Party.query.get(form.party_id.data)
    if request.method == 'POST' and form.validate():
        party.update({"title": form.title.data,
                      "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Party title updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/partydatetime', methods=['POST'])
@login_required
@email_confirmation_required
def party_datetime():
    """Takes an Ajax request and changes a party's title"""

    form = PartyDatetimeForm(request.form)

    if request.method == 'POST' and form.validate():
        session_timezone = session['timezone']
        _datetime_ = datetime.combine(form.date.data, form.hour.data)
        tz = timezone(session_timezone)
        party_date = tz.localize(_datetime_)
        party = Party.query.get(form.party_id.data)
        party.update({"datetime_of_party": party_date, "last_updated": datetime.utcnow()})
        _display_datetime = (party.datetime_of_party).astimezone(tz)
        monkey_datetime = _display_datetime.strftime('%A, %B %d, %Y %I:%M %p')
        if monkey_datetime[-8] == '0':
            monkey_datetime = monkey_datetime[:-8] + monkey_datetime[-7:]
        return monkey_datetime
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/changepartynotes.json', methods=['POST'])
@login_required
@email_confirmation_required
def changepartynotes():
    """Takes an Ajax request and changes a note on the Party table"""

    form = PartyNotesForm(request.form)
    party = Party.query.get(form.party_id.data)
    if request.method == 'POST' and form.validate():
        party.update({"party_notes": form.notes.data,
                      "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Notes updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/clearpartynote.json', methods=['POST'])
@login_required
@email_confirmation_required
def clearpartynotes():
    """Takes an Ajax request and clears a note on the Party table"""

    form = PartyNotesForm(request.form)
    party = Party.query.get(form.party_id.data)
    if request.method == 'POST' and form.validate():
        party.update({"party_notes": None,
                      "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Notes updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/discardparty', methods=['POST'])
@login_required
@email_confirmation_required
def discardparty():
    """Takes an Ajax request and deletes a party and all of it's associated records"""

    form = DeletePartyForm(request.form)
    party = Party.query.get(form.party_id.data)
    if request.method == 'POST' and form.validate():
        party.discard_party()
        return redirect(url_for('profiles.show_dashboard'))
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/invitetoparties.json', methods=['POST'])
@login_required
@email_confirmation_required
def invitetoparties():
    """Takes an Ajax request and updates the PartyGuest table"""

    inviteform = InviteForm(request.form)

    upcoming_parties_invited_to = db.session.query(PartyGuest).join(Party).filter(Party.user_id == current_user.id, Party.datetime_of_party >=
                                                                                  datetime.utcnow(),
                                                                                  PartyGuest.friend_profile_id == inviteform.profileid.data).order_by(Party.datetime_of_party).all()

    upcoming_parties = db.session.query(Party).filter(Party.user_id == current_user.id,
                                                      Party.datetime_of_party >= datetime.utcnow()).all()
    inviteform.parties.choices = [(party.party_id, party.title) for party in upcoming_parties]

    form_data = inviteform.parties.data

    profile_id = inviteform.profileid.data

    if request.method == 'POST' and inviteform.validate():
        if form_data is not None:
            for choice in form_data:
                PartyGuest.create_record(party_id=choice,
                                         friend_profile_id=profile_id)
        for party in upcoming_parties_invited_to:
            if party.party.party_id not in form_data:
                party._delete_()
        return jsonify(data={'message': 'PartyGuest updated'})
    else:
        for field, error in inviteform.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(inviteform, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)
