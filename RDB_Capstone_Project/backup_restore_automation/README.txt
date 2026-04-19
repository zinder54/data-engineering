in this module we automated back up and restore within mysql.
first we created the connection to mysql and opened the mysql cli
i then created a database:
CREATE DATABASE sales;

---i then used a .sql file to populate the databse with tables and data rows:
SOURCE database_create_load.sql

---then in a new terminal i used the below command to access and edit the configuration file of Cloud 
IDE interface with the relevant client information to establish connections automatically, 
without requiring manual entry of passwords.

sudo nano ~/.my.cnf

[client]
host = mysql
port = 3306
user = root
password = <Your MySQL Password>

---next i created an sh file to automate the back up restore of the sales database. this can be found
in the backup_restore_automation folder. the file is called backup_automation.sh
--- i also used the below command in terminal to make the file an executable

chmod +x backup_automation.sh
##sudo chmod u+x+r backup_automation.sh

--- next i opened crontab using the below command to schedule the process
crontab -e

---and used the below command to create the cron job to run every 3 minutes
*/3 * * * * /home/project/backup_automation.sh
^O followed by Enter - to write the file
^X to exit crontab

--- i then used the below comman to start the cron job
sudo service cron start

--- the beloew to check the file had been created in te directory
ls -l /home/theia/backups

--- and the below to stop the con job
sudo service cron stop

--- next i created another sh file to truncate the sales database
    this can be found in the truncate_tables.sh
    i then used 
        sudo chmod u+x+r backup_automation.sh to make the file executable
    then i used the below:
        bash truncate_tables.sh to run the file

--- after running the truncate file i checked the database table to see if the rows had been removed
 SELECT * FROM DimDate;

---next i unzipped the backup file using
gunzip /home/theia/backups/backup_sales_19-04-2026_15-39-01.gz

--- i used the below command to restore the sales database from the back up file
SOURCE /home/theia/backups/backup_sales_19-04-2026_15-39-01;

--- and finally i used the below to make sure the restore was succesful using mysql cli
 SELECT * FROM DimDate LIMIT 1O;



