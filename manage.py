# coding: utf-8

"""

    manage
    ~~~~~~

    stamaimer 04/25/17

"""


import pymysql

from flask import current_app

from flask_script import Manager
from flask_migrate import MigrateCommand

from app.model import db

from app import create_app, model


manager = Manager(create_app)

manager.add_option("-c", "--config", dest="config_name", required=True)

manager.add_command("db", MigrateCommand)


@manager.shell
def make_shell_context():

    return dict(app=manager.app, db=db, model=model)


@manager.command
def delete_db():

    try:

            connection = pymysql.connect(host=current_app.config["DB_HOST"],
                                         port=current_app.config["DB_PORT"],
                                         user=current_app.config["DB_USER"], passwd=current_app.config["DB_PSWD"])

            cursor = connection.cursor()

            cursor.execute("DROP DATABASE IF EXISTS {}".format(current_app.config["DB_NAME"]))

    except:

        pass

    # finally:
    #
    #     cursor.close()
    #
    #     connection.close()


@manager.command
def create_db():

    try:

            connection = pymysql.connect(host=current_app.config["DB_HOST"],
                                         port=current_app.config["DB_PORT"],
                                         user=current_app.config["DB_USER"], passwd=current_app.config["DB_PSWD"])

            cursor = connection.cursor()

            cursor.execute("CREATE DATABASE IF NOT EXISTS {} CHARACTER SET utf8 COLLATE utf8_general_ci"
                           .format(current_app.config["DB_NAME"]))

    except:

        pass

    # finally:
    #
    #     cursor.close()
    #
    #     connection.close()


@manager.command
def resets_db():

    delete_db()

    create_db()


if __name__ == "__main__":

    manager.run()
