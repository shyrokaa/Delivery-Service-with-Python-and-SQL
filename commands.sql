CREATE SCHEMA ds;

INSERT INTO users (FirstName, LastName, Email, Phone, City, Street, SNumber,UPassword)
VALUES ('Mike', 'Bell', 'mbell@gmail.com', '0753765967', 'Iasi', 'Mihai Eminescu', '15','parola123');

INSERT INTO users (FirstName, LastName, Email, Phone, City, Street, SNumber,UPassword)
VALUES ('Sara', 'Jones', 'sarj@gmail.com', '0752525464', 'Iasi', 'Mihai Viteazu', '25','password33');

# TABLE CREATION

CREATE TABLE users( userID INT(4) NOT NULL AUTO_INCREMENT,userType int,FirstName varchar(100), LastName varchar(100), Email varchar(100), Phone varchar(20), UPassword varchar(100),PRIMARY KEY(userID)); 
SELECT * FROM users;

CREATE TABLE address( userID INT(4) NOT NULL AUTO_INCREMENT, 	City varchar(100), Street varchar(100), Number varchar(20),FOREIGN KEY (userID) REFERENCES users(userID)); 
SELECT * FROM address;

CREATE TABLE routes(routeID INT(4) NOT NULL AUTO_INCREMENT,startCity varchar(100), interCity1 varchar(100), interCity2 varchar(100), stopCity varchar(100),PRIMARY KEY(routeID));
SELECT * FROM routes;

CREATE TABLE drivers( driverID INT(4) NOT NULL AUTO_INCREMENT, routeID INT(4), space INT(4), usedSpace INT(4),FOREIGN KEY (routeID) REFERENCES routes(routeID),PRIMARY KEY(driverID));
SELECT * FROM drivers;

CREATE TABLE orders(orderID INT(4) NOT NULL AUTO_INCREMENT,userID INT(4), driverID int, weight int,FOREIGN KEY (userID) REFERENCES users(userID),FOREIGN KEY (driverID) REFERENCES drivers(driverID),PRIMARY KEY(orderID));
SELECT * FROM orders;


# RELATIONSHIPS BETWEEN TABLES

# ONE TO ONE   - > users (userID)   --- address(userID)

# ONE TO MANY  - > users (userID)   --- orders(userID) 
#			   - > driver(driverID) --- orders(driverID) 

# MANY TO MANY - > users(userID)    --- drivers(driverID)
# intermediary table = orders


# INSERTS FOR SOME EXISTING DATA

# users
INSERT INTO users (userID, userType, FirstName, LastName, Email, Phone, UPassword) VALUES (1 , 0 ,'Mike', 'Bell', 'mbell@gmail.com', '0753765967','parola123');
INSERT INTO users (userID, userType, FirstName, LastName, Email, Phone, UPassword) VALUES (2 , 0 ,'Sara', 'Jones', 'sarj@gmail.com', '0752525464','pass333');
INSERT INTO users (userType, FirstName, LastName, Email, Phone, UPassword) VALUES ( 0 ,'Mihai', 'Ionescu', 'mjohn@gmail.com', '0752533454','pass111');

SELECT * FROM users;

# address
INSERT INTO address(userID,City,Street,Number) VALUES ( 1 , 'Iasi', 'Mihai Eminescu', '15');
INSERT INTO address(userID,City,Street,Number) VALUES ( 2 , 'Iasi', 'Mihai Viteazu', '24');

SELECT * FROM address;



SELECT u.FirstName , u.LastName, u.Email, u.Phone, a.City, a.Street, a.Number, u.UPassword FROM users u, address a WHERE u.userID = a.userID;


# emergency wipe

drop table orders;
drop table drivers;
drop table routes;
drop table address;
drop table users;
