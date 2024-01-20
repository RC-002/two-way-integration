-- Create the "zenskar" database
CREATE DATABASE zenskar;

-- Connect to the "zenskar" database
\connect zenskar;

-- Create the "customer" table in the "zenskar" database
CREATE TABLE customer (
    ID character varying(32) PRIMARY KEY,
    name character varying(255) NOT NULL,
    email character varying(255) UNIQUE NOT NULL
);

-- Create the "id_mapping" table to map customer_id to stripe_id
CREATE TABLE id_mapping (
    id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id character varying(255) UNIQUE NOT NULL,
    stripe_id character varying(255) UNIQUE NULL,
    FOREIGN KEY (customer_id) REFERENCES customer(ID)
);