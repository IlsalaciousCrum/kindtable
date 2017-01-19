from flask import render_template, redirect, request, url_for, flash

from . import userdata

from ..models import Profile

from .forms import ProfileData


@userdata.route('/register', methods=['GET', 'POST'])
def register():
    form = ProfileData()
    if form.validate_on_submit():
        user_profile = Profile.query.filter(Profile.email == form.email.data,
                                            Profile.is_user_profile is True).first()
        return url_for('auth/login.html')
        flash('That email address is already registered. Would you like to login or reset your password?')

        user = user_profile.user
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
            flash('Invalid username or password.')
    else:
        return render_template('auth/login.html', form=form)


# @auth.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('You have been logged out.')
#     return redirect(url_for('main.index'))
