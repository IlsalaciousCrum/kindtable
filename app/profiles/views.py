from flask import render_template, redirect, url_for, flash, session, request

from . import profiles

from .. import db

from ..models import User, Profile, Diet, Intolerance, ProfileIntolerance, IngToAvoid

from flask_login import login_required


@profiles.route('/update_profile/<profile_id>', methods=['GET', 'POST'])
@login_required
def update_profile(profile_id):
    """Make changes to a profile"""

    # update_profile_form = ProfileUpdateForm(request.form)
    profile = Profile.query.get(profile_id)
    session_token = session.get("session_token")
    user = User.query.filter(session_token == session_token).first()
    friends = user.friends
    parties = user.parties

    # if request.method == 'POST' and update_profile_form.validate():
    #     pass
    # else:
    #     return render_template('datacollection/profile_update.html',
    #                            form=update_profile_form,
    #                            profile=profile,
    #                            friends=friends,
    #                            parties=parties)
