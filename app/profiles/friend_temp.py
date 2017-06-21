from flask import (render_template, redirect, url_for, flash, session,
                   request, jsonify, abort)

from . import profiles

from .. import db

from ..models import (User, Profile, Diet, Intolerance, Party, PartyGuest,
                      IngToAvoid, ProfileIntolerance, Friend)

from flask_login import login_required, current_user

from .forms import (FirstNameForm, LastNameForm, DietForm, DietReasonForm,
                    AddAvoidForm, UpdateAvoidForm, IntoleranceForm,
                    AddNewPartyForm, DeleteFriendForm, ChangeFriendEmailForm,
                    FriendNotesForm, FindaFriendForm, AddGuestToPartyForm)


from ..decorators import email_confirmation_required

from ..email import send_email


@profiles.route('/connect_friends', methods=['GET', 'POST'])
@login_required
@email_confirmation_required
def connect_friends():
    """Loads modal content for connecting a new friend and processes the request"""

    find_friend_form = FindaFriendForm(request.form)
    if request.method == 'POST' and find_friend_form.validate():
        existing_user = db.session.query(Profile
                                         ).join(User
                                                ).filter(Profile.email ==
                                                         find_friend_form.friend_email.data,
                                                         Profile.profile_id ==
                                                         User.profile_id).first()
        if existing_user:
            already_connected_friends = Friend.query.filter(Friend.user_id ==
                                                            current_user.id,
                                                            Friend.friend_profile_id ==
                                                            existing_user.profile_id).first()
            if already_connected_friends:
                flash("Looks like you are already connected to %s, you can find\
                      their profile information from the navigation bar above or\
                      on your dashboard." % find_friend_form.friend_email.data,
                      "warning")
                return redirect(request.referrer)
            if existing_user:
                friendship = Friend.create_record(user_id=current_user.id,
                                                  friend_profile_id=existing_user.profile_id)
                token = friendship.generate_email_token()
                send_email(to=existing_user.email,
                           subject=' {0} {1}({2}) wants to connect\
                           on KindTable'.format(current_user.profile.first_name,
                                                current_user.profile.last_name,
                                                current_user.profile.email),
                           template='profiles/email/friend_existing_user',
                           profile=existing_user,
                           friend=current_user.profile,
                           token=token)
                friendship.update({"friend_request_sent": True})
                flash('An connection request email has been sent to %s.'
                      % existing_user.email, "success")
                return redirect(request.referrer)
            if already_connected_friends.friend_request_sent is True:
                flash("Looks like you have already sent this person a friend\
                      request. Maybe check with them personally or create a friend\
                      profile for them yourself?", "danger")
                return redirect(request.referrer)
        else:
            new_friend_profile = Profile.create_record(email=find_friend_form.friend_email.data)
            friendship = Friend.create_record(user_id=current_user.id,
                                              friend_profile_id=new_friend_profile.profile_id)
            token = friendship.generate_email_token()
            send_email(to=new_friend_profile.email,
                       subject=' %s %s wants to connect on KindTable',
                       template='profiles/email/friend_new_user',
                       friend=current_user.profile, token=token)
            flash('An connection request email has been sent to %s.'
                  % new_friend_profile.email, "success")
            return redirect(request.referrer)
    return render_template("profiles/find_a_friend.html",
                           find_friend_form=find_friend_form)


@profiles.route('/non_reg_confirm_friendship/<token>', methods=['GET'])
@login_required
@email_confirmation_required
def confirm_friendship_with_existing_user(token):
    """Validates an email token and confirms friendship between
    two existing users"""

    friend_dict = Friend.process_email_token(token)
    print friend_dict
    if not friend_dict:
        abort(404)
    else:
        new_friend = User.query.get(friend_dict['user_id'])
        Friend.create_record(user_id=current_user.id,
                             friend_profile_id=new_friend.profile_id,
                             friendship_verified_by_email=True)
        flash("Congratulations! You are now friends!", "success")
        return redirect('profiles/friendprofile/%s' % new_friend.profile_id)


@profiles.route('/reg_confirm_friendship/<token>', methods=['GET'])
@login_required
@email_confirmation_required
def confirm_friendship_with_new_user(token):
    """Validates an email token and confirms friendship between
    two existing users"""

    friendship = Friend.process_email_token(token)
    if not friendship:
        abort(404)
    else:
        new_friend = friendship.user.profile
        flash("Congratulations! You are now friends!", "success")
        return redirect('profiles/friendprofile/%s' % new_friend.profile_id)
