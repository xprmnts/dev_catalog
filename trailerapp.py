# Trailr App
# Author: XPRMNTS
# Python Version: 3
#------------------------------------------------------------------------------
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbsetup import Base, Genre, Trailer, User
app = Flask(__name__)

engine = create_engine('postgresql://catalog_owner:pass1234@localhost/trailer_catalog')
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
    return render_template('genres.html', genres=genres)

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
        return render_template('editGenre.html', genre_id = genre_id, genre = currentGenre)

# Route to Delete selected Genre Page /genres/#/deleteGenre (DELTE Method)
# TODO: Generate a popup instead of sending to new page


@app.route('/genres/<int:genre_id>/deletegenre', methods=['GET','POST'])
def deleteGenre(genre_id):
    currentGenre = session.query(Genre).filter_by(id=genre_id).one()
    if request.method == 'POST':
        session.delete(currentGenre)
        session.commit()
        return redirect(url_for('showGenres'))
    else:
        return render_template('deleteGenre.html', genre_id = genre_id, genre = currentGenre)


# Route to View Trailers by Genere Page /genres/#/Trailers/


@app.route('/genres/<int:genre_id>/trailers')
def showTrailers(genre_id):
    currentGenre = session.query(Genre).filter_by(id=genre_id).one()
    trailers = session.query(Trailer).filter_by(genre_id=genre_id).all()
    return render_template('trailers.html', trailers = trailers, genre=currentGenre)

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
    trailerToShow = session.query(Trailer).filter_by(id=trailer_id, genre_id=genre_id).one()
    return render_template('showTrailer.html', trailer=trailerToShow)

# TODO: Route to Edit a Trailer /library/#/Trailers/#/editTrailer


@app.route('/genres/<int:genre_id>/trailers/<int:trailer_id>/edittrailer', methods=['GET','POST'])
def editTrailer(genre_id, trailer_id):
    trailerToEdit = session.query(Trailer).filter_by(id=trailer_id, genre_id=genre_id).one()
    if request.method == 'POST':
        trailerToEdit.title=request.form['title']
        trailerToEdit.year=request.form['year']
        trailerToEdit.rated=request.form['rated']
        trailerToEdit.plot=request.form['plot']
        trailerToEdit.director=request.form['director']
        trailerToEdit.poster=request.form['poster']
        trailerToEdit.trailer=request.form['trailer']
        trailerToEdit.imdb_rating=request.form['imdb_rating']
        trailerToEdit.imdb_id=request.form['imdb_id']
        trailerToEdit.boxoffice=request.form['boxoffice']
        session.add(trailerToEdit)
        session.commit()
        return redirect(url_for('showTrailers', genre_id=trailerToEdit.genre_id))
    else:
        return render_template('editTrailer.html', genre_id=genre_id, trailer=trailerToEdit)

# TODO: Route to Delete a Trailer /library/#/Content/#/deleteTrailer


@app.route('/genres/<int:genre_id>/trailers/<int:trailer_id>/deletetrailer', methods=['GET','POST'])
def deleteTrailer(genre_id, trailer_id):
    trailerToDelete = session.query(Trailer).filter_by(id=trailer_id, genre_id=genre_id).one()
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
    return render_template('login.html')

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run()
