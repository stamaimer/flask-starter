# coding: utf-8

"""

    app.main
    ~~~~~~~~

    stamaimer 04/25/17

"""


import traceback

import flask

from flask import abort, current_app, jsonify, render_template, request

from flask_security import current_user, login_required

from app.model import db, Answer, Question


main = flask.Blueprint("main", __name__)


@main.app_errorhandler(500)
def not_found(e):

    return e.description.decode("utf-8"), 500, {"content-type": "text/plain; charset=utf-8"}


@main.route('/')
def index():

    question = Question.query.filter_by(status=1).order_by(Question.create_datetime.desc()).first()

    return render_template("index.html", question_id=question.id)


@main.route("/answer", methods=["POST"])
@login_required
def create_answer():

    try:

        request_json = request.get_json()

        answer = request_json.get("answer")

        question_id = request_json.get("question_id")

        question = Question.query.filter_by(status=1).order_by(Question.create_datetime.desc()).first()

        if question.id == int(question_id):

            answer = Answer(answer, current_user.id, question_id)

            answer.save()

            data_dict = dict(answer_id=answer.id)

            return jsonify(data_dict)

        else:

            return "Bad Request", 400

    except:

        db.session.rollback()

        current_app.logger.error(traceback.format_exc())

        abort(500, traceback.format_exc())
