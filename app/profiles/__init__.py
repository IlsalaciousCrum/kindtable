from flask import Blueprint

profiles = Blueprint('profiles', __name__)

from . import views
