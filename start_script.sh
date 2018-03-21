python manage.py create_user -p $MYSQL_ROOT_PASSWORD
python manage.py create_db
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
python manage.py runserver