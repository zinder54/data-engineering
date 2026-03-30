"""
This file is for relational databse administration capstone project. When doing the data
engineering course on coursera there was a lot of carry over with this course.
with that i decided to complete this capstone project along with the data engineering
course/capstone to further my studies and gain more experience using the tools ive learned.
below you will find the code that i used within the project to complete the exercises/tasks.
the tools used were MySQL, Python, SQL, BashOperator.
"""

-- Create Database --
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