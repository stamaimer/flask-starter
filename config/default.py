# coding: utf-8

"""

    config.default
    ~~~~~~~~~~~~~~

    stamaimer 04/25/17

"""


class DefaultConfig(object):

    DEBUG = True

    SENTRY_USER_ATTRS = ["email", "username"]

    SESSION_TYPE = "filesystem"

    SECURITY_REGISTERABLE = True

    SECURITY_SEND_REGISTER_EMAIL = False

    SECURITY_PASSWORD_HASH = "bcrypt"

    SECURITY_USER_IDENTITY_ATTRIBUTES = ("username", )  # https://github.com/mattupstate/flask-security/issues/124

    SQLALCHEMY_TRACK_MODIFICATIONS = False
