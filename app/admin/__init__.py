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
from flask_admin.contrib.sqla.view import func

from app.model import db
from app.model import Role
from app.model import User
from app.model import Project


class AppModelView(ModelView):

    def is_accessible(self):

        return current_user.has_role("admin")

    def inaccessible_callback(self, name, **kwargs):

        return redirect(url_for("security.login", next=request.url))


class RoleModelView(AppModelView):

    pass


class UserModelView(AppModelView):

    pass


class ApplyUnitModelView(AppModelView):

    def is_accessible(self):

        return current_user.has_role("admin")

    def get_query(self):

        return self.session.query(self.model).filter(self.model.roles.any(name="applyunit"))

    def get_count_query(self):

        return self.session.query(func.count('*')).select_from(self.model).filter(self.model.roles.any(name="applyunit"))

    column_list = ["username", "displayname", "description", "phone"]

    form_excluded_columns = ["create_datetime", "update_datetime", "active", "email"]

    labels = dict(username=u"登陆账号", password=u"密码", displayname=u"申请单位", description=u"联系地址", phone=u"联系方式", roles=u"账号类型")

    column_labels = labels


class ApplicantModelView(AppModelView):

    def is_accessible(self):

        return current_user.has_role("applyunit")

    def get_query(self):

        return self.session.query(self.model).filter(self.model.roles.any(name="applicant"))

    def get_count_query(self):

        return self.session.query(func.count('*')).select_from(self.model).filter(self.model.roles.any(name="applicant"))

    column_list = ["username", "displayname", "description", "phone"]

    form_excluded_columns = ["create_datetime", "update_datetime", "active", "email"]

    labels = dict(username=u"登陆账号", password=u"密码", displayname=u"姓名", description=u"单位名称", phone=u"联系方式", roles=u"账号类型")

    column_labels = labels


class ProjectModelViewForApplyUnit(AppModelView):

    def is_accessible(self):

        return current_user.has_role("applicant")

    def get_query(self):

        return self.session.query(self.model).filter_by(create_user_id=current_user.id)

    def get_count_query(self):

        return self.session.query(func.count('*')).select_from(self.model).filter_by(create_user_id=current_user.id)

    form_excluded_columns = ["create_datetime", "update_datetime", "current_audit"]

    column_list = ["create_datetime", "pro_name", "pro_type", "sub_type", "pro_time", "res_type", "res_form", "keywords", "status"]

    labels = dict(current_audit=u"审批流程", create_datetime=u"创建时间", update_datetime=u"修改时间", pro_name=u"项目名称", pro_type=u"项目类别",
                sub_type=u"学科分类", pro_time=u"起止时间", res_type=u"研究类型", res_form=u"预期成果", keywords=u"主题词", status=u"状态")

    column_labels = labels


admin = Admin(name=u"课题网申", base_template="app_master.html", template_mode="bootstrap3")


admin.add_view(RoleModelView(Role, db.session, name=u"角色管理"))
admin.add_view(UserModelView(User, db.session, name=u"用户管理"))
admin.add_view(ApplyUnitModelView(User, db.session, name=u"申请单位管理", endpoint="applyunit"))
admin.add_view(ApplicantModelView(User, db.session, name=u"申请人员管理", endpoint="applicant"))
admin.add_view(ProjectModelViewForApplyUnit(Project, db.session, name=u"项目创建"))
