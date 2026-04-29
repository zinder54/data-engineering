for the final project for the module linux command and shell scripting
i created the backup.sh file in this folder (linux_shell/final_project)
below are the commands i used after in the terminal.

--- made the file executable
chmod u+x backup.sh
    ls -l backup.sh
        -rwxr-xr-x 1 theia users 1413 Apr 28 16:01 backup.sh

--- i downloaded a zip containing files for the backup.sh file
wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-LX0117EN-SkillsNetwork/labs/Final%20Project/important-documents.zip

--- unzip the archive files - without restoring original modified date
unzip -DDo important-documents.zip

--- created folder for the files
touch important-documents/*

--- testing the script
./backup.sh important-documents .

--- command to show if file has been created from the backup.sh script
ls -l
    total 24
    -rw-r--r-- 1 theia users 4422 Apr 28 16:10 backup-1777407014.tar.gz
    -rwxr-xr-x 1 theia users 1413 Apr 28 16:01 backup.sh
    drwxr-sr-x 2 theia users 4096 Apr 28 16:10 important-documents
    -rw-r--r-- 1 theia users 4995 Sep 28  2022 important-documents.zip

- i then used the below to copy the file to the bin folder
sudo cp ./backup.sh /usr/local/bin/
    ---then the below to show that the file exists within bin/
    ls -l /usr/local/bin/backup.sh
        -rwxr-xr-x 1 root root 1413 Apr 29 15:25 /usr/local/bin/backup.sh

--- i then created a cron job to run every minute
*/1 * * * * /usr/local/bin/backup.sh /home/project/important-documents /home/project
    ---below is used to start the cronjob as i was using a virtual environment 
    sudo service cron start

---once the above was tested i changed it to every 24 hours
    i used crontab -l to see the crontab list 
theia@theia-zinderab:/home/project$ crontab -l
# Edit this file to introduce tasks to be run by cron.
# 
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
# 
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
# 
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
# 
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
# 
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
# 
# For more information see the manual pages of crontab(5) and cron(8)
# 
# m h  dom mon dow   command
0 0 * * * /usr/local/bin/backup.sh /home/project/important-documents /home/project