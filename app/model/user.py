# coding: utf-8

"""

    app.model.user
    ~~~~~~~~~~~~~~

    stamaimer 04/25/17

"""


from flask import current_app

from flask_security import UserMixin

from . import db, roles_users
from . import AppModel


class User(AppModel, UserMixin):

    email = db.Column(db.String(128), nullable=False, unique=True)

    active = db.Column(db.Boolean, default=True)

    username = db.Column(db.String(128), nullable=False, unique=True)

    password = db.Column(db.String(128), nullable=False)

    roles = db.relationship("Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic"))

    if current_app.config["SECURITY_TRACKABLE"]:

        login_count = db.Column(db.Integer)

        last_login_at = db.Column(db.DateTime)

        last_login_ip = db.Column(db.String(15))

        current_login_at = db.Column(db.DateTime)

        current_login_ip = db.Column(db.String(15))

    if current_app.config["SECURITY_CONFIRMABLE"]:

        confirmed_at = db.Column(db.DateTime)

    def __repr__(self):

        return self.username
