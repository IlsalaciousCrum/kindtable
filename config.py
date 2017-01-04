import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = True,
    MAIL_DEFAULT_SENDER = os.environ['KIND_TABLE_DEFAULT_SENDER'],
    MAIL_USERNAME = os.environ['KIND_TABLE_EMAIL'],
    MAIL_PASSWORD = os.environ['KIND_TABLE_EMAIL_PASSWORD'],
    SECRET_KEY = os.environ['APP_SECRET_KEY']
    KIND_MAIL_SUBJECT_PREFIX = '[Flasky]'
    KIND_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres:///kind'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'postgres:///kindtest'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgres:///kind'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
