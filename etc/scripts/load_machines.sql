-- set global local_infile = true;

-- all OS's => save the load_machines.txt file (add something, then delete it, then save)
-- MacOS => change "lines terminated by" to '\r'
-- Windows => change "lines terminated by" to '\r\n' (default)
-- Linux =>  change "lines terminated by" to '\n'

use laundry_tracker_db;

load data local infile './etc/scripts/load_machines.txt' into table Machine
lines terminated by '\n';

insert into MachineUser value ('person@mtu.edu', 'username', '147E Wads (Mafia/Utopia)', sha2('asdfasdfXXXXX', 256), 'XXXXX');
insert into Administrator value ('person@mtu.edu');

-- set global local_infile = false;

-- remove empty tuple
delete from Machine where machine_id = '';
