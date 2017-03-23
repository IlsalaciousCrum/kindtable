from flask import Blueprint

profiles = Blueprint('datacollection', __name__)

from . import views
