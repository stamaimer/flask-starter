# coding: utf-8

"""

    app.admin.user
    ~~~~~~~~~~~~~~

    stamaimer 04/25/17

"""


from . import AppModelView


class UserModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime", "password"]

    form_excluded_columns = ["answers", "create_datetime", "update_datetime"]

    column_searchable_list = ["email", "username"]

    labels = dict(roles=u"权限", email=u"邮箱", active=u"状态", username=u"姓名", password=u"密码")

    column_labels = labels
