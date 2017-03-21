'''Configuration settings for the app'''

import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = os.environ['KIND_TABLE_DEFAULT_SENDER']
    MAIL_USERNAME = os.environ['KIND_TABLE_EMAIL']
    MAIL_PASSWORD = os.environ['KIND_TABLE_EMAIL_PASSWORD']
    SECRET_KEY = os.environ['APP_SECRET_KEY']
    KIND_MAIL_SUBJECT_PREFIX = '[Kind Table]'
    KIND_MAIL_SENDER = 'Kind Table Admin <mail@kindtable.net>'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    KIND_ADMIN = os.environ.get('KIND_ADMIN')

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
    SQLALCHEMY_DATABASE_URI = 'postgres://ctufwrrmmozyit:2f60a317a9f8bbe24db52ea5efd32651ae6b8a55500e709f70386d87c30b25a0@ec2-54-225-119-223.compute-1.amazonaws.com:5432/d7scv1f00qis1d'
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
