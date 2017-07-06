from flask import Blueprint

spoonacular = Blueprint('spoonacular', __name__)

from . import views, forms
