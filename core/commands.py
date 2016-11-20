# coding=utf-8

import os
import unittest
import config

from flask_script import Command, Option

from core.database import create_all
from core.database import drop_all


class CreateDB(Command):
    """Creates sqlalchemy database"""
    def run(self):
        create_all()


class DropDB(Command):
    """Drops sqlalchemy database"""
    def run(self):
        drop_all()


class Test(Command):
    """Run tests"""
    start_discovery_dir = "tests"

    def __init__(self, app):
        self.app = app

    def get_options(self):
        return [
            Option(
                '--start_discover', '-s', dest='start_discovery',
                help='Pattern to search for features',
                default=self.start_discovery_dir
            ),
        ]

    def run(self, start_discovery):

        self.app.config.update(config.Testing.__dict__.items())

        if os.path.exists(start_discovery):
            argv = ["flask-wiki", "discover"]
            argv += ["-s", start_discovery]
            unittest.main(argv=argv)
        else:
            print(
                "Directory '{0}' was not found in project root."
                .format(start_discovery)
            )
