#YOU MUST CREATE A DB FIRST sudo su - postgres, psql, CREATE DATABASE trailer_catalog
import sys

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

class Users(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True, autoincrement=True)
	username = Column(String(64), unique=True)
	email = Column(String(128), unique=True)

	@property
	def serialize(self):
		#Returns object data in easily serializable format
		return {
			'id' : self.id,
			'username'	:	self.username,
			'email'	:	self.email,
		}

# Create the Table Classes
class Genre(Base):
	__tablename__ = "genre"

	id = Column(Integer, primary_key = True, autoincrement=True)
	name = Column(String(64), nullable = False, unique=True)
	description = Column(String(512), nullable = True)
	num_trailers = Column(Integer, nullable = True)
	image = Column(String(128), nullable = True)
	users_id = Column(Integer, ForeignKey('users.id'))
	users = relationship(Users)

	@property
	def serialize(self):
		#Returns object data in easily serializable format
		return {
			'id' : self.id,
			'name'	:	self.name,
			'description'	:	self.description,
			'numTrailers'	:	self.num_trailers,
			'image'	:	self.image,
		}


	#TODO: Serailize for JSON

class Trailer(Base):
	__tablename__ = "trailer"

	id = Column(Integer, primary_key = True, autoincrement=True)
	title = Column(String(128), nullable = False)
	year = Column(String(4), nullable = True)
	rated = Column(String(16), nullable = True)
	released = Column(String(16), nullable = True)
	genre = Column(String(32), nullable = True)
	plot = Column(String(512), nullable = True)
	director = Column(String(64), nullable = True)
	poster = Column(String(256), nullable = True)
	trailer = Column(String(128), nullable = True)
	imdb_rating = Column(String(4), nullable = True)
	imdb_id = Column(String(16), nullable = True)
	boxoffice = Column(String(16), nullable = True)
	genre_id = Column(Integer, ForeignKey('genre.id'))
	genre = relationship(Genre)
	users_id = Column(Integer, ForeignKey('users.id'))
	users = relationship(Users)

	@property
	def serialize(self):
		#Returns object data in easily serializable format
		return {
			'id' : self.id,
			'title'	:	self.title,
			'year'	:	self.year,
			'rated'	:	self.rated,
			'released'	:	self.released,
			'genre'	:	self.genre,
			'plot'	:	self.plot,
			'director'	:	self.director,
			'poster'	:	self.poster,
			'trialer'	:	self.trailer,
			'imdbRating'	:	self.imdb_rating,
			'imdbId'	:	self.imdb_id,
			'boxoffice'	:	self.boxoffice,
		}

engine = create_engine('postgresql://catalog_owner:pass1234@localhost/trailer_catalog')
Base.metadata.create_all(engine)