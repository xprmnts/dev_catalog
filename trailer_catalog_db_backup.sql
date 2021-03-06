--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: genre; Type: TABLE; Schema: public; Owner: catalog_owner; Tablespace: 
--

CREATE TABLE genre (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    description character varying(512),
    num_trailers integer,
    image character varying(128),
    users_id integer
);


ALTER TABLE public.genre OWNER TO catalog_owner;

--
-- Name: genre_id_seq; Type: SEQUENCE; Schema: public; Owner: catalog_owner
--

CREATE SEQUENCE genre_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.genre_id_seq OWNER TO catalog_owner;

--
-- Name: genre_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: catalog_owner
--

ALTER SEQUENCE genre_id_seq OWNED BY genre.id;


--
-- Name: trailer; Type: TABLE; Schema: public; Owner: catalog_owner; Tablespace: 
--

CREATE TABLE trailer (
    id integer NOT NULL,
    title character varying(128) NOT NULL,
    year character varying(4),
    rated character varying(16),
    released character varying(16),
    plot character varying(512),
    director character varying(64),
    poster character varying(256),
    trailer character varying(128),
    imdb_rating character varying(4),
    imdb_id character varying(16),
    boxoffice character varying(16),
    genre_id integer,
    users_id integer
);


ALTER TABLE public.trailer OWNER TO catalog_owner;

--
-- Name: trailer_id_seq; Type: SEQUENCE; Schema: public; Owner: catalog_owner
--

CREATE SEQUENCE trailer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trailer_id_seq OWNER TO catalog_owner;

--
-- Name: trailer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: catalog_owner
--

ALTER SEQUENCE trailer_id_seq OWNED BY trailer.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: catalog_owner; Tablespace: 
--

CREATE TABLE users (
    id integer NOT NULL,
    username character varying(64),
    email character varying(128)
);


ALTER TABLE public.users OWNER TO catalog_owner;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: catalog_owner
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO catalog_owner;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: catalog_owner
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: catalog_owner
--

ALTER TABLE ONLY genre ALTER COLUMN id SET DEFAULT nextval('genre_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: catalog_owner
--

ALTER TABLE ONLY trailer ALTER COLUMN id SET DEFAULT nextval('trailer_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: catalog_owner
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Data for Name: genre; Type: TABLE DATA; Schema: public; Owner: catalog_owner
--

COPY genre (id, name, description, num_trailers, image, users_id) FROM stdin;
3	Sci-Fi	Science	2	images/scifi_background.jpg	1
4	Documentaries	About IRL Things	2	images/documentaries_background.jpg	2
5	Action	Action	1	/images/genre_background.jpg	3
1	Comedy	Funny Movies	1	images/genre_background.jpg	1
2	Horror	Scary movies	3	images/horror_background.jpg	1
\.


--
-- Name: genre_id_seq; Type: SEQUENCE SET; Schema: public; Owner: catalog_owner
--

SELECT pg_catalog.setval('genre_id_seq', 5, true);


--
-- Data for Name: trailer; Type: TABLE DATA; Schema: public; Owner: catalog_owner
--

COPY trailer (id, title, year, rated, released, plot, director, poster, trailer, imdb_rating, imdb_id, boxoffice, genre_id, users_id) FROM stdin;
1	The Witch	2016	14A	\N	New England, 1630: William and Katherine lead a devout Christian life, homesteading on the edge of an impassible wilderness, with five children. When their newborn son mysteriously vanishes and their crops fail, the family begins to turn on one another. 'The Witch' is a chilling portrait of a family unraveling within their own fears and anxieties, leaving them prey for an inescapable evil.	Robert Eggers	https://images-na.ssl-images-amazon.com/images/M/MV5BMTUyNzkwMzAxOF5BMl5BanBnXkFtZTgwMzc1OTk1NjE@._V1_SX300.jpg	https://www.youtube.com/embed/iQXmlf3Sefg	6.8	tt4263482	$19,239,494	2	1
2	Pineapple Express	2008	R	\N	A process server and his marijuana dealer wind up on the run from hitmen and a corrupt police officer after he witnesses his dealer's boss murder a competitor while trying to serve papers on him.	David Gordon Green	https://images-na.ssl-images-amazon.com/images/M/MV5BMTY1MTE4NzAwM15BMl5BanBnXkFtZTcwNzg3Mjg2MQ@@._V1_SX300.jpg	https://www.youtube.com/embed/BWZt4v6b1hI	7.0	tt0910936	$101,600,00	1	1
3	The Martian	2015	PG-13	\N	Matt Damon, Jessica Chastain, Kristen Wiig, Jeff Daniels","Plot":"An astronaut becomes stranded on Mars after his team assume him dead, and must rely on his ingenuity to find a way to signal to Earth that he is alive.	Ridley Scott	https://images-na.ssl-images-amazon.com/images/M/MV5BMTc2MTQ3MDA1Nl5BMl5BanBnXkFtZTgwODA3OTI4NjE@._V1_SX300.jpg	https://www.youtube.com/embed/ej3ioOneTy8	8.0	tt3659388	$202,313,768	3	1
8	Aliens	1986	R	\N	The moon from Alien (1979) has been colonized, but contact is lost. This time, the rescue team has impressive firepower, but will it be enough?	James Cameron	https://images-na.ssl-images-amazon.com/images/M/MV5BYzVlMWViZGEtYjEyYy00YWZmLThmZGEtYmM4MDZlN2Q5MmRmXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg	https://www.youtube.com/embed/XKSQmYUaIyE	8.4	tt0090605	\N	5	3
9	Alien: Covenant	2017	R	\N	The crew of a colony ship, bound for a remote planet, discover an uncharted paradise with a threat beyond their imagination, and must attempt a harrowing escape.	Ridley Scott	https://images-na.ssl-images-amazon.com/images/M/MV5BNzI5MzM3MzkxNF5BMl5BanBnXkFtZTgwOTkyMjI4MTI@._V1_SX300.jpg	https://www.youtube.com/embed/u5KPP6lxRVg	6.8	tt2316204	\N	2	2
4	Helvetica	2007	G	\N	A documentary about typography, graphic design, and global visual culture.	Gary Hustwit	http://www.hustwit.com/wp-content/uploads/2014/01/store-helvetica-poster.jpg	https://www.youtube.com/embed/wkoX0pEwSCw	7.2	tt0847817	$	4	1
5	I Am Heath Ledger	2017	N/A	\N	Friends and family of the late actor Heath Ledger remember his life and career.	Adrian Buitenhuis	https://images-na.ssl-images-amazon.com/images/M/MV5BNDE1OTYyNzgwOV5BMl5BanBnXkFtZTgwMDM5MDY5MTI@._V1_SX300.jpg	https://www.youtube.com/embed/5PPTDsTnaPk	7.4	tt6739646	$	4	1
6	Inception	2010	PG-13	\N	A thief, who steals corporate secrets through use of dream-sharing technology, is given the inverse task of planting an idea into the mind of a CEO.	Christopher Nolan	https://images-na.ssl-images-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg	https://www.youtube.com/embed/YoHD9XEInc0	8.8	tt1375666	$292,568,851	3	1
7	Alien	1979	R	\N	After a space merchant vessel perceives an unknown transmission as a distress call, its landing on the source moon finds one of the crew attacked by a mysterious life-form, and they soon realize that its life cycle has merely begun.	Ridley Scott	https://images-na.ssl-images-amazon.com/images/M/MV5BNDNhN2IxZWItNGEwYS00ZDNhLThiM2UtODU3NWJlZjBkYjQxXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg	https://www.youtube.com/embed/LjLamj-b0I8?showinfo=0	8.5	tt0078748	\N	2	1
\.


--
-- Name: trailer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: catalog_owner
--

SELECT pg_catalog.setval('trailer_id_seq', 9, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: catalog_owner
--

COPY users (id, username, email) FROM stdin;
3	xprmnts3	test3@gmail.com
2	xprmnts2	test2@gmail.com
1	xprmnts1	test1@gmail.com
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: catalog_owner
--

SELECT pg_catalog.setval('users_id_seq', 3, true);


--
-- Name: genre_name_key; Type: CONSTRAINT; Schema: public; Owner: catalog_owner; Tablespace: 
--

ALTER TABLE ONLY genre
    ADD CONSTRAINT genre_name_key UNIQUE (name);


--
-- Name: genre_pkey; Type: CONSTRAINT; Schema: public; Owner: catalog_owner; Tablespace: 
--

ALTER TABLE ONLY genre
    ADD CONSTRAINT genre_pkey PRIMARY KEY (id);


--
-- Name: trailer_pkey; Type: CONSTRAINT; Schema: public; Owner: catalog_owner; Tablespace: 
--

ALTER TABLE ONLY trailer
    ADD CONSTRAINT trailer_pkey PRIMARY KEY (id);


--
-- Name: users_email_key; Type: CONSTRAINT; Schema: public; Owner: catalog_owner; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: catalog_owner; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_username_key; Type: CONSTRAINT; Schema: public; Owner: catalog_owner; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: genre_users_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: catalog_owner
--

ALTER TABLE ONLY genre
    ADD CONSTRAINT genre_users_id_fkey FOREIGN KEY (users_id) REFERENCES users(id);


--
-- Name: trailer_genre_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: catalog_owner
--

ALTER TABLE ONLY trailer
    ADD CONSTRAINT trailer_genre_id_fkey FOREIGN KEY (genre_id) REFERENCES genre(id);


--
-- Name: trailer_users_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: catalog_owner
--

ALTER TABLE ONLY trailer
    ADD CONSTRAINT trailer_users_id_fkey FOREIGN KEY (users_id) REFERENCES users(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

