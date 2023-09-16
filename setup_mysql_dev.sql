-- create or use a database
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- use the database
USE hbnb_dev_db;

-- create or use an existing user identified by a passowrd
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- the user hbnb_dev should have all priviledges on hbnb_dev_db
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- grant select priviledge on performance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';