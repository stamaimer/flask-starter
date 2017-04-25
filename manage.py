# coding: utf-8

"""

    manage
    ~~~~~~

    stamaimer 04/25/17

"""


import pymysql

import click

from flask import current_app

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app.model import db

from app import create_app


app = create_app("config.DefaultConfig")

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command("db", MigrateCommand)


@manager.command
def create_db():

    try:

        if click.confirm("This command will destroy current database and all data in it. "
                         "Do you want to continue?",
                         default=False):

            connection = pymysql.connect(host=current_app.config["DB_HOST"],
                                         port=current_app.config["DB_PORT"],
                                         user=current_app.config["DB_USER"], passwd=current_app.config["DB_PSWD"])

            cursor = connection.cursor()

            cursor.execute("DROP DATABASE IF EXISTS {}".format(current_app.config["DB_NAME"]))

            cursor.execute("CREATE DATABASE IF NOT EXISTS {} CHARACTER SET utf8 COLLATE utf8_general_ci"
                           .format(current_app.config["DB_NAME"]))

    except:

        pass


if __name__ == "__main__":

    manager.run()
