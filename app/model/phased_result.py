# -*- coding: utf-8 -*-

"""

    app.model.phased_result
    ~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 01/02/18

"""


from . import db, AppModel


class PhasedResult(AppModel):

    name = db.Column(db.String(128), nullable=False)

    form = db.Column(db.String(128), nullable=False)

    phase = db.Column(db.String(128), nullable=False)

    bearer = db.Column(db.String(128), nullable=False)

    project_id = db.Column(db.Integer(), db.ForeignKey("project.id"))

    project = db.relationship("Project", foreign_keys=project_id, backref="phased_results")