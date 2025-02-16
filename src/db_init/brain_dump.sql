--
-- PostgreSQL database dump
--

-- Dumped from database version 17.3
-- Dumped by pg_dump version 17.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: attention_maps; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.attention_maps (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    attention_map bytea NOT NULL,
    model_id uuid NOT NULL
);


ALTER TABLE public.attention_maps OWNER TO postgres;

--
-- Name: comment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comment (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    author character varying(255) NOT NULL,
    content character varying(255) NOT NULL,
    "timestamp" timestamp with time zone NOT NULL
);


ALTER TABLE public.comment OWNER TO postgres;

--
-- Name: ct_series; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ct_series (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    patient_id character varying(255) NOT NULL,
    upload_date timestamp with time zone NOT NULL,
    status character varying(50) NOT NULL,
    hemorrhage_percent uuid,
    projections uuid,
    comment uuid,
    attention_map uuid
);


ALTER TABLE public.ct_series OWNER TO postgres;

--
-- Name: model; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.model (
    model_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    model_path character varying(255) NOT NULL
);


ALTER TABLE public.model OWNER TO postgres;

--
-- Name: model_results; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.model_results (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    hemorrhage_percent uuid NOT NULL
);


ALTER TABLE public.model_results OWNER TO postgres;

--
-- Name: projections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projections (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    axial bytea NOT NULL,
    sagital bytea NOT NULL,
    coronal bytea NOT NULL
);


ALTER TABLE public.projections OWNER TO postgres;

--
-- Data for Name: attention_maps; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.attention_maps (id, attention_map, model_id) FROM stdin;
\.


--
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.comment (id, author, content, "timestamp") FROM stdin;
\.


--
-- Data for Name: ct_series; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ct_series (id, patient_id, upload_date, status, hemorrhage_percent, projections, comment, attention_map) FROM stdin;
58322e7d-f677-4b9c-a15f-dbdfd61afa42	12345	2025-02-15 20:38:30.051837+05	test	\N	\N	\N	\N
baa3a1f5-a8f3-49fc-9bc9-dc91291df9b7	12345	2025-02-15 20:41:57.567656+05	test	\N	\N	\N	\N
0927379e-197c-4bd9-ac72-df9b8cc5160b	12345	2025-02-15 20:45:36.590496+05	test	\N	\N	\N	\N
fe553527-8e19-40df-87f7-0b44761789c5	example_id	2025-02-16 19:33:20.589452+05	test_status	\N	\N	\N	\N
\.


--
-- Data for Name: model; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.model (model_id, model_path) FROM stdin;
\.


--
-- Data for Name: model_results; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.model_results (id, hemorrhage_percent) FROM stdin;
\.


--
-- Data for Name: projections; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projections (id, axial, sagital, coronal) FROM stdin;
\.


--
-- Name: attention_maps attention_maps_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attention_maps
    ADD CONSTRAINT attention_maps_pkey PRIMARY KEY (id);


--
-- Name: comment comment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_pkey PRIMARY KEY (id);


--
-- Name: ct_series ct_series_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ct_series
    ADD CONSTRAINT ct_series_pkey PRIMARY KEY (id);


--
-- Name: model model_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.model
    ADD CONSTRAINT model_pkey PRIMARY KEY (model_id);


--
-- Name: model_results model_results_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.model_results
    ADD CONSTRAINT model_results_pkey PRIMARY KEY (id);


--
-- Name: projections projections_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projections
    ADD CONSTRAINT projections_pkey PRIMARY KEY (id);


--
-- Name: attention_maps attention_maps_fk2; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attention_maps
    ADD CONSTRAINT attention_maps_fk2 FOREIGN KEY (model_id) REFERENCES public.model(model_id);


--
-- Name: ct_series ct_series_fk4; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ct_series
    ADD CONSTRAINT ct_series_fk4 FOREIGN KEY (hemorrhage_percent) REFERENCES public.model_results(id);


--
-- Name: ct_series ct_series_fk5; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ct_series
    ADD CONSTRAINT ct_series_fk5 FOREIGN KEY (projections) REFERENCES public.projections(id);


--
-- Name: ct_series ct_series_fk6; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ct_series
    ADD CONSTRAINT ct_series_fk6 FOREIGN KEY (comment) REFERENCES public.comment(id);


--
-- Name: ct_series ct_series_fk7; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ct_series
    ADD CONSTRAINT ct_series_fk7 FOREIGN KEY (attention_map) REFERENCES public.attention_maps(id);


--
-- PostgreSQL database dump complete
--

