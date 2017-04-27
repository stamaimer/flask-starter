# coding: utf-8

"""

    config.default
    ~~~~~~~~~~~~~~

    stamaimer 04/25/17

"""


class DefaultConfig(object):

    DEBUG = True

    SECURITY_TRACKABLE = False

    SECURITY_CHANGEABLE = False

    SECURITY_CONFIRMABLE = False

    SECURITY_RECOVERABLE = False

    SECURITY_PASSWORDLESS = False

    SECURITY_REGISTERABLE = False

    SECURITY_PASSWORD_HASH = "bcrypt"

    SECURITY_USER_IDENTITY_ATTRIBUTES = ("email", )  # https://github.com/mattupstate/flask-security/issues/124

    SQLALCHEMY_TRACK_MODIFICATIONS = False
