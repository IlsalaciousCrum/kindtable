"""K(i)nd app views for the 'main' blueprint"""

from flask import render_template, request, redirect, flash, url_for
from . import main
from flask_login import current_user, login_required
from ..decorators import email_confirmation_required
from .forms import (BetaAccessForm)
from ..email import send_email


@main.route('/')
def index():
    """Homepage."""

    if current_user.is_authenticated:
        profile = current_user.profile
        return render_template("main/kind_homepage.html", profile=profile)
    else:
        return render_template("main/kind_homepage.html")


@main.route('/request_beta_access', methods=['POST', 'GET'])
@login_required
@email_confirmation_required
def request_beta_access():
    """Load the beta access request view and process a request"""

    this_user = current_user
    this_profile = this_user.profile
    beta_request_form = BetaAccessForm(request.form)
    if request.method == 'POST' and beta_request_form.validate():
        if this_user.beta_approved:
            return redirect(url_for('profiles.show_dashboard'))
        else:
            send_email(to='kindtableapp@gmail.com',
                       subject=' Beta Access Request',
                       template='main/email/request_beta_access_email',
                       profile_id=this_profile.profile_id,
                       user_id=this_user.id,
                       full_name=beta_request_form.full_name.data,
                       email=beta_request_form.email.data,
                       reason=beta_request_form.reason.data)
            flash("Thank you! You will receive an email when your beta access is granted.")
            return redirect(url_for("profiles.show_dashboard"))
    else:
        beta_request_form.full_name.data = this_profile.first_name + " " + this_profile.last_name
        beta_request_form.email.data = this_profile.email
        return render_template("main/beta_access_request.html",
                               beta_request_form=beta_request_form)
