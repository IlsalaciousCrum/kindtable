from functools import wraps
from flask import redirect, url_for, flash, request
from flask_login import current_user


def email_confirmation_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.profile.email_verified:
            flash("Please check your email and confirm your email address to view this page.", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def beta_approval_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.beta_approved:
            return redirect(url_for('main.request_beta_access'))
        return f(*args, **kwargs)
    return decorated_function


def load_base(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.profile:
            return redirect(url_for('auth/login', next=request.url))
            return f(*args, **kwargs)
        return decorated_function

# Though this is not a decoratator, it is similar in nature


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" %
                  (getattr(form, field).label.text, error), 'danger')
