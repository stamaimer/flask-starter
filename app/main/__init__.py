# coding: utf-8

"""

    app.main
    ~~~~~~~~

    stamaimer 04/25/17

"""


import flask

from flask import redirect

from flask_security import login_required


main = flask.Blueprint("main", __name__)


@main.route('/')
@main.route("/index")
def index():

    return redirect("/admin")


@main.route("/submit/<int:id>")
@login_required
def submit(id):

    return "<html>" \
           "    <head>" \
           "        <script>" \
           "            history.go(-1);" \
           "        </script>" \
           "    </head>" \
           "</html>"