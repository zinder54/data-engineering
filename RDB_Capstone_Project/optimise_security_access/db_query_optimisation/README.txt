in this module of the RDM adminitration capstone project i work through optimising database and queries.
db security and access management. below are the steps i took within the module which is all self led.

All of the following tasks are to be performed on the MySQL CLI

--- created a a databse using:
CREATE DATABASE sales

---used th data base and used a sql file to populate with tables and rows
USE sales
    SOURCE load-data.sql

---got all rows where country id = 50 from tables
SELECT * FROM FactSales WHERE countryid = 50
    ---followed by explain query
    EXPLAIN SELECT * FROM FactSales WHERE countryid = 50

---created index on countryid
CREATE INDEX idx_country ON FactSales(countryid);
    ---then viewed the index
    SHOW INDEX FROM FactSales;

---i then used phpmyadmin to edit the data types to be more efficient i.e. int > tinyint etc.

--- lastly i used the below command to optimise the tables
OPTIMIZE TABLE DimDate;