# -*- coding: utf-8 -*-

"""

    app.model.answer
    ~~~~~~~~~~~~~~~~

    stamaimer 07/05/17

"""


from . import AppModel, db


class Answer(AppModel):

    answer = db.Column(db.Enum('A', 'B', 'C', 'D'))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))

    def __repr__(self):

        pass
