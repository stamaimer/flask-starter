# coding: utf-8

"""

    app.extension.security
    ~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 04/25/17

"""


from flask_security import Security, SQLAlchemyUserDatastore

from app.model import db
from app.model import Role
from app.model import User


user_datastore = SQLAlchemyUserDatastore(db, User, Role)

security = Security(datastore=user_datastore)
