# coding:utf-8

"""

    instance.config
    ~~~~~~~~~~~~~~~

    stamaimer 04/25/17

"""


SECRET_KEY = "flask-starter"

SENTRY_DSN = ""

SECURITY_PASSWORD_SALT = "flask-starter"

DB = "mysql"

DB_DRIVER = "pymysql"

DB_USER = "stamaimer"
DB_PSWD = "123456"
DB_HOST = "192.168.33.11"
DB_PORT = "3306"
DB_NAME = "flask-starter"

SQLALCHEMY_DATABASE_URI = "{db}+{db_driver}://{db_user}:{db_pswd}@{db_host}:{db_port}/{db_name}?charset=utf8".format(
    db=DB,
    db_driver=DB_DRIVER,
    db_user=DB_USER,
    db_pswd=DB_PSWD,
    db_host=DB_HOST,
    db_port=DB_PORT,
    db_name=DB_NAME
)
