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
from flask_assets import Environment, Bundle

jsglue = JSGlue()
db = SQLAlchemy()
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()

login_manager = LoginManager()
login_manager.login_view = "auth.login"

login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    assets = Environment(app)

    js = Bundle("js/addAvoid-Register.js", "js/addAvoid.js", "js/addFriendProfile.js",
                "js/addParty.js", "js/base.js", "js/datetime.js", "js/diet.js",
                "js/dietReason.js", "js/discardParty.js", "js/emailMenu.js",
                "js/findFriend.js", "js/firstName.js", "js/friendEmail.js",
                "js/friendNotes.js", "js/Intol-register.js", "js/Intol.js",
                "js/inviteFriendToParties.js", "js/lastName.js",
                "js/login_timezone.js", "js/manageGuestList.js", "js/partyNotes.js",
                "js/partyTitle.js", "js/recipeNotes.js",
                "js/recipeSearch.js", "js/updateAvoid-register.js", "js/updateAvoid.js",
                filters='jsmin', output='gen/packed.js')

    assets.init_app(app)
    assets.register('js_all', js)

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
