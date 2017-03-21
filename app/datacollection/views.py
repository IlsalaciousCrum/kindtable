from flask import render_template, redirect, request, url_for, flash

from . import userdata

from .. import db

from ..models import Profile

from .forms import ProfileData

from flask_login import logout_user, login_required


@userdata.route('/register', methods=['GET', 'POST'])
def register():
    form = ProfileData()
    if form.validate_on_submit():
        user_profile = Profile.query.filter(Profile.email == form.email.data,
                                            Profile.is_user_profile is True).first()
        return url_for('auth/login.html')
        flash('That email address is already registered. Would you like to login or reset your password?')

    else:
        return render_template('auth/login.html', form=form)


@userdata.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
