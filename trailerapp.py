# Trailr App
# Author: XPRMNTS
# Python Version: 2.7.6
#------------------------------------------------------------------------------
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask import session as login_session
import random
import string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbsetup import Base, Genre, Trailer, Users

# For Youtube API
import urllib2
import urllib
import trailersearch
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from argparse import Namespace

# For Google Sign in API
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('/vagrant/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Trailr Catalog App"

engine = create_engine(
    'postgresql://catalog_owner:pass1234@localhost/trailer_catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Fake Data
# Route to Discover Page /

#Creating Users
def createUser(login_session):
    newUser = Users(username = login_session['username'], email = login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(Users).filter_by(email = login_session['email']).one()
    return user.id

def getUserInfo(users_id):
    user = session.query(Users).filter_by(id = users_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(Users).filter_by(email = email).one()
        return user.id
        print ("Returning User ID: %s" % user.id)
    except:
        return None

# TODO: Route to Login Page


@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('/vagrant/client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    # store only the access_token
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.to_json()
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    print(data)

    login_session['username'] = data['name']
    login_session['email'] = data['email']


    users_id = getUserID(login_session['email'])
    if users_id == None:
        print("User Id = NONE %s" % users_id)
        users_id = createUser(login_session)
    login_session['users_id'] = users_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash('Successfull Login.')
    return output

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    credentials = json.loads(login_session['credentials'])
    print(type(credentials))
    print(credentials)
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash('Successfully disconnected.')
        return redirect(url_for('showLandingPage'))
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# MAIN PAGE

@app.route('/')
@app.route('/discover')
def showLandingPage():
    trailers = session.query(Trailer).all()
    if 'username' not in login_session:
        loggedIn = 'false'
        return render_template('index.html', trailers=trailers, loggedIn=loggedIn, visclass="hide-links")
    else:
        loggedIn = 'true'
        return render_template('index.html', trailers=trailers, loggedIn=loggedIn)


# Route to Genres Page /genres


@app.route('/genres')
def showGenres():
    genres = session.query(Genre).all()
    if 'username' not in login_session:
        loggedIn = 'false'
        return render_template('genres.html', genres=genres, loggedIn=loggedIn, visclass="hide-links")
    else:
        loggedIn = 'true'
        return render_template('genres.html', genres=genres, loggedIn=loggedIn)

# Route to Add Genre Page /genre/addGenre


@app.route('/genres/newgenre', methods=['GET', 'POST'])
def newGenre():
    if request.method == 'POST':
        aNewGenre = Genre(
            name=request.form['name'],
            description=request.form['description'],
            num_trailers=0,
            image=request.form['image'],
            users_id=login_session['users_id'])
        session.add(aNewGenre)
        session.commit()
        return redirect(url_for('showGenres'))
    else:
        if 'username' not in login_session:
            loggedIn = 'false'
            return render_template('newGenre.html', loggedIn=loggedIn)
        else:
            loggedIn = 'true'
            return render_template('newGenre.html', loggedIn=loggedIn)

# Route to Edit selected Genre Page /genres/#/editGenre (POST)


@app.route('/genres/<int:genre_id>/editgenre', methods=['GET', 'POST'])
def editGenre(genre_id):
    currentGenre = session.query(Genre).filter_by(id=genre_id).one()
    if request.method == 'POST':
        currentGenre.name = request.form['name']
        currentGenre.description = request.form['description']
        currentGenre.image = request.form['image']
        session.add(currentGenre)
        session.commit()
        return redirect(url_for('showGenres'))
    else:
        if 'username' not in login_session:
            loggedIn = 'false'
            return render_template('editGenre.html', genre_id=genre_id, genre=currentGenre, loggedIn=loggedIn)
        else:
            loggedIn = 'true'
            if currentGenre.users_id != login_session['users_id']:
                return "<script>function myFunction(){alert('Unauthorized');}</script><body onload='myFunction()''>"
            return render_template('editGenre.html', genre_id=genre_id, genre=currentGenre, loggedIn=loggedIn)

# Route to Delete selected Genre Page /genres/#/deleteGenre (DELTE Method)
# TODO: Generate a popup instead of sending to new page


@app.route('/genres/<int:genre_id>/deletegenre', methods=['GET', 'POST'])
def deleteGenre(genre_id):
    currentGenre = session.query(Genre).filter_by(id=genre_id).one()
    if request.method == 'POST':
        trailersToDelete = session.query(Trailer).filter_by(genre_id=genre_id).all()
        for trailer in trailersToDelete:
            session.delete(trailer)
        session.delete(currentGenre)
        session.commit()
        return redirect(url_for('showGenres'))
    else:
        if 'username' not in login_session:
            loggedIn = 'false'
            return render_template('deleteGenre.html', genre_id=genre_id, genre=currentGenre, loggedIn=loggedIn)
        else:
            loggedIn = 'true'
            if currentGenre.users_id != login_session['users_id']:
                return "<script>function myFunction(){alert('Unauthorized');}</script><body onload='myFunction()''>"
            return render_template('deleteGenre.html', genre_id=genre_id, genre=currentGenre, loggedIn=loggedIn)


# Route to View Trailers by Genere Page /genres/#/Trailers/


@app.route('/genres/<int:genre_id>/trailers')
def showTrailers(genre_id):
    currentGenre = session.query(Genre).filter_by(id=genre_id).one()
    trailers = session.query(Trailer).filter_by(genre_id=genre_id).all()
    if 'username' not in login_session:
        loggedIn = 'false'
        return render_template('trailers.html', trailers=trailers, genre=currentGenre, loggedIn=loggedIn)
    else:
        loggedIn = 'true'
        return render_template('trailers.html', trailers=trailers, genre=currentGenre, loggedIn=loggedIn)
# TODO: Route to Add Trailer /library/#/Trailers/addTrailer


@app.route('/genres/<int:genre_id>/trailers/newtrailer', methods=['GET', 'POST'])
def newTrailer(genre_id):
    currentGenre = session.query(Genre).filter_by(id=genre_id).one()
    if request.method == 'POST':
        aNewTrailer = Trailer(
            title=request.form['title'],
            year=request.form['year'],
            rated=request.form['rated'],
            plot=request.form['plot'],
            director=request.form['director'],
            poster=request.form['poster'],
            trailer=request.form['trailer'],
            imdb_rating=request.form['imdb_rating'],
            imdb_id=request.form['imdb_id'],
            boxoffice=request.form['boxoffice'],
            genre_id=genre_id)
        session.add(aNewTrailer)
        currentGenre.num_trailers = currentGenre.num_trailers + 1
        session.add(currentGenre)
        session.commit()
        return redirect(url_for('showTrailers', genre_id=currentGenre.id))
    else:
        if 'username' not in login_session:
            loggedIn = 'false'
            return render_template('newTrailer.html', genre=currentGenre, loggedIn=loggedIn)
        else:
            loggedIn = 'true'
            return render_template('newTrailer.html', genre=currentGenre, loggedIn=loggedIn)

# TODO: Route to Show a Trailer /library/#/Trailers/#/editTrailer


@app.route('/genres/<int:genre_id>/trailers/<int:trailer_id>/showtrailer')
def showTrailer(genre_id, trailer_id):
    trailerToShow = session.query(Trailer).filter_by(
        id=trailer_id, genre_id=genre_id).one()
    if 'username' not in login_session:
        loggedIn = 'false'
        return render_template('showTrailer.html', trailer=trailerToShow, loggedIn=loggedIn)
    else:
        loggedIn = 'true'
        return render_template('showTrailer.html', trailer=trailerToShow, loggedIn=loggedIn)

# TODO: Route to Edit a Trailer /library/#/Trailers/#/editTrailer


@app.route('/genres/<int:genre_id>/trailers/<int:trailer_id>/edittrailer', methods=['GET', 'POST'])
def editTrailer(genre_id, trailer_id):
    trailerToEdit = session.query(Trailer).filter_by(
        id=trailer_id, genre_id=genre_id).one()
    if request.method == 'POST':
        trailerToEdit.title = request.form['title']
        trailerToEdit.year = request.form['year']
        trailerToEdit.rated = request.form['rated']
        trailerToEdit.plot = request.form['plot']
        trailerToEdit.director = request.form['director']
        trailerToEdit.poster = request.form['poster']
        trailerToEdit.trailer = request.form['trailer']
        trailerToEdit.imdb_rating = request.form['imdb_rating']
        trailerToEdit.imdb_id = request.form['imdb_id']
        trailerToEdit.boxoffice = request.form['boxoffice']
        session.add(trailerToEdit)
        session.commit()
        return redirect(url_for('showTrailers', genre_id=trailerToEdit.genre_id))
    else:
        if 'username' not in login_session:
            loggedIn = 'false'
            return render_template('editTrailer.html', genre_id=genre_id, trailer=trailerToEdit, loggedIn=loggedIn)
        else:
            loggedIn = 'true'
            if trailerToEdit.users_id != login_session['users_id']:
                return "<script>function myFunction(){alert('Unauthorized');}</script><body onload='myFunction()''>"
            return render_template('editTrailer.html', genre_id=genre_id, trailer=trailerToEdit, loggedIn=loggedIn)

# TODO: Route to Delete a Trailer /library/#/Content/#/deleteTrailer


@app.route('/genres/<int:genre_id>/trailers/<int:trailer_id>/deletetrailer', methods=['GET', 'POST'])
def deleteTrailer(genre_id, trailer_id):
    trailerToDelete = session.query(Trailer).filter_by(
        id=trailer_id, genre_id=genre_id).one()
    if request.method == 'POST':
        session.delete(trailerToDelete)
        currentGenre = session.query(Genre).filter_by(id=genre_id).one()
        currentGenre.num_trailers = currentGenre.num_trailers - 1
        session.add(currentGenre)
        session.commit()
        return redirect(url_for('showTrailers', genre_id=genre_id))
    else:
        if 'username' not in login_session:
            loggedIn = 'false'
            return render_template('deleteTrailer.html', genre_id=genre_id, trailer=trailerToDelete, loggedIn=loggedIn)
        else:
            loggedIn = 'true'
            if trailerToDelete.users_id != login_session['users_id']:
                return "<script>function myFunction(){alert('Unauthorized');}</script><body onload='myFunction()''>"
            return render_template('deleteTrailer.html', genre_id=genre_id, trailer=trailerToDelete, loggedIn=loggedIn)

# TODO: Route to Search Results Page /searchTrailers
# TODO: Instead of routing to different page render results within search page


@app.route('/searchtrailers')
def searchTrailers():
    if 'username' not in login_session:
        loggedIn = 'false'
        flash("You must login to search.")
        return render_template('login.html')
    else:
        loggedIn = 'true'
        return render_template('searchTrailers.html', loggedIn=loggedIn)

@app.route('/searchprocess', methods=['POST'])
def searchProcess():
    title = request.form['title']
    year = request.form['year']
    #API key for OMDB API:
    apiKey = 'a7ab3c0e'#insert API Key
    args = Namespace()
    if year:
        f = { 't' : title, 'y' : year, 'apiKey' : apiKey}
        argparser.add_argument("--q", help="Search term", default="%s %s trailer" % (title, year))
    else:
        f = { 't' : title, 'apiKey' : apiKey}
        argparser.add_argument("--q", help="Search term", default="%s trailer" % title)
    params = urllib.urlencode(f)
    print ('http://www.omdbapi.com/?%s' %
                     (params))
    r = requests.get('http://www.omdbapi.com/?%s' %
                     (params))
    print("request %r" % r)
    movieJSON = r.json()
    posterURL = movieJSON['Poster']
    argparser.add_argument("--max-results", help="Max results", default=1)
    args = argparser.parse_args()
    try:
      trailerID = trailersearch.youtube_search(args)
    except urllib2.HTTPError as e:
      return ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

    if title:
        movieJSON['Trailer'] = ('https://www.youtube.com/embed/%s' % trailerID)
        print(type(movieJSON))
        print(movieJSON)
        return jsonify(movieJSON)

    return jsonify({'error' : 'Unsuccesful Search!'})

# Accept incoming search request for a movie and return movie data


@app.route('/newsearchedtrailer', methods=['POST'])
def newSearchedTrailer():
    genre = request.form['Genre']
    if ',' in genre:
        genre = genre[:genre.index(',')]
    print(genre)

    exists = session.query(Genre.id).filter_by(name=genre).scalar() is not None
    print(exists)

    if exists:
        currentGenre = session.query(Genre).filter_by(name=genre).one()
        genre_id = currentGenre.id
        print(genre_id)
        aNewTrailer = Trailer(
            title=request.form['Title'],
            year=request.form['Year'],
            rated=request.form['Rated'],
            plot=request.form['Plot'],
            director=request.form['Director'],
            poster=request.form['Poster'],
            trailer=request.form['Trailer'],
            imdb_rating=request.form['imdbRating'],
            imdb_id=request.form['imdbID'],
            users_id=login_session['users_id'],
            genre_id=genre_id)
        session.add(aNewTrailer)
        currentGenre.num_trailers = currentGenre.num_trailers + 1
        session.add(currentGenre)
        session.commit()
        return jsonify({'success' : 'Movie Added!'})
    else:
        aNewGenre = Genre(
            name=genre,
            description=genre,
            num_trailers=0,
            image='/images/genre_background.jpg',
            users_id=login_session['users_id'])
        session.add(aNewGenre)
        session.commit()
        currentGenre = session.query(Genre).filter_by(name=genre).one()
        genre_id = currentGenre.id
        print(genre_id)
        aNewTrailer = Trailer(
            title=request.form['Title'],
            year=request.form['Year'],
            rated=request.form['Rated'],
            plot=request.form['Plot'],
            director=request.form['Director'],
            poster=request.form['Poster'],
            trailer=request.form['Trailer'],
            imdb_rating=request.form['imdbRating'],
            imdb_id=request.form['imdbID'],
            users_id=login_session['users_id'],
            genre_id=genre_id)
        session.add(aNewTrailer)
        currentGenre = session.query(Genre).filter_by(id=genre_id).one()
        currentGenre.num_trailers = currentGenre.num_trailers + 1
        session.add(currentGenre)
        session.commit()
        return jsonify({'success' : 'Movie Added!'})

    return jsonify({'error' : 'Failed!'})



# TODO: Route to API End Points /trailersJSON

@app.route('/genres/JSON')
def allGenresJSON():
    genres = session.query(Genre).all()
    return jsonify(Genre=[g.serialize for g in genres])

@app.route('/trailers/JSON')
def allTrailersJSON():
    trailers = session.query(Trailer).all()
    return jsonify(Trailer=[t.serialize for t in trailers])

@app.route('/users/JSON')
def allUsersJSON():
    users = session.query(Users).all()
    return jsonify(Trailer=[u.serialize for u in users])

@app.route('/genres/<int:genre_id>/trailers/JSON')
def trailersInGenreJSON(genre_id):
    currentGenre = session.query(Genre).filter_by(id=genre_id).one()
    trailers = session.query(Trailer).filter_by(genre_id=genre_id).all()
    return jsonify(Trailer=[t.serialize for t in trailers])

@app.route('/genres/<int:genre_id>/trailers/<int:trailer_id>/JSON')
def oneTrailerJSON(genre_id, trailer_id):
    trailerToShow = session.query(Trailer).filter_by(
        id=trailer_id, genre_id=genre_id).one()
    return jsonify(Trailer=[trailerToShow.serialize])

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run()
