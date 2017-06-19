from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem, User

engine = create_engine('sqlite:///restaurantmenuwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = Users(username = "Abhinay", email = "abhinayk16@gmail.com")
session.add(User1)
session.commit()

# Add Three Genres

Genre1 = Genre(name = "Comedy",
description = "Funny Movies",
num_trailers = 1,
image = "images/genre_background.jpg",
users_id = 1)
session.add(Genre1)
session.commit()

Genre2 = Genre(name = "Horror",
description = "Scary Movies",
num_trailers = 1,
image = "images/horror_background.jpg",
users_id = 1)
session.add(Genre2)
session.commit()

Genre3 = Genre(name = "Sci-Fi",
description = "Sciency Movies",
num_trailers = 1,
image = "images/scifi_background.jpg",
users_id = 1)
session.add(Genre3)
session.commit()

Trailer1 = Trailer(title = 'The Witch',
       year = '2016',
       rated = '14A',
       released = NULL,
       plot = 'New England, 1630: William and Katherine lead a devout Christian life, homesteading on the edge of an impassible wilderness, with five children. When their newborn son mysteriously vanishes and their crops fail, the family begins to turn on one another. ''The Witch'' is a chilling portrait of a family unraveling within their own fears and anxieties, leaving them prey for an inescapable evil.',
       director = 'Robert Eggers',
       poster = 'https://images-na.ssl-images-amazon.com/images/M/MV5BMTUyNzkwMzAxOF5BMl5BanBnXkFtZTgwMzc1OTk1NjE@._V1_SX300.jpg',
       trailer = 'https://www.youtube.com/embed/iQXmlf3Sefg',
       imdb_rating = '6.8',
       imdb_id = 'tt4263482',
       boxoffice = '$19,239,494',
       genre_id = 1,
       users_id = 1)
session.add(Trailer1)
session.commit()


Trailer2 = Trailer(title = 'Pineapple Express',
       year = '2008',
       rated = 'R',
       released = NULL,
       plot = 'A process server and his marijuana dealer wind up on the run from hitmen and a corrupt police officer after he witnesses his dealer''s boss murder a competitor while trying to serve papers on him.', 'David Gordon Green', 'https://images-na.ssl-images-amazon.com/images/M/MV5BMTY1MTE4NzAwM15BMl5BanBnXkFtZTcwNzg3Mjg2MQ@@._V1_SX300.jpg',
       director = 'David Gordon Green',
       poster = 'https://images-na.ssl-images-amazon.com/images/M/MV5BMTY1MTE4NzAwM15BMl5BanBnXkFtZTcwNzg3Mjg2MQ@@._V1_SX300.jpg',
       trailer = 'https://www.youtube.com/embed/iQXmlf3Sefg',
       imdb_rating = '7.0',
       imdb_id = 'tt0910936',
       boxoffice = '$101,600,000',
       genre_id = 1,
       users_id = 1)
session.add(Trailer2)
session.commit()

Trailer3 = Trailer(title = 'The Martian',
       year = '2015',
       rated = 'PG-13',
       released = NULL,
       plot = 'Matt Damon, Jessica Chastain, Kristen Wiig, Jeff Daniels","Plot":"An astronaut becomes stranded on Mars after his team assume him dead, and must rely on his ingenuity to find a way to signal to Earth that he is alive.',
       director = 'Ridley Scott',
       poster = 'https://images-na.ssl-images-amazon.com/images/M/MV5BMTc2MTQ3MDA1Nl5BMl5BanBnXkFtZTgwODA3OTI4NjE@._V1_SX300.jpg',
       trailer = 'https://www.youtube.com/embed/ej3ioOneTy8',
       imdb_rating = '8.0',
       imdb_id = 'tt3659388',
       boxoffice = '$202,313,768',
       genre_id = 3,
       users_id = 1)
session.add(Trailer3)
session.commit()

print "added trailer items!"