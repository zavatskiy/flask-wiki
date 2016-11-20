# coding=utf-8

import os
import sys

APPS_ROOT = os.path.join(os.path.normpath(os.path.dirname(__file__)), 'apps')
sys.path.insert(0, APPS_ROOT)


from flask_script import Manager

from core import commands
from core.main import create_app


app = create_app('config.Dev')

manager = Manager(app)
manager.add_command("test", commands.Test(app))
manager.add_command("create_db", commands.CreateDB())
manager.add_command("drop_db", commands.DropDB())


if __name__ == '__main__':
    manager.run()
