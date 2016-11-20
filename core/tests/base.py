# coding=utf-8

from fixture import DataTestCase
from flask_testing import TestCase as TestCaseOrig

from core.database import db
from core.main import create_app
from core.fixtures import dbfixture


class TestCase(DataTestCase, TestCaseOrig):

    fixture = dbfixture

    def setUp(self):
        super(TestCase, self).setUp()

    def tearDown(self):
        super(TestCase, self).tearDown()
        db.session.remove()
        db.get_engine(self.app).dispose()

    def create_app(self):
        return create_app('config.Testing')
