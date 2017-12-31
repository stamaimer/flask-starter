# -*- coding: utf-8 -*-

"""

    app.model.project
    ~~~~~~~~~~~~~~~~~

    stamaimer 12/27/17

"""


from . import db, AppModel


class Project(AppModel):

    pro_name = db.Column(db.String(128), nullable=False)

    pro_time = db.Column(db.String(128), nullable=False)

    pro_type = db.Column(db.String(128), nullable=False)  # 项目类别

    sub_type = db.Column(db.String(128), nullable=False)  # 学科类别

    res_type = db.Column(db.String(128), nullable=False)  # 研究类型

    res_form = db.Column(db.String(128), nullable=False)  # 预期成果

    keywords = db.Column(db.String(128), nullable=False)

    create_user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    create_user = db.relationship("User", foreign_keys=create_user_id)

    status = db.Column(db.Enum(u"创建中", u"审批中", u"已驳回", u"已通过"), default=u"创建中")

    current_audit_id = db.Column(db.Integer(), db.ForeignKey("audit.id"))

    current_audit = db.relationship("Audit", foreign_keys=current_audit_id, uselist=0, cascade="all,delete", post_update=1)
