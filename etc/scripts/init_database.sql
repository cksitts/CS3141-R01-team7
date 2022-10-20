-- set the password in the database to the one we are using
alter user 'root'@'localhost' identified by 'MRy_0VE9ARuv2zgcgaeepw';

-- setup the database
create database laundry_tracker_db;

-- setup the tables in the new database
use laundry_tracker_db;

create table MachineUser (	email varchar(64) primary key not null, 
							username char(64) not null, 
                            pass_hash char(64) not null, 
                            pass_salt char(10) not null );

create table Machine (	machine_id varchar(64) primary key not null, 
						location varchar(10) not null,
                        machine_type char(8) not null );

create table UsingMachine (	machine_id varchar(64) primary key not null, 
							email varchar(64) not null, 
							time_started time not null, 
							foreign key (machine_id) references Machine(machine_id),
                            foreign key (email) references MachineUser(email));