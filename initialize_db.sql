-- Create the database if it does not exist
-- Create the library database
CREATE DATABASE IF NOT EXISTS library_db;

-- Switch to the library_db database
USE library_db;

-- Create the books table to store book details
CREATE TABLE IF NOT EXISTS books (
    book_name VARCHAR(255),
    book_id VARCHAR(255) PRIMARY KEY,
    author VARCHAR(255),
    status VARCHAR(255),        -- "Available" or "Issued"
    card_id VARCHAR(255)        -- Will be used for the Card ID of the Issuer (if applicable)
);
