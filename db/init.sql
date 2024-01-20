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
