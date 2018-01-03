# coding: utf-8

"""

    app.admin
    ~~~~~~~~~

    stamaimer 04/25/17

"""


from datetime import date
from jinja2 import Markup

from flask import flash, redirect, request, url_for

from flask_security import current_user

from flask_admin import Admin, form
from flask_admin.base import expose
from flask_admin.form import FormOpts
from flask_admin.babel import gettext
from flask_admin.helpers import get_redirect_target
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.view import func
from flask_admin.model.helpers import get_mdict_item_or_list
from flask_admin.model.template import EndpointLinkRowAction

from app.model import db
from app.model import Role, User, Audit, Budget, Project, Recommender, Participant, FinalResult, PhasedResult, ChargePerson


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

    can_export = 1

    can_view_details = 1

    def is_accessible(self):

        return current_user.has_role("applicant")

    def get_query(self):

        return self.session.query(self.model).filter_by(create_user_id=current_user.id)

    def get_count_query(self):

        return self.session.query(func.count('*')).select_from(self.model).filter_by(create_user_id=current_user.id)

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        """
            Edit model view
        """
        return_url = get_redirect_target() or self.get_url('.index_view')

        if not self.can_edit:
            return redirect(return_url)

        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)

        model = self.get_one(id)

        if model is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(return_url)

        if model.status != u"创建中":
            flash(u"当前项目已经提交审批，不能编辑", "error")
            return redirect(return_url)

        form = self.edit_form(obj=model)
        if not hasattr(form, '_validated_ruleset') or not form._validated_ruleset:
            self._validate_form_instance(ruleset=self._form_edit_rules, form=form)

        if self.validate_form(form):
            if self.update_model(form, model):
                flash(gettext('Record was successfully saved.'), 'success')
                if '_add_another' in request.form:
                    return redirect(self.get_url('.create_view', url=return_url))
                elif '_continue_editing' in request.form:
                    return redirect(request.url)
                else:
                    # save button
                    return redirect(self.get_save_return_url(model, is_created=False))

        if request.method == 'GET' or form.errors:
            self.on_form_prefill(form, id)

        form_opts = FormOpts(widget_args=self.form_widget_args,
                             form_rules=self._form_edit_rules)

        if self.edit_modal and request.args.get('modal'):
            template = self.edit_modal_template
        else:
            template = self.edit_template

        return self.render(template,
                           model=model,
                           form=form,
                           form_opts=form_opts,
                           return_url=return_url)

    @expose("/delete/", methods=("POST", ))
    def delete_view(self):

        return_url = get_redirect_target() or self.get_url('.index_view')

        if not self.can_delete:
            return redirect(return_url)

        form = self.delete_form()

        if self.validate_form(form):
            # id is InputRequired()
            id = form.id.data

            model = self.get_one(id)

            if model is None:
                flash(gettext('Record does not exist.'), 'error')
                return redirect(return_url)

            if model.status != u"创建中":
                flash(u"当前项目已经提交审批，不能删除", "error")
                return redirect(return_url)

            # message is flashed from within delete_model if it fails
            if self.delete_model(model):
                flash(gettext('Record was successfully deleted.'), 'success')
                return redirect(return_url)
        else:
            flash_errors(form, message='Failed to delete record. %(error)s')

        return redirect(return_url)

    def on_model_change(self, form, model, is_created):

        if is_created:

            model.create_user = current_user

    def _list_audit_process(view, context, model, name):

        audits = Audit.query.filter_by(project_id=model.id, status=1)\
            .order_by(Audit.update_datetime).all()

        return Markup("<br />".join(["<pre>" + item.__repr__() + "</pre>" for item in audits]))

    def _list_recommenders(view, context, model, name):

        recommenders = Recommender.query.filter_by(project_id=model.id).order_by(Recommender.create_datetime).all()

        rows = ''

        for recommender in recommenders:

            rows += "<tr>"

            for attr in ["name", "work", "title", "advice"]:

                rows += "<td>" + getattr(recommender, attr) + "</td>"

            rows += "</tr>"

        return Markup("<table class='table'><tr><th>姓名</th><th>工作单位</th><th>专业职称</th><th>意见</th></tr>%s</table>".decode("utf-8") % rows)

    def _list_participants(view, context, model, name):

        participants = Participant.query.filter_by(project_id=model.id).order_by(Participant.create_datetime).all()

        rows = ''

        for participant in participants:

            rows += "<tr>"

            for attr in ["name", "gender", "birth", "title", "research", "edu", "degree", "work"]:

                data = getattr(participant, attr)

                rows += "<td>" + (str(data) if type(data) is date else data) + "</td>"

            rows += "</tr>"

        return Markup("<table class='table'><tr><th>姓名</th><th>性别</th><th>出生年月</th><th>专业职称</th><th>研究专长</th><th>学历</th><th>学位</th><th>工作单位</th></tr>%s</table>".decode("utf-8") % rows)

    def _list_phased_results(view, context, model, name):

        phased_results = PhasedResult.query.filter_by(project_id=model.id)

        rows = ''

        for phased_result in phased_results:

            rows += "<tr>"

            for attr in ["name", "phase", "form", "bearer"]:

                rows += "<td>" + getattr(phased_result, attr) + "</td>"

            rows += "</tr>"

        return Markup("<table class='table'><tr><th>成果名称</th><th>研究阶段</th><th>成果形式</th><th>承担人</th></tr>%s</table>".decode("utf-8") % rows)

    def _list_final_results(view, context, model, name):

        final_results = FinalResult.query.filter_by(project_id=model.id)

        rows = ''

        for final_result in final_results:

            rows += "<tr>"

            for attr in ["name", "time", "form", "word", "bearer"]:

                data = getattr(final_result, attr)

                rows += "<td>" + (str(data) if type(data) is date else data) + "</td>"

            rows += "</tr>"

        return Markup("<table class='table'><tr><th>成果名称</th><th>完成时间</th><th>成果形式</th><th>预计字数</th><th>完成人</th></tr>%s</table>".decode("utf-8") % rows)

    def _list_budgets(view, context, model, name):

        budgets = Budget.query.filter_by(project_id=model.id)

        rows = ''

        for budget in budgets:

            rows += "<tr>"

            for attr in ["name", "description", "amount"]:

                data = getattr(budget, attr)

                rows += "<td>" + (str(data) if type(data) is int else data) + "</td>"

            rows += "</tr>"

        return Markup("<table class='table'><tr><th>经费开支科目</th><th>预算经费</th><th>金额（元）</th></tr>%s</table>".decode("utf-8") % rows)

    def _list_charge_person(view, context, model, name):

        charge_person = ChargePerson.query.filter_by(project_id=model.id).first()

        if not charge_person: return ""

        row = "<tr>"

        for attr in ["name", "gender", "ethnic", "birth", "duty", "title", "research", "edu", "degree", "phone", "work", "email", "addr", "zip"]:

            data = getattr(charge_person, attr)

            row += "<td>" + (str(data) if type(data) is date else data) + "</td>"

        row += "</tr>"

        return Markup("<table class='table'><tr><th>姓名</th><th>性别</th><th>民族</th><th>出生年月</th><th>行政职务</th><th>专业职称</th><th>研究专长</th><th>最后学历</th><th>最后学位</th><th>联系电话</th><th>工作单位</th><th>Email</th><th>通讯地址</th><th>邮政编码</th></tr>%s</table>".decode("utf-8") % row)

    def _list_file(view, context, model, name):

        if not model.path:

            return ""

        return Markup("<a href='%s'>%s</a>" % (url_for("static", filename= "files/" + model.path), model.path))

    def namegen(obj, file_data):

        return file_data.filename

    column_formatters = {
        "audit_process": _list_audit_process,
        "recommenders": _list_recommenders,
        "participants": _list_participants,
        "phased_results": _list_phased_results,
        "final_results": _list_final_results,
        "budgets": _list_budgets,
        "charge_person": _list_charge_person,
        "path": _list_file
    }

    column_extra_row_actions = [
        EndpointLinkRowAction("glyphicon glyphicon-send", "main.submit")
    ]

    form_overrides = {
        'path': form.FileUploadField
    }

    form_args = {
        'path': {
            'label': u'附件',
            'base_path': "app/static/files",
            'allow_overwrite': False,
            'namegen': namegen
        }
    }

    column_details_list = ["create_datetime", "pro_name", "pro_type", "sub_type", "pro_time", "res_type", "res_form", "keywords", "status", "path",
    "charge_person", "recommenders", "participants", "phased_results", "final_results", "budgets", "other_source_of_funding", "funding_management_unit", "audit_process"]

    column_exclude_list = ["create_user", "update_datetime", "current_audit", "other_source_of_funding", "funding_management_unit", "path"]

    column_searchable_list = ["pro_name", "pro_type", "pro_time", "sub_type", "res_type", "keywords", "status"]

    column_filters = column_searchable_list

    column_export_exclude_list = ["create_user", "current_audit", "update_datetime", "path"]

    form_excluded_columns = ["create_user", "create_datetime", "update_datetime", "current_audit", "audits", "status"]

    labels = dict(create_datetime=u"创建时间", pro_name=u"项目名称", pro_type=u"项目类别", sub_type=u"学科分类", path=u"附件",
    pro_time=u"起止时间", res_type=u"研究类型", res_form=u"预期成果", keywords=u"主题词", word_counts=u"字数", status=u"状态", 
    audit_process=u"审批意见", recommenders=u"推荐人", participants=u"参加者", phased_results=u"阶段性成果", final_results=u"最终成果", 
    budgets=u"项目经费预算", other_source_of_funding=u"其他经费来源", funding_management_unit=u"经费管理单位", charge_person=u"负责人")

    column_labels = labels

    inline_models = [(ChargePerson, dict(form_columns=["id", "name", "gender", "ethnic", "birth", "duty", "title", "research", "edu", "degree", "phone", "work", "email", "addr", "zip"], column_labels=dict(name=u"姓名", gender=u"性别", ethnic=u"民族", birth=u"出生日期", duty=u"行政职务", title=u"专业职称", research=u"研究专长", edu=u"最后学历", degree=u"最后学位", phone=u"联系方式", work=u"工作单位", email=u"Email", addr=u"通讯地址", zip=u"邮政编码"))),
    (Recommender, dict(form_columns=["id", "name", "work", "title", "advice"], column_labels=dict(name=u"姓名", work=u"工作单位", title=u"专业职称", advice=u"意见"))),
    (Participant, dict(form_columns=["id", "name", "gender", "birth", "title", "research", "edu", "degree", "work"], column_labels=dict(name=u"姓名", work=u"工作单位", title=u"专业职称", gender=u"性别", birth=u"出生年月", research=u"研究专长", edu=u"学历", degree=u"学位"))),
    (PhasedResult, dict(form_columns=["id", "name", "phase", "form", "bearer"], column_labels=dict(name=u"成果名称", phase=u"研究阶段", form=u"成果形式", bearer=u"承担人"))),
    (FinalResult, dict(form_columns=["id", "name", "time", "form", "word", "bearer"], column_labels=dict(name=u"成果名称", time=u"完成时间", form=u"成果形式", word=u"预计字数", bearer=u"完成人"))), 
    (Budget, dict(form_columns=["id", "name", "description", "amount"], column_labels=dict(name=u"经费开支科目", description=u"预算经费", amount=u"金额（元）")))]



class ProjectModelViewForApplyUnit(ProjectModelViewForApplicant):

    can_edit = 0

    can_create = 0

    can_delete = 0

    can_view_details = 1

    def is_accessible(self):

        return current_user.has_role("applyunit") or current_user.has_role("expert") or current_user.has_role("admin")

    def get_query(self):

        return self.session.query(self.model).join(Audit, Audit.audit_user==current_user)

    # def get_count_query(self):

    #     return self.session.query(func.count('*')).select_from(self.model).join(Audit, Audit.audit_user==current_user)

    column_extra_row_actions = [
        EndpointLinkRowAction("glyphicon glyphicon-filter", "main.show_audit")
    ]


admin = Admin(name=u"课题网申", base_template="app_master.html", template_mode="bootstrap3")


# admin.add_view(RoleModelView(Role, db.session, name=u"角色管理"))
# admin.add_view(UserModelView(User, db.session, name=u"用户管理"))
admin.add_view(ApplyUnitModelView(User, db.session, name=u"单位管理", endpoint="applyunit"))
admin.add_view(ApplicantModelView(User, db.session, name=u"人员管理", endpoint="applicant"))
admin.add_view(ProjectModelViewForApplicant(Project, db.session, name=u"项目创建", endpoint="project4c"))
admin.add_view(ProjectModelViewForApplyUnit(Project, db.session, name=u"项目管理", endpoint="project4u"))
