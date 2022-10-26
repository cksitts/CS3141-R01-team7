-- setup the database
create database if not exists laundry_tracker_db;

-- setup the tables in the new database
use laundry_tracker_db;

set foreign_key_checks = 0;
drop table if exists MachineUser;
drop table if exists UsingMachine;
drop table if exists Machine;
set foreign_key_checks = 1;

create table MachineUser (	email varchar(64) primary key not null, 
							username varchar(64) unique not null, 
                            pass_hash char(64) not null, 
                            pass_salt char(16) not null );

create table Machine (	machine_id char(10) primary key not null, 
						location varchar(32) not null,
                        machine_type char(8) not null );

create table UsingMachine (	machine_id char(10) primary key not null, 
							email varchar(64) not null,
							username varchar(64) not null, 
							time_started time not null default 0, 
							foreign key (machine_id) references Machine(machine_id),
							foreign key (email) references MachineUser(email),
                            foreign key (username) references MachineUser(username)	);