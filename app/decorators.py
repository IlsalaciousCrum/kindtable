from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def email_confirmation_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.profile.email_verified:
            flash("Please check your email and confirm your email address.")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
