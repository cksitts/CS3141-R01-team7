#!/bin/bash
read -p "Enter host domain: " host
read -p "Enter username: " user
read -s -p "Enter database password: " pass

mysql -h $host -u $user -p$pass laundry_tracker_db < ./etc/scripts/init_database.sql
mysql --local-infile=1 -h $host -u $user -p$pass laundry_tracker_db < ./etc/scripts/load_machines.sql