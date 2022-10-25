set global local_infile = true;

load data local infile './etc/scripts/load_machines.txt' into table Machine;

set global local_infile = false;
