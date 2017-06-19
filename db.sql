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
    image character varying(128)
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
    poster character varying(128),
    trailer character varying(128),
    imdb_rating character varying(4),
    imdb_id character varying(16),
    boxoffice character varying(16),
    genre_id integer
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
-- Name: user; Type: TABLE; Schema: public; Owner: catalog_owner; Tablespace: 
--

CREATE TABLE "user" (
    id integer NOT NULL,
    username character varying(64),
    email character varying(128)
);


ALTER TABLE public."user" OWNER TO catalog_owner;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: catalog_owner
--

CREATE SEQUENCE user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO catalog_owner;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: catalog_owner
--

ALTER SEQUENCE user_id_seq OWNED BY "user".id;


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

ALTER TABLE ONLY "user" ALTER COLUMN id SET DEFAULT nextval('user_id_seq'::regclass);


--
-- Data for Name: genre; Type: TABLE DATA; Schema: public; Owner: catalog_owner
--

COPY genre (id, name, description, num_trailers, image) FROM stdin;
2	Comedy	Funny Movies	0	genre_background.jpg
3	Horror	Scary movies	0	images/horror_background.jpg
4	Sci-Fi	Science	0	images/scifi_background.jpg
\.


--
-- Name: genre_id_seq; Type: SEQUENCE SET; Schema: public; Owner: catalog_owner
--

SELECT pg_catalog.setval('genre_id_seq', 4, true);


--
-- Data for Name: trailer; Type: TABLE DATA; Schema: public; Owner: catalog_owner
--

COPY trailer (id, title, year, rated, released, plot, director, poster, trailer, imdb_rating, imdb_id, boxoffice, genre_id) FROM stdin;
1	The Witch	2016	14A	\N	New England, 1630: William and Katherine lead a devout Christian life, homesteading on the edge of an impassible wilderness, with five children. When their newborn son mysteriously vanishes and their crops fail, the family begins to turn on one another. 'The Witch' is a chilling portrait of a family unraveling within their own fears and anxieties, leaving them prey for an inescapable evil.	Robert Eggers	https://images-na.ssl-images-amazon.com/images/M/MV5BMTUyNzkwMzAxOF5BMl5BanBnXkFtZTgwMzc1OTk1NjE@._V1_SX300.jpg	https://www.youtube.com/embed/iQXmlf3Sefg	6.8	tt4263482	$19,239,494	3
6	Pineapple Express	2008	R	\N	A process server and his marijuana dealer wind up on the run from hitmen and a corrupt police officer after he witnesses his dealer's boss murder a competitor while trying to serve papers on him.	David Gordon Green	https://images-na.ssl-images-amazon.com/images/M/MV5BMTY1MTE4NzAwM15BMl5BanBnXkFtZTcwNzg3Mjg2MQ@@._V1_SX300.jpg	https://www.youtube.com/embed/BWZt4v6b1hI	7.0	tt0910936	$101,600,00	2
7	The Martian	2015	PG-13	\N	Matt Damon, Jessica Chastain, Kristen Wiig, Jeff Daniels","Plot":"An astronaut becomes stranded on Mars after his team assume him dead, and must rely on his ingenuity to find a way to signal to Earth that he is alive.	Ridley Scott	https://images-na.ssl-images-amazon.com/images/M/MV5BMTc2MTQ3MDA1Nl5BMl5BanBnXkFtZTgwODA3OTI4NjE@._V1_SX300.jpg	https://www.youtube.com/embed/ej3ioOneTy8	8.0	tt3659388	$202,313,768	4
\.


--
-- Name: trailer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: catalog_owner
--

SELECT pg_catalog.setval('trailer_id_seq', 7, true);


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: catalog_owner
--

COPY "user" (id, username, email) FROM stdin;
\.


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: catalog_owner
--

SELECT pg_catalog.setval('user_id_seq', 1, false);


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
-- Name: user_email_key; Type: CONSTRAINT; Schema: public; Owner: catalog_owner; Tablespace: 
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user_pkey; Type: CONSTRAINT; Schema: public; Owner: catalog_owner; Tablespace: 
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user_username_key; Type: CONSTRAINT; Schema: public; Owner: catalog_owner; Tablespace: 
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: trailer_genre_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: catalog_owner
--

ALTER TABLE ONLY trailer
    ADD CONSTRAINT trailer_genre_id_fkey FOREIGN KEY (genre_id) REFERENCES genre(id);


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

