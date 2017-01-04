#!/usr/bin/kind_env python

import os
from app import create_app, db
from app.models import User, Profile, Friend, UserIntolerance, Intolerance, Diet, Cuisine, Course, IngToAvoid, PartyGuest, Party, RecipeCard, RecipeBox, PartyRecipes
from Flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from jinja2 import StrictUndefined
from app.seed import LoadSeedData

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# StrictUndefined raises an error.

app.jinja_env.undefined = StrictUndefined


def make_shell_context():
    return dict(app=app, db=db, User=User, Profile=Profile, Friend=Friend,
                UserIntolerance=UserIntolerance, Intolerance=Intolerance,
                Diet=Diet, Cuisine=Cuisine, Course=Course, IngToAvoid=IngToAvoid,
                PartyGuest=PartyGuest, Party=Party, RecipeCard=RecipeCard,
                RecipeBox=RecipeBox, PartyRecipes=PartyRecipes)
    manager.add_command("shell", Shell(make_context=make_shell_context))
    manager.add_command('db', MigrateCommand)

server = Server(host="0.0.0.0", port=5000, use_debugger=True, use_reloader=True)
manager.add_command("runserver", server)
manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    LoadSeedData()


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade
    from app.seed import LoadSeedData

    # migrate database to latest revision
    upgrade()

    LoadSeedData()


if __name__ == '__main__':
    manager.run()
