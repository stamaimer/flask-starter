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

    email = db.Column(db.String(128), unique=True)

    phone = db.Column(db.String(128), unique=True, nullable=False)

    active = db.Column(db.Boolean, default=True)

    username = db.Column(db.String(128), unique=True, nullable=False)

    displayname = db.Column(db.String(128), nullable=False)

    description = db.Column(db.String(128), nullable=False)

    password = db.Column(db.String(128), nullable=False)

    roles = db.relationship("Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic"))

    def __init__(self, email="", phone="", username="", password="", roles=[], displayname="", description=""):

        self.email = email

        self.phone = phone

        self.roles = roles

        self.username = username

        self.password = password

        self.displayname = displayname

        self.description = description

    def __repr__(self):

        return self.displayname
