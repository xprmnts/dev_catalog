# Trailr App
# Author: XPRMNTS
# Python Version: 3
#------------------------------------------------------------------------------
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask import session as login_session
import random
import string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbsetup import Base, Genre, Trailer, User

# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenCredentials
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


@app.route('/')
@app.route('/discover')
def showLandingPage():
    trailers = session.query(Trailer).all()
    return render_template('index.html', trailers=trailers)
# TODO: Show assortment of movie posters
# TODO: Allow filtering by Genere
# TODO: Allow searching by Movie Name & Year

# Route to Genres Page /genres


@app.route('/genres')
def showGenres():
    genres = session.query(Genre).all()
    return render_template('genres.html', genres=genres, visclass="hide-links")

# Route to Add Genre Page /genre/addGenre


@app.route('/genres/newgenre', methods=['GET', 'POST'])
def newGenre():
    if request.method == 'POST':
        aNewGenre = Genre(
            name=request.form['name'],
            description=request.form['description'],
            num_trailers=0,
            image=request.form['image'])
        session.add(aNewGenre)
        session.commit()
        return redirect(url_for('showGenres'))
    else:
        return render_template('newGenre.html')

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
        return render_template('editGenre.html', genre_id=genre_id, genre=currentGenre)

# Route to Delete selected Genre Page /genres/#/deleteGenre (DELTE Method)
# TODO: Generate a popup instead of sending to new page


@app.route('/genres/<int:genre_id>/deletegenre', methods=['GET', 'POST'])
def deleteGenre(genre_id):
    currentGenre = session.query(Genre).filter_by(id=genre_id).one()
    if request.method == 'POST':
        session.delete(currentGenre)
        session.commit()
        return redirect(url_for('showGenres'))
    else:
        return render_template('deleteGenre.html', genre_id=genre_id, genre=currentGenre)


# Route to View Trailers by Genere Page /genres/#/Trailers/


@app.route('/genres/<int:genre_id>/trailers')
def showTrailers(genre_id):
    currentGenre = session.query(Genre).filter_by(id=genre_id).one()
    trailers = session.query(Trailer).filter_by(genre_id=genre_id).all()
    return render_template('trailers.html', trailers=trailers, genre=currentGenre)

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
        session.commit()
        return redirect(url_for('showTrailers', genre_id=currentGenre.id))
    else:
        return render_template('newTrailer.html', genre=currentGenre)

# TODO: Route to Show a Trailer /library/#/Trailers/#/editTrailer


@app.route('/genres/<int:genre_id>/trailers/<int:trailer_id>/showtrailer')
def showTrailer(genre_id, trailer_id):
    trailerToShow = session.query(Trailer).filter_by(
        id=trailer_id, genre_id=genre_id).one()
    return render_template('showTrailer.html', trailer=trailerToShow)

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
        return render_template('editTrailer.html', genre_id=genre_id, trailer=trailerToEdit)

# TODO: Route to Delete a Trailer /library/#/Content/#/deleteTrailer


@app.route('/genres/<int:genre_id>/trailers/<int:trailer_id>/deletetrailer', methods=['GET', 'POST'])
def deleteTrailer(genre_id, trailer_id):
    trailerToDelete = session.query(Trailer).filter_by(
        id=trailer_id, genre_id=genre_id).one()
    if request.method == 'POST':
        session.delete(trailerToDelete)
        session.commit()
        return redirect(url_for('showTrailers', genre_id=genre_id))
    else:
        return render_template('deleteTrailer.html', genre_id=genre_id, trailer=trailerToDelete)

# TODO: Route to Search Results Page /searchTrailers
# TODO: Instead of routing to different page render results within search page


@app.route('/searchtrailers')
def searchTrailers():
    return render_template('resultTrailers.html', trailers=trailers)

# TODO: Route to API End Points /trailersJSON

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
    login_session['credentials'] = credentials.access_token
    credentials = AccessTokenCredentials(login_session['credentials'], 'user-agent-value')
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    #output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session[
        'access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:

        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run()
