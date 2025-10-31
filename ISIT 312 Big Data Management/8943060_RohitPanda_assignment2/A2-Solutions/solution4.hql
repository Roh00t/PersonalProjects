-- ISIT312 Big Data Management - Assignment 2, Task 4
-- Student Name: ROHIT PANDA
-- Student UOWID: 8943060

-- Drop tables first to make the script rerunnable
DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS item;

-- Create the EXTERNAL table for authors.
-- Schema MUST match dbcreate.sql
CREATE EXTERNAL TABLE author (
    a_id        INT,
    a_fname     VARCHAR(20),
    a_lname     VARCHAR(20),
    a_mname     VARCHAR(20),
    a_dob       DATE,
    a_bio       VARCHAR(500)
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
LOCATION '/user/bigdata/assignment2task4/author/';

-- Create the EXTERNAL table for items.
-- Schema MUST match dbcreate.sql
CREATE EXTERNAL TABLE item (
    i_id        INT,
    i_title     VARCHAR(140),
    i_a_id      INT,
    i_pub_date  DATE,
    i_publisher VARCHAR(60),
    i_subject   VARCHAR(60),
    i_desc      VARCHAR(600),
    i_cost      DECIMAL(13,2),
    i_srp       DECIMAL(13,2),
    i_avail     DATE,
    i_isbn      CHAR(13),
    i_page      INT,
    i_dimensions VARCHAR(25),
    i_cover_type VARCHAR(10)
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
LOCATION '/user/bigdata/assignment2task4/item/';

-- Part 2: Verification Queries
SELECT 'Number of rows in author:', count(*) FROM author;
SELECT 'Number of rows in item:', count(*) FROM item;
SELECT * FROM author LIMIT 3;
SELECT * FROM item LIMIT 3;
SELECT 'Total rows in both tables:', (SELECT count(*) FROM author) + (SELECT count(*) FROM item);

