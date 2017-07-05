# -*- coding: utf-8 -*-

"""

    app.form
    ~~~~~~~~

    stamaimer 07/05/17

"""


from wtforms.fields import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

from flask_security.forms import LoginForm, RegisterForm


class AppLoginForm(LoginForm):

    email = StringField(u"邮箱", [DataRequired(), Email()])

    password = PasswordField(u"密码", [DataRequired()])

    remember = BooleanField(u"记住我")

    submit = SubmitField(u"登录")


class AppRegisterForm(RegisterForm):

    email = StringField(u"邮箱", [DataRequired(), Email()])

    username = StringField(u"姓名", [DataRequired()])

    password = PasswordField(u"密码", [DataRequired()])

    password_confirm = PasswordField(u"确认密码", [DataRequired(), EqualTo("password")])

    submit = SubmitField(u"注册")
