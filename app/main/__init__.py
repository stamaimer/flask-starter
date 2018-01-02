# coding: utf-8

"""

    app.main
    ~~~~~~~~

    stamaimer 04/25/17

"""


import traceback

import flask

from sqlalchemy.sql import func

from flask import abort, current_app, redirect, render_template, request

from flask_security import current_user, login_required

from app.model import db
from app.model.user import User
from app.model.audit import Audit
from app.model.project import Project


main = flask.Blueprint("main", __name__)


@main.route('/')
@main.route("/index")
def index():

    return redirect("/admin")


@main.route("/submit/<int:id>")
@login_required
def submit(id):

    try:

        project = Project.query.get(id)

        if project.status == u"创建中":

            project.status = u"审批中"

            rd3_audit = Audit(audit_user=User.query.filter_by(username="expert").first(), project=project)

            rd3_audit.save()

            nd2_audit = Audit(audit_user=User.query.filter_by(username="admin").first(), project=project, next_id=rd3_audit.id)

            nd2_audit.save()

            st1_audit = Audit(audit_user=User.query.filter_by(displayname=project.create_user.description).first(), project=project, next_id=nd2_audit.id, status=1)

            st1_audit.save()

            project.current_audit = st1_audit

            db.session.commit()

            return "<html>" \
                   "    <head>" \
                   "        <script>" \
                   "            alert('提交成功');location.replace(document.referrer);" \
                   "        </script>" \
                   "    </head>" \
                   "</html>"

        else:

            return "<html>" \
                   "    <head>" \
                   "        <script>" \
                   "            alert('当前项目%s');location.replace(document.referrer);" \
                   "        </script>" \
                   "    </head>" \
                   "</html>" % project.status.encode("utf-8")

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500, traceback.format_exc())


@main.route("/audit/<int:id>")
@login_required
def show_audit(id):

    try:

        project = Project.query.get(id)

        audit = Audit.query.filter_by(audit_user=current_user, project_id=id).first()

        if project.status == u"审批中" and project.current_audit == audit and audit.status == 1 and audit.result is None:
    
            return render_template("audit.html", id=audit.id)

        else:

            return "<html>" \
                   "    <head>" \
                   "        <script>" \
                   "            alert('您现在没有权限审批当前项目！');location.replace(document.referrer);" \
                   "        </script>" \
                   "    </head>" \
                   "</html>"

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500, traceback.format_exc())


@main.route("/audit", methods=["POST"])
@login_required
def update_audit():

    try:

        id = request.form.get("id")

        audit = Audit.query.get(id)

        result = request.form.get("result")

        advice = request.form.get("advice")

        if audit.audit_user == current_user:

            audit.result = result

            audit.advice = advice

            audit.update_datetime = func.now()

            if result == u"同意":

                if audit._next_:

                    audit._next_.status = 1

                    audit.project.current_audit = audit._next_

                else:

                    audit.project.status = u"已通过"

            if result == u"驳回":

                audit.project.status = u"已驳回"

            db.session.commit()

            return redirect("/admin")

        else:

            return "Unauthorized", 401

    except:

        db.session.rollback()

        current_app.logger.error(traceback.format_exc())

        abort(500, traceback.format_exc())
