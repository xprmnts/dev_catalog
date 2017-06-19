

--
-- Data for Name: genre; Type: TABLE DATA; Schema: public; Owner: catalog_owner
--

INSERT INTO genre (id, name, description, num_trailers, image, users_id) VALUES (1, 'Comedy', 'Funny Movies', 0, 'genre_background.jpg', 1);
INSERT INTO genre (id, name, description, num_trailers, image, users_id) VALUES (2, 'Horror', 'Scary movies', 0, 'images/horror_background.jpg', 1);
INSERT INTO genre (id, name, description, num_trailers, image, users_id) VALUES (3, 'Sci-Fi', 'Science', 0, 'images/scifi_background.jpg', 1);



--
-- Data for Name: trailer; Type: TABLE DATA; Schema: public; Owner: catalog_owner
--

INSERT INTO trailer (id, title, year, rated, released, plot, director, poster, trailer, imdb_rating, imdb_id, boxoffice, genre_id, users_id) VALUES (1, 'The Witch', '2016', '14A', NULL, 'New England, 1630: William and Katherine lead a devout Christian life, homesteading on the edge of an impassible wilderness, with five children. When their newborn son mysteriously vanishes and their crops fail, the family begins to turn on one another. ''The Witch'' is a chilling portrait of a family unraveling within their own fears and anxieties, leaving them prey for an inescapable evil.', 'Robert Eggers', 'https://images-na.ssl-images-amazon.com/images/M/MV5BMTUyNzkwMzAxOF5BMl5BanBnXkFtZTgwMzc1OTk1NjE@._V1_SX300.jpg', 'https://www.youtube.com/embed/iQXmlf3Sefg', '6.8', 'tt4263482', '$19,239,494', 2, 1);
INSERT INTO trailer (id, title, year, rated, released, plot, director, poster, trailer, imdb_rating, imdb_id, boxoffice, genre_id, users_id) VALUES (2, 'Pineapple Express', '2008', 'R', NULL, 'A process server and his marijuana dealer wind up on the run from hitmen and a corrupt police officer after he witnesses his dealer''s boss murder a competitor while trying to serve papers on him.', 'David Gordon Green', 'https://images-na.ssl-images-amazon.com/images/M/MV5BMTY1MTE4NzAwM15BMl5BanBnXkFtZTcwNzg3Mjg2MQ@@._V1_SX300.jpg', 'https://www.youtube.com/embed/BWZt4v6b1hI', '7.0', 'tt0910936', '$101,600,00', 1, 1);
INSERT INTO trailer (id, title, year, rated, released, plot, director, poster, trailer, imdb_rating, imdb_id, boxoffice, genre_id, users_id) VALUES (3, 'The Martian', '2015', 'PG-13', NULL, 'Matt Damon, Jessica Chastain, Kristen Wiig, Jeff Daniels","Plot":"An astronaut becomes stranded on Mars after his team assume him dead, and must rely on his ingenuity to find a way to signal to Earth that he is alive.', 'Ridley Scott', 'https://images-na.ssl-images-amazon.com/images/M/MV5BMTc2MTQ3MDA1Nl5BMl5BanBnXkFtZTgwODA3OTI4NjE@._V1_SX300.jpg', 'https://www.youtube.com/embed/ej3ioOneTy8', '8.0', 'tt3659388', '$202,313,768', 3, 1);

INSERT INTO users (id, username, email) VALUES (1, 'Abhinay', 'abhinayk16@gmail.com');