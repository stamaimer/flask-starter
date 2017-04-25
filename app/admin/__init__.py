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


class AppModelView(ModelView):

    def is_accessible(self):

        return current_user.has_role("admin")

    def inaccessible_callback(self, name, **kwargs):

        return redirect(url_for("security.login", next=request.url))


admin = Admin(name="Dashboard", base_template="app_master.html", template_mode="bootstrap3")

from .file import AppFileAdmin
from .role import RoleModelView
from .user import UserModelView


admin.add_view(RoleModelView(Role, db.session, name="Role"))
admin.add_view(UserModelView(User, db.session, name="User"))
# admin.add_view(AppFileAdmin())
