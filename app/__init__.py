from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from config import config
from jinja2 import StrictUndefined
from flask_wtf.csrf import CSRFProtect
from flask_jsglue import JSGlue

jsglue = JSGlue()
db = SQLAlchemy()
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()

login_manager = LoginManager()
login_manager.login_view = "auth.login"

login_manager.session_protection = 'basic'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # bootstrap.init_app(app)
    Bootstrap(app)
    CSRFProtect(app)
    mail.init_app(app)
    moment.init_app(app)
    jsglue.init_app(app)
    db.app = app
    db.init_app(app)
    login_manager.init_app(app)
    app.jinja_env.undefined = StrictUndefined

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .profiles import profiles as profiles_blueprint
    app.register_blueprint(profiles_blueprint, url_prefix='/profiles')

    from .spoonacular import spoonacular as spoonacular_blueprint
    app.register_blueprint(spoonacular_blueprint, url_prefix='/spoonacular')

    db.app = app

    #  attach routes and custom error pages here

    return app
