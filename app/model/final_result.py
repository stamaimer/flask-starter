# -*- coding: utf-8 -*-

"""

    app.model.final_result
    ~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 01/02/18

"""


from . import db, AppModel


class FinalResult(AppModel):

    bearer = db.Column(db.String(128), nullable=False)

    name = db.Column(db.String(128), nullable=False)

    form = db.Column(db.String(128), nullable=False)

    word = db.Column(db.String(128), nullable=False)

    time = db.Column(db.Date(), nullable=False)

    project_id = db.Column(db.Integer(), db.ForeignKey("project.id"))

    project = db.relationship("Project", foreign_keys=project_id, backref="final_results")

