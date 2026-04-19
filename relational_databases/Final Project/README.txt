In this folder are the commands and queries i sued to complete the relational databases module
within the data engineering course.

part 1

-- create a user and a role in postgres cli
CREATE USER backup_operator;
CREATE ROLE backup;

-- grant privelidges to the role
GRANT CONNECT ON DATABASE tolldata TO backup;
GRANT SELECT ON ALL TABLES IN SCHEMA toll TO backup;

-- assign role to user
GRANT backup TO backup_operator;

-- backup tolldata
we did this within the postgres gui, i backuped the databse into a tar file.

part 2

-- restore database from sqldump file.(contains create database query). from terminal
mysql -u root -p < billing.sql

-- show tables within the database
mysql -u root -p -e "USE billing;SHOW TABLES;"

-- get table data size using a command within mysql cli
SELECT 
    table_name AS "Table",
    ROUND(data_length / 1024 / 1024, 2) AS "Data Size (MB)"
FROM information_schema.tables
WHERE table_schema = 'billing'
AND table_name = 'billdata';

-- baseline query to see run time 
SELECT * FROM billdata WHERE billedamount > 19999

-- create index to see if any performance gain
CREATE INDEX idx_bamount ON billdata(billedamount);

--next we reran the baseline query to see if it had improved.

-- show engines to see if myisam is supported
SHOW engines;

-- find engine of the billdata table
SELECT table_name, engine
    FROM information_schema.tables
    WHERE table_schema = 'billing'
    AND table_name = 'billdata';

part 3 

""" this part consists of using datasette to restore data, index and then view the creation.  """

--- after restoring the table billing i counted the rows within the table.
SELECT COUNT(*) FROM billing;

---i then created a view within datasette
CREATE VIEW basicbillingdetails AS 
SELECT customerid, month, billedamount
FROM billing;

--- next i ran a base query to see the runtime before indexing
SELECT strftime('%Y-%m-%d %H:%M:%f', 'now');
SELECT * FROM billing WHERE billedamount > 19929;
SELECT strftime('%Y-%m-%d %H:%M:%f', 'now');

--- i then created an index on billedamount
CREATE INDEX billingamount ON billing(billedamount);

--- i then reran the base query to see how much the runtime had improved
