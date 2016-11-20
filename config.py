# coding=utf-8

import os


class Config(object):
    DEBUG = True
    TESTING = False

    PROJECT_NAME = 'flask_wiki'
    PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:rhbcnb@localhost/{0}".format(PROJECT_NAME)
    )
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SECRET_KEY = "secret"
    API_KEY = "secret"

    LOGGER_NAME = PROJECT_NAME
    LOG_ROOT = os.path.join(PROJECT_ROOT, 'logs')
    LOG_FILE = os.path.join(LOG_ROOT, '{0}.log'.format(PROJECT_NAME))

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEBUG = DEBUG
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    NOREPLY_MAIL_SENDER = "noreply@example.com"
    MAIL_ERROR_BOXES = [NOREPLY_MAIL_SENDER]


class Dev(Config):
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:postgres@localhost/{0}"
        .format(Config.PROJECT_NAME)
    )


class Testing(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:postgres@localhost/{0}_test"
        .format(Config.PROJECT_NAME)
    )


class Production(Config):
    DEBUG = False
    SECRET_KEY = '4aR7*px~z[tgkja;)Y+LxElG'
    API_KEY = '4aR7*px~z[tgkja;)Y+LxElG'
