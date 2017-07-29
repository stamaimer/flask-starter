# coding: utf-8

"""

    app.model.role
    ~~~~~~~~~~~~~~

    stamaiemer 04/25/17

"""


from flask_security import RoleMixin

from . import db
from . import AppModel


class Role(AppModel, RoleMixin):

    name = db.Column(db.String(128), nullable=False, unique=True)

    description = db.Column(db.String(128))

    def __init__(self, name="", description=""):

        self.name = name

        self.description = description

    def __repr__(self):

        return self.description
