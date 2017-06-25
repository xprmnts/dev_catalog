# vagrant init ubuntu/trusty64
# vagrant up
# vagrant ssh
# sudo apt-get install git
# git clone https://github.com/xprmnts/dev_catalog.git
# mv dev_catalog/* .
# rm -rf dev_catalog
# sudo ./pg_config.sh
# sudo cp trailerApp.conf /etc/apache2/sites-available
# sudo cp apache2.conf /etc/apache2/
# sudo adduser catalog_owner
# sudo su - postgres
# createuser catalog_owner
# psql
# postgres=# CREATE DATABASE trailer_catalog OWNER catalog_owner;
# \q
# cd /vagrant
# psql trailer_catalog < trailer_catalog_backup
# exit
# exit
# vagrant reload
# vagrant ssh
# trailer_catalog=# ALTER USER catalog_owner WITH PASSWORD 'pass1234';
# sudo service apache2 start