# coding: utf-8

"""

    app.extension.migrate
    ~~~~~~~~~~~~~~~~~~~~~

    stamaimer 04/26/17

"""


from flask_migrate import Migrate

from app.model import db


migrate = Migrate(db)
