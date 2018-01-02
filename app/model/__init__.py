# coding: utf-8

"""

    app.model
    ~~~~~~~~~

    stamaimer 04/25/17

"""


from sqlalchemy.sql import func

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class AppModel(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True)

    create_datetime = db.Column(db.DateTime(), default=func.now())

    update_datetime = db.Column(db.DateTime(), default=func.now())

    def save(self):

        db.session.add(self)

        db.session.commit()

    def to_dict(self):

        pass


roles_users = db.Table("roles_users",
                       db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
                       db.Column("user_id", db.Integer, db.ForeignKey("user.id")))


from .role import Role
from .user import User
from .audit import Audit
from .budget import Budget
from .project import Project
from .recommender import Recommender
from .participant import Participant
from .final_result import FinalResult
from .phased_result import PhasedResult
from .charge_person import ChargePerson
