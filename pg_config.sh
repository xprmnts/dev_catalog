apt-get -qqy update
apt-get -qqy upgrade
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-sqlalchemy
apt-get -qqy install python-pip
apt-get install apache2 apache2-doc apache2-utils
apt-get install libapache2-mod-wsgi python-dev
a2enmod wsgi
pip install --upgrade pip
pip install werkzeug
pip install flask
pip install Flask-Login
pip install oauth2client
pip install requests
pip install httplib2
pip install google-api-python-client
pip install psycopg2
pip install SQLAlchemy
pip install urllib

