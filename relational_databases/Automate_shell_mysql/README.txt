in this folder is the shell script (sqlbackup.sh) i created to automate a sqldump back up for a database that 
i created using the mysql cli terminal using the CREATE Database command.

using the terminal i used this command to give myself the user executable permission.
sudo chmod u+x+r sqlbackup.sh

i then created a cron job to schedule the task to run every two minutes.
*/2 * * * * /home/project/sqlbackup.sh > /home/project/backup.log

then used the following command to start the cron job
sudo service cron start

the following command will stop the cron job
sudo service cron stop

the following command will run the task every mondau at 12am
0 0 * * 1 /home/project/sqlbackup.sh > /home/project/backup.

and the following would run it at 6 am everyday.
0 6 * * * /home/project/sqlbackup.sh > /home/project/backup.