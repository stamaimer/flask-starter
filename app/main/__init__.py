# coding: utf-8

"""

    app.main
    ~~~~~~~~

    stamaimer 04/25/17

"""


import flask


main = flask.Blueprint("main", __name__)


@main.route('/')
@main.route("/index")
def index():

    return "Hello, Flask Starter!"
