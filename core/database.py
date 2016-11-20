# coding=utf-8

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def drop_all():
    db.drop_all()


def create_all():
    db.create_all()
