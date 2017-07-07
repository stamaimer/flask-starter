# -*- coding: utf-8 -*-

"""

    app.admin.answer
    ~~~~~~~~~~~~~~~~

    stamaimer 07/05/17

"""


from . import AppModelView


class AnswerModelView(AppModelView):

    can_create = 0

    column_exclude_list = ["create_datetime", "update_datetime"]

    form_excluded_columns = ["create_datetime", "update_datetime"]

    column_filters = ["user.username", "question.id", "question.create_datetime"]

    labels = dict(user=u"用户", answer=u"答案", question=u"问题")

    column_labels = labels

    column_labels["user.username"] = u"用户"

    column_labels["question.id"] = u"问题编号"

    column_labels["question.create_datetime"] = u"问题创建时间"
