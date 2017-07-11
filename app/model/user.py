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

    answers = db.relation("Answer", backref="user", lazy="dynamic")

    def __init__(self, email="", username="", password="", roles=None, active=True):

        self.email = email

        self.roles = roles if roles else []

        self.active = active

        self.username = username

        self.password = password

    def __repr__(self):

        return self.username
