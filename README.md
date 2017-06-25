
# Catalog Project
A movie/trailer catalog application that allows simple CRUD operations on a library of trailers.

### Features:
1) Google Sign in to restrict destructive CRUD operations to signed in users
2) Movie Data Search (via OMDB API)
3) Youtube Video Search (Youtube API)
4) When you search for a movie, relevant data, posters and video for a trailer will be retreived and rendered on the same page (AJAX). You can improve search with the optional "year" field. Further you can add the searched movie to the library.

# Requirements
1) Virtualbox

# Installtion and Usage

### Start Virtualbox
1) ```vagrant init ubuntu/trusty64```
2) ```vagrant up```
3) ```vagrant ssh```

### Install Git & Download repo
4) ```sudo apt-get install git```
5) ```git clone https://github.com/xprmnts/dev_catalog.git```
6) ```mv dev_catalog/* .``` this is necessary for apache to get the right paths
7) ```rm -rf dev_catalog``` clean up

### Install dependencies
8) ```sudo ./pg_config.sh```

### Set up Database & Apache Server
9) ```sudo cp trailerApp.conf /etc/apache2/sites-available```
10) ```sudo cp apache2.conf /etc/apache2/```
11) ```sudo adduser catalog_owner```
12) ```sudo su - postgres```
13) ```createuser catalog_owner```
14) ```psql```
15) ```postgres=# CREATE DATABASE trailer_catalog OWNER catalog_owner;```
16) ```trailer_catalog=# ALTER USER catalog_owner WITH PASSWORD 'pass1234';```
17) ```\q```

### Load sample data
18) ```cd /vagrant```
19) ```psql trailer_catalog < trailer_catalog_db_backup```
20) ```exit``` switch back to vagrant user
21) ```exit``` exit the vm

### Reload VM (To take configuration from VagrantFile in repo - I made a minor tweak to port forwarding configuraiton)
22) ```vagrant reload```
23) ```vagrant ssh```
24) ```sudo service apache2 start```
25) Open browser and access site from: localhost:8080

If you followed everything right you should see something like this (link to demo):