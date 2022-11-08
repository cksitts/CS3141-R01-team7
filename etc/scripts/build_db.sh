#!/bin/bash
read -s -p "Enter database password: " pass

mysql -h localhost -u root -p$pass laundry_tracker_db < ./etc/scripts/init_database.sql
mysql --local-infile=1 -h localhost -u root -p$pass laundry_tracker_db < ./etc/scripts/load_machines.sql