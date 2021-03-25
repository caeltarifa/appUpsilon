--
-- PostgreSQL database dump
--

-- Dumped from database version 12.5 (Ubuntu 12.5-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.5 (Ubuntu 12.5-0ubuntu0.20.04.1)

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
-- Name: plan_vuelo_aeropuerto; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.plan_vuelo_aeropuerto (
    aeropuerto integer NOT NULL,
    nombre character varying(50) NOT NULL,
    iata character varying(5) NOT NULL,
    icao character varying(4) NOT NULL,
    longitude double precision NOT NULL,
    latitude double precision NOT NULL
);


ALTER TABLE public.plan_vuelo_aeropuerto OWNER TO postgres;

--
-- Name: plan_vuelo_aeropuerto_aeropuerto_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.plan_vuelo_aeropuerto_aeropuerto_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.plan_vuelo_aeropuerto_aeropuerto_seq OWNER TO postgres;

--
-- Name: plan_vuelo_aeropuerto_aeropuerto_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.plan_vuelo_aeropuerto_aeropuerto_seq OWNED BY public.plan_vuelo_aeropuerto.aeropuerto;


--
-- Name: plan_vuelo_aeropuerto aeropuerto; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_vuelo_aeropuerto ALTER COLUMN aeropuerto SET DEFAULT nextval('public.plan_vuelo_aeropuerto_aeropuerto_seq'::regclass);


--
-- Data for Name: plan_vuelo_aeropuerto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.plan_vuelo_aeropuerto (aeropuerto, nombre, iata, icao, longitude, latitude) FROM stdin;
2	Cobija Capitan Anibal Arab Airport	CIJ	SLCO	-68.782898	-11.0404
3	Cochabamba Jorge Wilstermann International Airport	CBB	SLCB	-66.177101	-17.421
4	Guayaramerin Airport	GYA	SLGY	-65.345802	-10.8216
5	La Paz El Alto International Airport	LPB	SLLP	-68.1922	-16.5133
7	Rurrenabaque Airport	RBQ	SLRQ	-67.498001	-14.4275
9	Santa Cruz El Trompillo Airport	SRZ	SLET	-63.171398	-17.811501
10	Sucre Alcantari International Airport	SRE	SLSU	-65.149612	-19.246836
12	Trinidad Teniente Jorge Henrich Arauz Airport	TDD	SLTR	-64.917999	-14.8187
13	Uyuni Joya Andina Airport	UYU	SLUY	-66.830002	-20.459999
8	Santa Cruz Viru Viru International Airport	VVI	SLVR	-63.1353	-17.644699
1	Aeropuerto de Chimore	CCA	SLHI	-65.141502	-16.98975
6	Riberalta Airport	RIB	SLRI	-66.116669	-11.0105
14	Reyes Airport	REY	SLRY	-65.149612	-13.3333333333
15	Pto. Suarez Tte. AV. Salvador Ogaya Airport	PSZ	SLPS	-57.8191625744	-18.9748221244
16	Yacuiba Airport	BYC	SLYA	-63.65166666666	-21.9608333
17	Monteagudo Apiaguaki Tumpa Airport	MHW	SLAG	-63.9627777777	-19.8238889
18	Apolo Airport	APB	SLAP	-68.4119444444	-14.7355556
19	Ascension de Guarayos Airport	ASC	SLAS	-63.15666666666	-15.9302778
20	Bermejo Airport	BJO	SLBJ	-64.3127777777	-22.7733333
21	Camiri Airport	CAM	SLCA	-63.5274999999	-20.0072222
22	Concepcion Airport	CEP	SLCP	-62.028611111	-16.1383333
23	San Jose de Chiquitos Airport	SJS	SLJE	-60.7430555555	-17.8308333
24	San Joaquin Airport	SJB	SLJO	-64.6744444444	-13.0658333
25	San Javier Airport	SJV	SLJV	-62.4702777777	-16.2708333
26	Magdalena Airport	MGD	SLMG	-64.0619444444	-13.2586111
27	Oruro Juan Mendoza Airport	ORU	SLOR	-67.075	-17.9555556
28	Potosi Cap. Nicolas Acosta Airport	POI	SLPO	-65.7233333333	19.5422222
29	San Ramon Airport	SRD	SLRA	-64.6038888888	-13.2638889
30	Robore Airport	RBO	SLRB	-59.7658333333	-18.3277778
31	Santa Ana del Yacuma Airport	SBL	SLSA	-65.4347222222	-13.7616667
32	San Borja Cap. German Quiroga Airport	SRJ	SLSB	-66.7386111111	-14.8577778
33	San Ignacio de Velasco Cap. AV. Juan Cochamanidis	SNG	SLSI	-60.96166666666	-16.3844444
34	San Ignacio de Moxos Airport	SNM	SLSM	-65.6338888888	-14.9655556
35	Santa Rosa del Yacuma	SRB	SLSR	-66.7869444444	-14.0744444
36	San Matias Airport	MQK	SLTI	-58.40194444444	-16.3391667
37	Vallegrande Cap. Av. Vidal Villagomez Airport	VAH	SLVG	-64.0994444444	-18.4825
38	Villamontes Tcnl. Rafael Pabon Airport	VLM	SLVM	-63.4066666666	-21.2541667
11	Tarija Airport	TJA	SLTJ	-64.701302	-21.5557
39	FIR BOLIVIA	SLLF	SLLF	0	0
\.


--
-- Name: plan_vuelo_aeropuerto_aeropuerto_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.plan_vuelo_aeropuerto_aeropuerto_seq', 39, true);


--
-- Name: plan_vuelo_aeropuerto plan_vuelo_aeropuerto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_vuelo_aeropuerto
    ADD CONSTRAINT plan_vuelo_aeropuerto_pkey PRIMARY KEY (aeropuerto);


--
-- PostgreSQL database dump complete
--

