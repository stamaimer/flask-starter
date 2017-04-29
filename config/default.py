# coding: utf-8

"""

    config.default
    ~~~~~~~~~~~~~~

    stamaimer 04/25/17

"""


class DefaultConfig(object):

    DEBUG = True

    SENTRY_USER_ATTRS = ["email", "username"]

    SECURITY_PASSWORD_HASH = "bcrypt"

    SECURITY_USER_IDENTITY_ATTRIBUTES = ("email", )  # https://github.com/mattupstate/flask-security/issues/124

    SQLALCHEMY_TRACK_MODIFICATIONS = False
