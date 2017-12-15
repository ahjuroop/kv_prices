--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.10
-- Dumped by pg_dump version 9.5.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: kv_prices; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE kv_prices WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';


ALTER DATABASE kv_prices OWNER TO postgres;

\connect kv_prices

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

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
-- Name: object_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE object_info (
    id integer NOT NULL,
    object_id text,
    "timestamp" timestamp without time zone DEFAULT now(),
    address text,
    description_text text,
    description text,
    price text,
    pic_url text,
    obj_url text
);


ALTER TABLE object_info OWNER TO postgres;

--
-- Name: object_info_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE object_info_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE object_info_id_seq OWNER TO postgres;

--
-- Name: object_info_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE object_info_id_seq OWNED BY object_info.id;


--
-- Name: objects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE objects (
    id integer NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now(),
    x text,
    y text,
    object_id text
);


ALTER TABLE objects OWNER TO postgres;

--
-- Name: objects_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE objects_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE objects_id_seq OWNER TO postgres;

--
-- Name: objects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE objects_id_seq OWNED BY objects.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY object_info ALTER COLUMN id SET DEFAULT nextval('object_info_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY objects ALTER COLUMN id SET DEFAULT nextval('objects_id_seq'::regclass);


--
-- Name: object_info_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY object_info
    ADD CONSTRAINT object_info_pkey PRIMARY KEY (id);


--
-- Name: objects_object_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY objects
    ADD CONSTRAINT objects_object_id_key UNIQUE (object_id);


--
-- Name: objects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY objects
    ADD CONSTRAINT objects_pkey PRIMARY KEY (id);


--
-- Name: object_info_object_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY object_info
    ADD CONSTRAINT object_info_object_id_fkey FOREIGN KEY (object_id) REFERENCES objects(object_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: object_info; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE object_info FROM PUBLIC;
REVOKE ALL ON TABLE object_info FROM postgres;
GRANT ALL ON TABLE object_info TO postgres;
GRANT ALL ON TABLE object_info TO userhere;


--
-- Name: object_info_id_seq; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE object_info_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE object_info_id_seq FROM postgres;
GRANT ALL ON SEQUENCE object_info_id_seq TO postgres;
GRANT SELECT,USAGE ON SEQUENCE object_info_id_seq TO userhere;


--
-- Name: objects; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE objects FROM PUBLIC;
REVOKE ALL ON TABLE objects FROM postgres;
GRANT ALL ON TABLE objects TO postgres;
GRANT ALL ON TABLE objects TO userhere;


--
-- Name: objects_id_seq; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE objects_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE objects_id_seq FROM postgres;
GRANT ALL ON SEQUENCE objects_id_seq TO postgres;
GRANT SELECT,USAGE ON SEQUENCE objects_id_seq TO userhere;


--
-- PostgreSQL database dump complete
--

