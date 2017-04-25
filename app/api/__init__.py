# coding: utf-8

"""

    app.api
    ~~~~~~~

    stamaimer 04/25/17

"""


import flask


api = flask.Blueprint("api", __name__, url_prefix="/api")
