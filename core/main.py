# coding=utf-8

import os
import logging
from logging.handlers import SMTPHandler

from flask import Flask

from core.database import db
from core.restless import apimanager
from core.restless.registered_models import api_registered_models


def create_app(config, app_name=None, blueprints=None):
    app_name = app_name or __name__

    app = Flask(app_name, static_folder=None)

    configure_app(app, config)
    configure_logger(app)
    configure_sqlalchemy(app)
    configure_api(app)

    return app


def configure_app(app, config):
    config = os.environ.get('WIKI_CONFIG', config)
    app.config.from_object(config)


def configure_sqlalchemy(app):
    db.init_app(app)


def configure_api(app):
    for api_model in api_registered_models:
        apimanager.create_api(**api_model)
    apimanager.init_app(app, flask_sqlalchemy_db=db)


def create_logs_root(app):
    try:
        os.mkdir(app.config['LOG_ROOT'], 0775)
    except OSError:
        pass


def configure_logger(app):
    if not app.debug:
        mail_handler = SMTPHandler('127.0.0.1',
                                   'server-error@example.com',
                                   app.config['MAIL_ERROR_BOXES'],
                                   'Application Failed')
        mail_handler.setLevel(logging.WARNING)
        mail_handler.setFormatter(logging.Formatter('''
        Message type:       %(levelname)s
        Location:           %(pathname)s:%(lineno)d
        Module:             %(module)s
        Function:           %(funcName)s
        Time:               %(asctime)s

        Message:

        %(message)s
        '''))
        app.logger.addHandler(mail_handler)

        create_logs_root(app)
        file_handler = logging.FileHandler(app.config['LOG_FILE'])
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        app.logger.addHandler(file_handler)
