# coding: utf-8

"""

    app.admin
    ~~~~~~~~~

    stamaimer 04/25/17

"""


from flask import redirect, request, url_for

from flask_security import current_user

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.model import db
from app.model import Role
from app.model import User
from app.model import Answer
from app.model import Question


class AppModelView(ModelView):

    # def is_accessible(self):
    #
    #     return current_user.has_role("admin")
    #
    # def inaccessible_callback(self, name, **kwargs):
    #
    #     return redirect(url_for("security.login", next=request.url))

    pass


admin = Admin(name=u"在线答题", base_template="app_master.html", template_mode="bootstrap3")

from .file import AppFileAdmin
from .role import RoleModelView
from .user import UserModelView
from .answer import AnswerModelView
from .question import QuestionModelView


admin.add_view(RoleModelView(Role, db.session, name=u"权限"))
admin.add_view(UserModelView(User, db.session, name=u"用户"))
admin.add_view(AnswerModelView(Answer, db.session, name=u"答案记录"))
admin.add_view(QuestionModelView(Question, db.session, name=u"问题列表"))
# admin.add_view(AppFileAdmin("app/static", "/static/", name="Static Files"))
