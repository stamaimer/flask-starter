### Flask-Stater

A starter template for Flask based web application.

#### Features

- ORM by Flask-SQLAlchemy
- Manage script by Flask-Script
- Dashboard based on Flask-admin
- Real-time error tracking by raven
- Internationalization by Flask-Babel
- Database migrations by Flask-Migrate
- Server-side session by Flask-Session
- Security mechanisms by Flask-Security
- Views separated by Blueprint from Flask

#### Deployment

    git clone https://github.com/stamaimer/flask-starter
    
    cd flask-starter
    
    cp instance/config.example.py instance/config.py  # change the user and pswd fields
    
    ./create_venv
    
    source .venv/bin/activate
    
    python manage.py create_user -p <password for root of mysql>  # create user specified in instance/config.py
    
    python manage.py create_db  
    
    # create tables 
    
    python manage.py db init
    
    python manage.py db migrate
    
    python manage.py db upgrade
    
    python manage.py runserver -h 0.0.0.0 or ./start.sh
    
#### To Do

- Test
- Docker
    