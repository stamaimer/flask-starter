# coding: utf-8

"""

    app.main
    ~~~~~~~~

    stamaimer 04/25/17

"""


import flask

from flask import render_template

from flask_security import login_required


main = flask.Blueprint("main", __name__)


@main.route('/')
def index():

    return render_template("index.html")

