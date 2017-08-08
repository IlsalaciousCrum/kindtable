"""K(i)nd app views for the 'main' blueprint"""

from flask import render_template
from . import main
from flask_login import current_user


@main.route('/')
def index():
    """Homepage."""

    if current_user.is_authenticated:
        profile = current_user.profile
        return render_template("main/kind_homepage.html", profile=profile)
    else:
        return render_template("main/kind_homepage.html")
