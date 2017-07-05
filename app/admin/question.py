# -*- coding: utf-8 -*-

"""

    app.admin.question
    ~~~~~~~~~~~~~~~~~~

    stamaimer 07/05/17

"""


from . import AppModelView, Answer


class QuestionModelView(AppModelView):

    # column_exclude_list = ["update_datetime"]

    def _list_count_a(view, context, model, name):

        return Answer.query.filter_by(question_id=model.id, answer='A').count()

    def _list_count_b(view, context, model, name):

        return Answer.query.filter_by(question_id=model.id, answer='B').count()

    def _list_count_c(view, context, model, name):

        return Answer.query.filter_by(question_id=model.id, answer='C').count()

    def _list_count_d(view, context, model, name):

        return Answer.query.filter_by(question_id=model.id, answer='D').count()

    column_formatters = {
        "count_a": _list_count_a,
        "count_b": _list_count_b,
        "count_c": _list_count_c,
        "count_d": _list_count_d
    }

    column_list = ["id", "create_datetime", "correct_answer", "status", "memo",
                   "count_a", "count_b", "count_c", "count_d"]

    form_excluded_columns = ["answers", "create_datetime", "update_datetime"]

    column_editable_list = ["status"]

    labels = dict(id=u"编号", create_datetime=u"创建时间", correct_answer=u"正确答案", status=u"状态", memo=u"备注",
                  count_a='A', count_b='B', count_c='C', count_d='D')

    column_labels = labels
