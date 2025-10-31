
-- Student Name: ROHIT PANDA
-- Student UOWID: 8943060
-- Clean up by dropping the table if it already exists
DROP TABLE IF EXISTS student_evaluations;

-- Part 1: Create the internal nested table with delimiter information
CREATE TABLE student_evaluations (
    student_id INT,
    evaluations ARRAY<STRUCT<subject: STRING, grade: INT>>
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
COLLECTION ITEMS TERMINATED BY ','
MAP KEYS TERMINATED BY ':'
STORED AS TEXTFILE;

-- Part 2: Load the sample data from the local text file
-- This is the correct and efficient method for bulk loading in Hive.
LOAD DATA LOCAL INPATH '/home/bigdata/Desktop/students.tbl' INTO TABLE student_evaluations;

-- Part 3: Select all data from the table to verify the load
SELECT * FROM student_evaluations;
