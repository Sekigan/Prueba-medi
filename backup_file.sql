--
-- PostgreSQL database dump
--

\restrict Y9OZWrETvsmQZd3Q17TJQZlYM2S6DLImJKrNLNXX1Fyd9FSR9UsE8CO1s6BXfsj

-- Dumped from database version 15.17 (Debian 15.17-1.pgdg13+1)
-- Dumped by pg_dump version 15.17 (Debian 15.17-1.pgdg13+1)

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
-- Name: customers; Type: TABLE; Schema: public; Owner: medi
--

CREATE TABLE public.customers (
    id integer NOT NULL,
    name character varying,
    email character varying,
    city character varying
);


ALTER TABLE public.customers OWNER TO medi;

--
-- Name: customers_id_seq; Type: SEQUENCE; Schema: public; Owner: medi
--

CREATE SEQUENCE public.customers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.customers_id_seq OWNER TO medi;

--
-- Name: customers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: medi
--

ALTER SEQUENCE public.customers_id_seq OWNED BY public.customers.id;


--
-- Name: inventory_movements; Type: TABLE; Schema: public; Owner: medi
--

CREATE TABLE public.inventory_movements (
    movement_id integer NOT NULL,
    product_id integer NOT NULL,
    movement_type character varying(20) NOT NULL,
    quantity integer NOT NULL,
    previous_stock integer NOT NULL,
    new_stock integer NOT NULL,
    reference_id integer,
    movement_date timestamp without time zone,
    notes text
);


ALTER TABLE public.inventory_movements OWNER TO medi;

--
-- Name: inventory_movements_movement_id_seq; Type: SEQUENCE; Schema: public; Owner: medi
--

CREATE SEQUENCE public.inventory_movements_movement_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.inventory_movements_movement_id_seq OWNER TO medi;

--
-- Name: inventory_movements_movement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: medi
--

ALTER SEQUENCE public.inventory_movements_movement_id_seq OWNED BY public.inventory_movements.movement_id;


--
-- Name: order_items; Type: TABLE; Schema: public; Owner: medi
--

CREATE TABLE public.order_items (
    item_id integer NOT NULL,
    order_id integer NOT NULL,
    product_id integer NOT NULL,
    quantity integer NOT NULL,
    unit_price numeric(10,2) NOT NULL
);


ALTER TABLE public.order_items OWNER TO medi;

--
-- Name: order_items_item_id_seq; Type: SEQUENCE; Schema: public; Owner: medi
--

CREATE SEQUENCE public.order_items_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.order_items_item_id_seq OWNER TO medi;

--
-- Name: order_items_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: medi
--

ALTER SEQUENCE public.order_items_item_id_seq OWNED BY public.order_items.item_id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: medi
--

CREATE TABLE public.orders (
    order_id integer NOT NULL,
    customer_id integer NOT NULL,
    order_date timestamp without time zone,
    status character varying(25),
    total numeric(10,2)
);


ALTER TABLE public.orders OWNER TO medi;

--
-- Name: orders_order_id_seq; Type: SEQUENCE; Schema: public; Owner: medi
--

CREATE SEQUENCE public.orders_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_order_id_seq OWNER TO medi;

--
-- Name: orders_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: medi
--

ALTER SEQUENCE public.orders_order_id_seq OWNED BY public.orders.order_id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: medi
--

CREATE TABLE public.products (
    product_id integer NOT NULL,
    name character varying NOT NULL,
    product_code integer NOT NULL,
    stock integer,
    category character varying(50),
    price numeric(10,2) NOT NULL
);


ALTER TABLE public.products OWNER TO medi;

--
-- Name: products_product_id_seq; Type: SEQUENCE; Schema: public; Owner: medi
--

CREATE SEQUENCE public.products_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.products_product_id_seq OWNER TO medi;

--
-- Name: products_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: medi
--

ALTER SEQUENCE public.products_product_id_seq OWNED BY public.products.product_id;


--
-- Name: customers id; Type: DEFAULT; Schema: public; Owner: medi
--

ALTER TABLE ONLY public.customers ALTER COLUMN id SET DEFAULT nextval('public.customers_id_seq'::regclass);


--
-- Name: inventory_movements movement_id; Type: DEFAULT; Schema: public; Owner: medi
--

ALTER TABLE ONLY public.inventory_movements ALTER COLUMN movement_id SET DEFAULT nextval('public.inventory_movements_movement_id_seq'::regclass);


--
-- Name: order_items item_id; Type: DEFAULT; Schema: public; Owner: medi
--

ALTER TABLE ONLY public.order_items ALTER COLUMN item_id SET DEFAULT nextval('public.order_items_item_id_seq'::regclass);


--
-- Name: orders order_id; Type: DEFAULT; Schema: public; Owner: medi
--

ALTER TABLE ONLY public.orders ALTER COLUMN order_id SET DEFAULT nextval('public.orders_order_id_seq'::regclass);


--
-- Name: products product_id; Type: DEFAULT; Schema: public; Owner: medi
--

ALTER TABLE ONLY public.products ALTER COLUMN product_id SET DEFAULT nextval('public.products_product_id_seq'::regclass);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: medi
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (id);


--
-- Name: inventory_movements inventory_movements_pkey; Type: CONSTRAINT; Schema: public; Owner: medi
--

ALTER TABLE ONLY public.inventory_movements
    ADD CONSTRAINT inventory_movements_pkey PRIMARY KEY (movement_id);


--
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: medi
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (item_id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: medi
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: medi
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_id);


--
-- Name: ix_customers_city; Type: INDEX; Schema: public; Owner: medi
--

CREATE INDEX ix_customers_city ON public.customers USING btree (city);


--
-- Name: ix_customers_email; Type: INDEX; Schema: public; Owner: medi
--

CREATE UNIQUE INDEX ix_customers_email ON public.customers USING btree (email);


--
-- Name: ix_customers_id; Type: INDEX; Schema: public; Owner: medi
--

CREATE INDEX ix_customers_id ON public.customers USING btree (id);


--
-- Name: ix_customers_name; Type: INDEX; Schema: public; Owner: medi
--

CREATE INDEX ix_customers_name ON public.customers USING btree (name);


--
-- Name: ix_inventory_movements_movement_id; Type: INDEX; Schema: public; Owner: medi
--

CREATE INDEX ix_inventory_movements_movement_id ON public.inventory_movements USING btree (movement_id);


--
-- Name: ix_order_items_item_id; Type: INDEX; Schema: public; Owner: medi
--

CREATE INDEX ix_order_items_item_id ON public.order_items USING btree (item_id);


--
-- Name: ix_orders_order_id; Type: INDEX; Schema: public; Owner: medi
--

CREATE INDEX ix_orders_order_id ON public.orders USING btree (order_id);


--
-- Name: ix_products_category; Type: INDEX; Schema: public; Owner: medi
--

CREATE INDEX ix_products_category ON public.products USING btree (category);


--
-- Name: ix_products_name; Type: INDEX; Schema: public; Owner: medi
--

CREATE INDEX ix_products_name ON public.products USING btree (name);


--
-- Name: ix_products_product_code; Type: INDEX; Schema: public; Owner: medi
--

CREATE UNIQUE INDEX ix_products_product_code ON public.products USING btree (product_code);


--
-- Name: ix_products_product_id; Type: INDEX; Schema: public; Owner: medi
--

CREATE INDEX ix_products_product_id ON public.products USING btree (product_id);


--
-- Name: ix_products_stock; Type: INDEX; Schema: public; Owner: medi
--

CREATE INDEX ix_products_stock ON public.products USING btree (stock);


--
-- Name: inventory_movements inventory_movements_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: medi
--

ALTER TABLE ONLY public.inventory_movements
    ADD CONSTRAINT inventory_movements_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id);


--
-- Name: order_items order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: medi
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(order_id);


--
-- Name: order_items order_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: medi
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id);


--
-- Name: orders orders_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: medi
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- PostgreSQL database dump complete
--

\unrestrict Y9OZWrETvsmQZd3Q17TJQZlYM2S6DLImJKrNLNXX1Fyd9FSR9UsE8CO1s6BXfsj

