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
    msg_time timestamp without time zone,
    bmessage bytea
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
165	user2	2b906c70201308fcfd27bedc2d89a374	2020-04-14 23:39:27
\.


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: rsbuhqmqigficf
--

COPY public.messages (msgid, from_usr, to_usr, message, msg_time, bmessage) FROM stdin;
83	user2	user2	\N	2020-04-14 16:55:51.15869	\\x67414141414142656c6a39333834654a7241727437795a6f504f6636507a594362562d362d3649377849493377593841416149645276444e6c753956305a4162796f4c4f41496372667179544c594b492d3056774275486b6f785474673772417178322d36554565546b59355570725972636f58394e4973387233727a6a4a7a78585838513163775145355145365934506e69674b65315550684a5650684444634f5a4c61506f426c516a797647546c5f6565645758733d
84	user2	user1	\N	2020-04-14 19:54:12.158692	\\x67414141414142656c6d6c454a6f6e36453151454530375763547343546a316b6f473869523166703152746b56495645767377723545656673316c52584c465242666745735a515f756d515479366f46776d475238497453734f535a7a5a4f7564334d634b433731704f5a39497671665a34457a304d6b5351796536374f44767546635058624c43716e78384d34745257535951562d525672424a5447376278626f646670725f5039514b304b764d4e7042304a7250447a697a646a5233392d555a6b753465326a4a326376646b6962755a727644706368705750425f4c744e616457694936435447626363595931424d5457477134334e4850427843625730705346347a3556424e4c6e476f656f6a594e6b4634457450763554376668345836795a6c4e595771756367684b6d75655f3176646a414c537077764f71706937383153785679343362547775742d35464f7a5645514f79326e6241625a47337441717947384f70624c76415041657761574a545a5f7a6b3d
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

SELECT pg_catalog.setval('public.auth_session_id_seq', 165, true);


--
-- Name: messages_msgid_seq; Type: SEQUENCE SET; Schema: public; Owner: rsbuhqmqigficf
--

SELECT pg_catalog.setval('public.messages_msgid_seq', 84, true);


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

