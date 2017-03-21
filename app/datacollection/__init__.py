from flask import Blueprint

datacollection = Blueprint('datacollection', __name__)

from . import views
