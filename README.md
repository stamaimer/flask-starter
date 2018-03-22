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

    # sudo yum install mariadb-server
    
    # sudo mysql_secure_installation
    
    # sudo systemctl start/enable/status mariadb

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
    
    # sudo yum install nginx
    
    # sudo systemctl start/enable/status nginx
    
    # create sites-available & sites-enabled directory in /etc/nginx 
    
    # create config file in sites-available
    
        upstream stamaimer {
            server 127.0.0.1:5000;
            server 127.0.0.1:5001;
            server 127.0.0.1:5002;
        }

        server{
            listen 80;
            server_name example.com;
            
            location / {
                proxy_pass http://stamaimer;
    
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
            }
            
            location /static {
                alias <path to static directory for your project>;
                expires max;
            }
        }
        
    # sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/example.com
    
    # add `include /etc/nginx/sites-enabled/*;` after `include /etc/nginx/conf.d/*.conf;`
    
    # sudo systemctl restart nginx
    
#### Deployment with Docker
    - git clone https://github.com/stamaimer/flask-starter
    - cd flask-starter
    - docker-compose up

#### To Do

- Test
    
