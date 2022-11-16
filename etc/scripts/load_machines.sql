-- set global local_infile = true;

-- all OS's => save the load_machines.txt file (add something, then delete it, then save)
-- MacOS => change "lines terminated by" to '\r'
-- Windows => change "lines terminated by" to '\r\n' (default)
-- Linux =>  change "lines terminated by" to '\n'

load data local infile './etc/scripts/load_machines.txt' into table Machine
lines terminated by '\r\n';

-- set global local_infile = false;

-- remove empty tuple
delete from Machine where machine_id = '';
