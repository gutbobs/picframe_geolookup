# picframe_geolookup
Adds geolookup data from android device history to photos for use in picframe

1st step is to download your Android Device location history from Google Takeout.
then, using the Records.json file store that in a MariaDB databasey. The DB is called geolookup. There are 2x tables, history and cached. the commands to build them are:

create table geolookup.history (id int auto_increment primary key, timestamp DATETIME, lat char(13), lon char(13));
create table geolookup.cached (id int auto_increment primary key, 
	lat char(13), 
	lon char(13), 
	state char(30),
	district char(30),
	town char(30),
	name char(30)	);
  
 The file import_to_db.py will iterate through Records.json and insert records into the DB
 
