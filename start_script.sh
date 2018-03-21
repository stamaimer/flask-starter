/flask-starter/wait-for-it.sh db:3306
python manage.py create_user -p $MYSQL_ROOT_PASSWORD
python manage.py create_db
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
python manage.py runserver -h 0.0.0.0