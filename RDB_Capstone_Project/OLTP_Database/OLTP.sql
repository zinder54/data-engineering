-- below are the command used within the CLI for mysql
-- when we created the table we had a csv file which we imported into the table to query.
-- and create the data dump file to back up the table

CREATE DATABASE sales;

-- Create sales_data table --
CREATE TABLE sales_data (
	product_id int NOT NULL,
    customer_id int NOT NULL,
    price int NOT NULL,
    quantity int NOT NULL,
    timestamp datetime NOT NULL
);

-- Show tables in DB -- 
SHOW TABLES -- Inputted in phpadmin, within MySQL

-- Record Count
SELECT COUNT(*) FROM `sales_data`;

-- Create index on timestamp column
CREATE INDEX ts ON sales_data (timestamp);

-- List indexes within sales_data
SHOW INDEX FROM sales_data;

-- Created a file for exporting all rows into a sql file
./datadump.sh --this is the file.