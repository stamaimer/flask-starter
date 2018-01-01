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
from flask_admin.model.template import EndpointLinkRowAction

from app.model import db
from app.model import Role
from app.model import User
from app.model import Audit
from app.model import Project


class AppModelView(ModelView):

    def is_accessible(self):

        return current_user.has_role("admin")

    def inaccessible_callback(self, name, **kwargs):

        return redirect(url_for("security.login", next=request.url))


class RoleModelView(AppModelView):

    pass


class UserModelView(AppModelView):

    column_exclude_list = ["email", "password", "update_datetime"]


class ApplyUnitModelView(AppModelView):

    def is_accessible(self):

        return current_user.has_role("admin")

    def get_query(self):

        return self.session.query(self.model).filter(self.model.roles.any(name="applyunit"))

    def get_count_query(self):

        return self.session.query(func.count('*')).select_from(self.model).filter(self.model.roles.any(name="applyunit"))

    def filter_func():

        return db.session.query(Role).filter_by(name="applyunit")

    form_args = {
        "roles": {
            "query_factory": filter_func
        }
    }

    # def on_model_change(self, form, model, is_created):
    #     if is_created:
    #         model.roles = [Role.query.filter_by(name="applyunit").first()]

    column_list = ["username", "displayname", "description", "phone"]

    form_excluded_columns = ["create_datetime", "update_datetime", "active", "email"]

    labels = dict(username=u"登陆账号", password=u"密码", displayname=u"申请单位", description=u"联系地址", phone=u"联系方式", roles=u"账号类型")

    column_labels = labels


class ApplicantModelView(AppModelView):

    def is_accessible(self):

        return current_user.has_role("applyunit")

    def get_query(self):

        return self.session.query(self.model).filter(self.model.roles.any(name="applicant"), self.model.description==current_user.displayname)

    def get_count_query(self):

        return self.session.query(func.count('*')).select_from(self.model).filter(self.model.roles.any(name="applicant"), self.model.description==current_user.displayname)

    def filter_func():

        return db.session.query(Role).filter_by(name="applicant")

    form_args = {
        "roles": {
            "query_factory": filter_func
        }
    }

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.description = current_user.displayname

    column_list = ["username", "displayname", "description", "phone"]

    form_excluded_columns = ["create_datetime", "update_datetime", "description", "active", "email"]

    labels = dict(username=u"登陆账号", password=u"密码", displayname=u"姓名", description=u"单位名称", phone=u"联系方式", roles=u"账号类型")

    column_labels = labels


class ProjectModelViewForApplicant(AppModelView):

    def is_accessible(self):

        return current_user.has_role("applicant")

    def get_query(self):

        return self.session.query(self.model).filter_by(create_user_id=current_user.id)

    def get_count_query(self):

        return self.session.query(func.count('*')).select_from(self.model).filter_by(create_user_id=current_user.id)

    def on_model_change(self, form, model, is_created):

        if is_created:

            model.create_user = current_user

    column_extra_row_actions = [
        EndpointLinkRowAction("glyphicon glyphicon-send", "main.submit")
    ]

    column_exclude_list = ["create_user", "update_datetime", "current_audit"]

    form_excluded_columns = ["create_user", "create_datetime", "update_datetime", "current_audit", "audits"]

    labels = dict(create_datetime=u"创建时间", pro_name=u"项目名称", pro_type=u"项目类别", sub_type=u"学科分类", 
    pro_time=u"起止时间", res_type=u"研究类型", res_form=u"预期成果", keywords=u"主题词", status=u"状态")

    column_labels = labels

    # inline_models = [(Audit, dict(form_columns=["id", "advice", "result"]))]


class ProjectModelViewForApplyUnit(AppModelView):

    can_edit = 0

    can_create = 0

    can_delete = 0

    def is_accessible(self):

        return current_user.has_role("applyunit") or current_user.has_role("expert") or current_user.has_role("admin")

    def get_query(self):

        return self.session.query(self.model).filter(Audit.audit_user==current_user,
                                                     Audit.result==None,
                                                     Audit.status==1,
                                                     Project.status==u"审批中").join(Project.current_audit)

    def get_count_query(self):

        return self.session.query(func.count('*')).select_from(self.model).filter(Audit.audit_user==current_user,
                                                                                  Audit.result==None,
                                                                                  Audit.status==1,
                                                                                  Project.status==u"审批中").join(Project.current_audit)

    column_extra_row_actions = [
        EndpointLinkRowAction("glyphicon glyphicon-filter", "main.audit")
    ]

    column_exclude_list = ["update_datetime", "current_audit"]

    labels = dict(create_user=u"创建人员", create_datetime=u"创建时间", pro_name=u"项目名称", pro_type=u"项目类别", sub_type=u"学科分类", 
    pro_time=u"起止时间", res_type=u"研究类型", res_form=u"预期成果", keywords=u"主题词", status=u"状态")

    column_labels = labels


admin = Admin(name=u"课题网申", base_template="app_master.html", template_mode="bootstrap3")


# admin.add_view(RoleModelView(Role, db.session, name=u"角色管理"))
# admin.add_view(UserModelView(User, db.session, name=u"用户管理"))
admin.add_view(ApplyUnitModelView(User, db.session, name=u"单位管理", endpoint="applyunit"))
admin.add_view(ApplicantModelView(User, db.session, name=u"人员管理", endpoint="applicant"))
admin.add_view(ProjectModelViewForApplicant(Project, db.session, name=u"项目创建", endpoint="project4c"))
admin.add_view(ProjectModelViewForApplyUnit(Project, db.session, name=u"项目管理", endpoint="project4u"))
