# -*- coding: utf-8 -*-

"""

    app.model.audit
    ~~~~~~~~~~~~~~~

    stamaimer 12/30/17

"""


from . import db, AppModel


class Audit(AppModel):

    next_id = db.Column(db.Integer(), db.ForeignKey("audit.id"))

    _next_ = db.relationship("Audit", remote_side="Audit.id", backref=db.backref("last", uselist=0), uselist=0,
                             post_update=1, cascade="all,delete")

    advice = db.Column(db.Text())

    status = db.Column(db.Boolean(), default=0)

    result = db.Column(db.Enum(u"同意", u"驳回"))

    audit_user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    audit_user = db.relationship("User", foreign_keys=audit_user_id)

    project_id = db.Column(db.Integer(), db.ForeignKey("project.id"))

    project = db.relationship("Project", foreign_keys=project_id, backref="audits")
    