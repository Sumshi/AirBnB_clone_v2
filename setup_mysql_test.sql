-- create or use a test database database
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- use the database u just created
USE hbnb_test_db;

-- create or use an existing user identified by a passowrd
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- the user hbnb_test should have all priviledges on hbnb_test_db
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- grant select priviledge on performance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';