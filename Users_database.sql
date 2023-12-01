CREATE DATABASE USERS;
USE USERS;

CREATE TABLE user_info (
userId INT PRIMARY KEY auto_increment,
username VARCHAR(255) NOT NULL, 
user_password VARCHAR(16) NOT NULL UNIQUE, 
user_email VARCHAR(100) NOT NULL CHECK( user_email Like '%@gmail.com')
);

ALTER TABLE user_info auto_increment = 100;

SELECT * FROM user_info;