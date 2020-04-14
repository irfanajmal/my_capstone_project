--
-- PostgreSQL database dump
--

-- Dumped from database version 12.2 (Ubuntu 12.2-2.pgdg16.04+1)
-- Dumped by pg_dump version 12.2 (Ubuntu 12.2-2.pgdg18.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_session; Type: TABLE; Schema: public; Owner: rsbuhqmqigficf
--

CREATE TABLE public.auth_session (
    id integer NOT NULL,
    username character varying(50) DEFAULT NULL::character varying,
    session_id character varying(2050) DEFAULT NULL::character varying,
    expiry timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.auth_session OWNER TO rsbuhqmqigficf;

--
-- Name: auth_session_id_seq; Type: SEQUENCE; Schema: public; Owner: rsbuhqmqigficf
--

CREATE SEQUENCE public.auth_session_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_session_id_seq OWNER TO rsbuhqmqigficf;

--
-- Name: auth_session_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rsbuhqmqigficf
--

ALTER SEQUENCE public.auth_session_id_seq OWNED BY public.auth_session.id;


--
-- Name: messages; Type: TABLE; Schema: public; Owner: rsbuhqmqigficf
--

CREATE TABLE public.messages (
    msgid integer NOT NULL,
    from_usr character varying(50) DEFAULT NULL::character varying,
    to_usr character varying(50) DEFAULT NULL::character varying,
    message character varying(2050) DEFAULT NULL::character varying,
    msg_time timestamp without time zone
);


ALTER TABLE public.messages OWNER TO rsbuhqmqigficf;

--
-- Name: messages_msgid_seq; Type: SEQUENCE; Schema: public; Owner: rsbuhqmqigficf
--

CREATE SEQUENCE public.messages_msgid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.messages_msgid_seq OWNER TO rsbuhqmqigficf;

--
-- Name: messages_msgid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rsbuhqmqigficf
--

ALTER SEQUENCE public.messages_msgid_seq OWNED BY public.messages.msgid;


--
-- Name: users; Type: TABLE; Schema: public; Owner: rsbuhqmqigficf
--

CREATE TABLE public.users (
    id integer NOT NULL,
    uname character varying(50) DEFAULT NULL::character varying,
    email character varying(50) DEFAULT NULL::character varying,
    pword character varying(2050) DEFAULT NULL::character varying,
    date_added timestamp without time zone,
    pvtkey character varying,
    pubkeys character varying
);


ALTER TABLE public.users OWNER TO rsbuhqmqigficf;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: rsbuhqmqigficf
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO rsbuhqmqigficf;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rsbuhqmqigficf
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: auth_session id; Type: DEFAULT; Schema: public; Owner: rsbuhqmqigficf
--

ALTER TABLE ONLY public.auth_session ALTER COLUMN id SET DEFAULT nextval('public.auth_session_id_seq'::regclass);


--
-- Name: messages msgid; Type: DEFAULT; Schema: public; Owner: rsbuhqmqigficf
--

ALTER TABLE ONLY public.messages ALTER COLUMN msgid SET DEFAULT nextval('public.messages_msgid_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: rsbuhqmqigficf
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: auth_session; Type: TABLE DATA; Schema: public; Owner: rsbuhqmqigficf
--

COPY public.auth_session (id, username, session_id, expiry) FROM stdin;
133	user1	29fe66b843b778e83de045b0d56448fd	2020-04-13 12:29:44
\.


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: rsbuhqmqigficf
--

COPY public.messages (msgid, from_usr, to_usr, message, msg_time) FROM stdin;
64	user1	user2	Tough times never last but tough people do.	2020-04-12 15:56:59.158673
65	user1	user2	😜	2020-04-12 15:57:18.158673
66	user2	user1	Yesterday you said tomorrow. Just do it.	2020-04-12 15:58:13.158673
67	user2	user1	Die with memories, not dreams.	2020-04-12 15:58:41.158673
68	user2	user1	<strong>Hell0</strong>	2020-04-12 15:59:20.158673
69	user2	user2	‘ or 1=1;–.\r\n\r\n	2020-04-12 19:48:31.158674
70	user2	user2	select * from notes nt where nt.subject = ‘ ‘ or 1=1;–	2020-04-12 19:49:08.158674
71	user1	User1	test 123	2020-04-13 12:19:34.15868
72	user1	User1	test2	2020-04-13 12:20:54.15868
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: rsbuhqmqigficf
--

COPY public.users (id, uname, email, pword, date_added, pvtkey, pubkeys) FROM stdin;
38	user1	\N	$argon2id$v=19$m=32768,t=16,p=2$jpG0Vj4KOBuZIebQn2LWVA$t/4IKVYzonw1B9978FMGzXqg69uRX1x7UBHW3c15VQ8	2020-04-05 09:04:02.158608	\N	\N
39	user2	\N	$argon2id$v=19$m=32768,t=16,p=2$LrTdys8t9GQHHkoqBg2f6A$N5jOx0rw8fK90IHfgMnmDYjia99ybwpPvaHZuCezAmA	2020-04-05 09:42:15.158608	\N	\N
40	user3	\N	$argon2id$v=19$m=32768,t=16,p=2$xw7TX6jwEe30IXh9cQ+vgQ$U6jHfbCgtaf8Bf9rluBAQYc0cY+wtBBztt9SMuV8yU4	2020-04-05 15:55:50.15861	\N	\N
41	test1	\N	$argon2id$v=19$m=32768,t=16,p=2$2/ME5spm1v4IGFCFod8trQ$rrKftSH3OR82OD13OfsmNSasXPe4NIawsRsUcid+JTg	2020-04-05 15:58:41.15861	\N	\N
73	user4	\N	$argon2id$v=19$m=32768,t=16,p=2$pN4Nf+8uJL/OpkjXL3iGLg$rO1R0+2VPX0zmJ7tOnIhl44gPJgAkvMM0HLJA860vEE	2020-04-12 12:57:17.158672	\N	\N
\.


--
-- Name: auth_session_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rsbuhqmqigficf
--

SELECT pg_catalog.setval('public.auth_session_id_seq', 133, true);


--
-- Name: messages_msgid_seq; Type: SEQUENCE SET; Schema: public; Owner: rsbuhqmqigficf
--

SELECT pg_catalog.setval('public.messages_msgid_seq', 72, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rsbuhqmqigficf
--

SELECT pg_catalog.setval('public.users_id_seq', 73, true);


--
-- Name: auth_session auth_session_pkey; Type: CONSTRAINT; Schema: public; Owner: rsbuhqmqigficf
--

ALTER TABLE ONLY public.auth_session
    ADD CONSTRAINT auth_session_pkey PRIMARY KEY (id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: rsbuhqmqigficf
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (msgid);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: rsbuhqmqigficf
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: LANGUAGE plpgsql; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON LANGUAGE plpgsql TO rsbuhqmqigficf;


--
-- PostgreSQL database dump complete
--

