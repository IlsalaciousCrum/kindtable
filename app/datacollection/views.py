from flask import render_template, redirect, request, url_for, flash

from . import datacollection

from .. import db

from ..models import Profile

from flask_login import login_required