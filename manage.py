# coding: utf-8

"""

    manage
    ~~~~~~

    stamaimer 04/25/17

"""


import pymysql

from flask import current_app

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app.model import db, Role, User

from app import create_app, model


app = create_app("config.DefaultConfig")

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command("db", MigrateCommand)


@manager.shell
def make_shell_context():

    return dict(app=manager.app, db=db, model=model)


@manager.option("-u", "--user", dest="user", default="root")
@manager.option("-p", "--pswd", dest="pswd", default='')
def create_user(user, pswd):

    with pymysql.connect(host=current_app.config["DB_HOST"],
                         port=current_app.config["DB_PORT"],
                         user=user, passwd=pswd) as cursor:

        cursor.execute("GRANT ALL PRIVILEGES ON {}.* TO '{}'@'%' IDENTIFIED BY '{}'"
            .format(current_app.config["DB_NAME"], current_app.config["DB_USER"], current_app.config["DB_PSWD"]))


@manager.option("-u", "--user", dest="user", default="root")
@manager.option("-p", "--pswd", dest="pswd", default='')
def delete_user(user, pswd):

    with pymysql.connect(host=current_app.config["DB_HOST"],
                         port=current_app.config["DB_PORT"],
                         user=user, passwd=pswd) as cursor:

        cursor.execute("REVOKE ALL PRIVILEGES ON {}.* FROM '{}'@'%'"
                       .format(current_app.config["DB_NAME"], current_app.config["DB_USER"]))

        cursor.execute("DROP USER '{}'@'%'".format(current_app.config["DB_USER"]))


@manager.command
def delete_db():

    with pymysql.connect(host=current_app.config["DB_HOST"],
                         port=current_app.config["DB_PORT"],
                         user=current_app.config["DB_USER"], passwd=current_app.config["DB_PSWD"]) as cursor:

        cursor.execute("DROP DATABASE IF EXISTS {}".format(current_app.config["DB_NAME"]))


@manager.command
def create_db():

    with pymysql.connect(host=current_app.config["DB_HOST"],
                         port=current_app.config["DB_PORT"],
                         user=current_app.config["DB_USER"], passwd=current_app.config["DB_PSWD"]) as cursor:

        cursor.execute("CREATE DATABASE IF NOT EXISTS {} CHARACTER SET utf8 COLLATE utf8_general_ci"
                       .format(current_app.config["DB_NAME"]))


@manager.command
def resets_db():

    delete_db()

    create_db()


@manager.command
def fillup_data():

    admin_role = Role("admin", "admin")

    expert_role = Role("expert", "expert")

    applyunit_role = Role("applyunit", "applyunit")

    applicant_role = Role("applicant", "applicant")

    admin_role.save()

    expert_role.save()

    applyunit_role.save()

    applicant_role.save()

    admin_user = User(None, "138xxxxxxxx", "admin", "admin", [admin_role], "系统管理员", "")

    expert_user = User(None, "139xxxxxxxx", "expert", "expert", [expert_role], "评审专家", "")

    admin_user.save()

    expert_user.save()


if __name__ == "__main__":

    manager.run()
