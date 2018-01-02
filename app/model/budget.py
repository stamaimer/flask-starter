# -*- coding: utf-8 -*-

"""

    app.model.budget
    ~~~~~~~~~~~~~~~~

    stamaimer 01/02/18

"""


from . import db, AppModel


class Budget(AppModel):

    name = db.Column(db.String(128), nullable=False)

    amount = db.Column(db.Integer(), nullable=False)

    description = db.Column(db.Text(), nullable=False)

    project_id = db.Column(db.Integer(), db.ForeignKey("project.id"))

    project = db.relationship("Project", foreign_keys=project_id, backref="budgets")