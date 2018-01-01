# coding: utf-8

"""

    app.main
    ~~~~~~~~

    stamaimer 04/25/17

"""


import traceback

import flask

from flask import abort, current_app, redirect

from flask_security import login_required

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
