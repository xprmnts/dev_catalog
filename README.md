
# Catalog Project
A movie/trailer catalog application that allows simple CRUD operations on a library of trailers.

# REVIEWER UPDATE
- The Google Sign in functionality *may* not work from your local host - it does work from the [demo](bskt.ca) site - so while the app might run on your local host not all the functionality will work
- In order for the app to work on localhost you have to modify the client_secrets.json with your own and set up the google api for the sign in. Instructions below.

### Features:
1) Google Sign in to restrict destructive CRUD operations to signed in users
2) Movie Data Search (via OMDB API)
3) Youtube Video Search (Youtube API)
4) When you search for a movie, relevant data, posters and video for a trailer will be retreived and rendered on the same page (AJAX). You can improve search with the optional "year" field. Further you can add the searched movie to the library.

# Requirements
1) Virtualbox

# Installtion and Usage (on macOS)

### Start Virtualbox
1) $```vagrant init ubuntu/trusty64```
2) $```vagrant up```
3) $```vagrant ssh```

### Install Git & Download repo
4) $```sudo apt-get install git -y```
5) $```cd /vagrant```
6) $```git clone https://github.com/xprmnts/dev_catalog.git```
7) $```mv dev_catalog/* .``` this is necessary for apache to get the right paths that I've configured
8) $```rm -rf dev_catalog``` clean up

### Install dependencies
9) $```sudo ./pg_config.sh``` this will take a few minutes, it might seem like nothing is happening for the first 4-5 mins...but just wait.

### Set up Database & Apache Server
10) $```sudo cp trailerApp.conf /etc/apache2/sites-available```
11) $```sudo cp trailerApp.conf /etc/apache2/sites-enabled```
12) $```sudo cp apache2.conf /etc/apache2/```
13) $```sudo service apache2 reload``` (if server isn't started you might have to run start instead of reload)
13) $```sudo adduser catalog_owner```
14) $```sudo su - postgres```
15) $```createuser catalog_owner```
16) $```psql```
17) postgres=#```CREATE DATABASE trailer_catalog OWNER catalog_owner;```
18) postgres=#```\q```
19) $```psql trailer_catalog```
20) trailer_catalog=# ```ALTER USER catalog_owner WITH PASSWORD 'pass1234';``` You should use this password as I've configured the app to use this password, you can change it if you want but you'll have to change the dbsetup.py file to use your password.
21) ```\q``` exit out of the sql editor

### Load sample data
22) $```cd /vagrant```
23) $```psql trailer_catalog < trailer_catalog_db_backup.sql```
24) $```exit``` switch back to vagrant user
25) $```exit``` exit the vm

### Reload VM (To take configuration from VagrantFile in repo - I made a minor tweak to port forwarding configuraiton)
26) $```vagrant reload```
27) $```vagrant ssh```
28) $```sudo service apache2 start```
29) Open browser and access site from: localhost:8000

If you followed everything right you should see something like this [Demo](http://bskt.ca/)

The one thing that's a little suspect is step 11 - typically you'd run sudo a2ensite on the trailerApp.conf file in sites-available and a2dissite on the default apache file - but in all the test runs I did the steps above worked.

### Some tips:
- The Genre Page: use /images/genre_background.jpg for a generic background, or use an image url
- The Trailer Page: Use the search feature to find a movie to add to the db ... or do it manually
- Try Logan and 2017 in search page for title and year or wonder woman!
- There may be bugs if you dont clear cache on your browser ... use incognito mode just in case.

### Google Sign In:
1) Go to your app's page in the Google APIs Console — https://console.developers.google.com/apis
2) Create a project from the dropdown on the top nav
3) Once the project is set up, select it in the dropdown on the top nav to go to it
4) Choose Credentials from the menu on the left.
5) It will ask you to configure consent screen
6) Enter your email and the app name: "Trailr Catalog App"
7) Create Credentials > select OAuth Client ID
8) Choose Web Application in the following screen
9) It will ask you to add origins and redirects:
	- Origins:
		- http://localhost:8000
	- Redirects:
		- http://localhost:8000/login
		- http://localhost:8000/gconnect
10) You will then be able to download the client ID and client secret - name it client_secrets.json
11) Overrite the existing file with your own
12) This should enable the google sign in functionality after you reload the server in the vagrant vm
13) Open the login.html page in the templates folder and modify the existing data-clientid attribute to use your newly generated client id.

# The following JSON Endpoints are allowed
1) '/genres/JSON'
2) '/trailers/JSON'
3) '/users/JSON'
4) '/genres/<int:genre_id>/trailers/JSON'
5) '/genres/<int:genre_id>/trailers/<int:trailer_id>/JSON'

# Future TODO:
1) I'd like to make use of configuration files to abstract out the API key's I used
2) The login UI needs work, will add email auth and facebook oauth next
3) Should optimize search to take into account already existing items in db before calling API's
4) Should restrict CRUD to only add NEW items, currently duplicates are allowed
