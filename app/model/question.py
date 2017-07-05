# -*- coding: utf-8 -*-

"""

    app.model.question
    ~~~~~~~~~~~~~~~~~~

    stamaimer 07/05/17

"""


from . import AppModel, db


class Question(AppModel):

    correct_answer = db.Column(db.Enum('A', 'B', 'C', 'D'))

    # count_of_a = db.Column(db.Integer())
    #
    # count_of_b = db.Column(db.Integer())
    #
    # count_of_c = db.Column(db.Integer())
    #
    # count_of_d = db.Column(db.Integer())

    status = db.Column(db.Boolean(), default=0)

    memo = db.Column(db.Text())

    answers = db.relation("Answer", backref="question", lazy="dynamic")

    def __repr__(self):

        return u"正确答案：{}，备注：{}".format(self.correct_answer, self.memo)
