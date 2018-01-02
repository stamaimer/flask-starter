# -*- coding: utf-8 -*-

"""

    app.model.recommender
    ~~~~~~~~~~~~~~~~~~~~~

    stamaimer 01/01/18

"""


from . import db, AppModel


class Recommender(AppModel):

    name = db.Column(db.String(128), nullable=False)

    work = db.Column(db.String(128), nullable=False)

    title = db.Column(db.String(128), nullable=False)

    advice = db.Column(db.Text(), nullable=False)

    project_id = db.Column(db.Integer(), db.ForeignKey("project.id"))

    project = db.relationship("Project", foreign_keys=project_id, backref="recommenders")