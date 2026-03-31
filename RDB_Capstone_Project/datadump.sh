# this file is for the exporting of all rows from the MySQL database sales, table sales_data
# for the relational database administrator capstone project.

#!/bin/bash

DB_USER="root"
DB_NAME="sales"

mysqldump -u $DB_USER -p $DB_NAME sales_data > sales_data.sql 