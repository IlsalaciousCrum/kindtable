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
    KIND_MAIL_SUBJECT_PREFIX = '[Kind Table App]'
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

    init_app(app)
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    secure = None
    if getattr(cls, 'MAIL_USERNAME', None) is not None:
        credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
        if getattr(cls, 'MAIL_USE_TLS', None):
            secure = ()
    mail_handler = SMTPHandler(
        mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
        fromaddr=cls.KIND_MAIL_SENDER,
        toaddrs=[cls.FLASKY_ADMIN],
        subject=cls.KIND_MAIL_SUBJECT_PREFIX + 'Application Error',
        credentials=credentials,
        secure=secure)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHANDLER(mail_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
