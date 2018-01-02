# -*- coding: utf-8 -*-

"""

    app.model.participant
    ~~~~~~~~~~~~~~~~~~~~~

    stamaimer 01/02/18

"""


from . import db, AppModel


class Participant(AppModel):

    edu = db.Column(db.String(128), nullable=False)

    name = db.Column(db.String(128), nullable=False)

    work = db.Column(db.String(128), nullable=False)

    title = db.Column(db.String(128), nullable=False)

    degree = db.Column(db.String(128), nullable=False)

    birth = db.Column(db.Date(), nullable=False)

    gender = db.Column(db.Enum(u"男", u"女"), nullable=False)  # 性别

    research = db.Column(db.String(128), nullable=False)

    project_id = db.Column(db.Integer(), db.ForeignKey("project.id"))

    project = db.relationship("Project", foreign_keys=project_id, backref="participants")
