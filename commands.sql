CREATE SCHEMA ds;

# TABLE CREATION

CREATE TABLE users( userID INT(4) NOT NULL AUTO_INCREMENT,userType int,FirstName varchar(100), LastName varchar(100), Email varchar(100), Phone varchar(20), UPassword varchar(100),PRIMARY KEY(userID)); 
SELECT * FROM users;

CREATE TABLE address( userID INT(4) NOT NULL AUTO_INCREMENT, City varchar(100), Street varchar(100), Number varchar(20),FOREIGN KEY (userID) REFERENCES users(userID)); 
SELECT * FROM address;

CREATE TABLE routes(routeID INT(4) NOT NULL AUTO_INCREMENT,startCity varchar(100), interCity1 varchar(100), interCity2 varchar(100), stopCity varchar(100),PRIMARY KEY(routeID));
SELECT * FROM routes;

CREATE TABLE drivers( driverID INT(4) NOT NULL AUTO_INCREMENT, routeID INT(4), space INT(4), usedSpace INT(4),FOREIGN KEY (routeID) REFERENCES routes(routeID),PRIMARY KEY(driverID));
SELECT * FROM drivers;

CREATE TABLE orders(orderID INT(4) NOT NULL AUTO_INCREMENT,userID INT(4), driverID INT(4),name varchar(100), weight INT(4), FOREIGN KEY (userID) REFERENCES users(userID),FOREIGN KEY (driverID) REFERENCES drivers(driverID),PRIMARY KEY(orderID));
SELECT * FROM orders;

CREATE TABLE destinations( orderID INT(4) NOT NULL AUTO_INCREMENT, 	City varchar(100), Street varchar(100), Number varchar(20),FOREIGN KEY (orderID) REFERENCES orders(orderID)); 
SELECT * FROM destinations;

# RELATIONSHIPS BETWEEN TABLES
# ONE TO ONE   - > users (userID)   ---  address(userID)

# ONE TO MANY  - > users (userID)   ---  orders(userID) 
#			   - > driver(driverID) ---  orders(driverID) 

# MANY TO MANY - > users(userID)    ---  drivers(driverID)
# intermediary table = orders

# INSERTS FOR SOME EXISTING DATA

# users
INSERT INTO users (userType, FirstName, LastName, Email, Phone, UPassword) VALUES ( 1 ,'Mike', 'Bell', 'mbell@gmail.com', '0753765967','parola123');
INSERT INTO users ( userType, FirstName, LastName, Email, Phone, UPassword) VALUES ( 0 ,'Sara', 'Jones', 'sarj@gmail.com', '0752525464','pass333');
INSERT INTO users ( userType, FirstName, LastName, Email, Phone, UPassword) VALUES ( 0 ,'Marius', 'Dumitru', 'dumm@gmail.com', '0762523464','pass111');
INSERT INTO users ( userType, FirstName, LastName, Email, Phone, UPassword) VALUES ( 0 ,'Ioana', 'Maciu', 'maciu@gmail.com', '0752525461','pass222');
INSERT INTO users ( userType, FirstName, LastName, Email, Phone, UPassword) VALUES ( 0 ,'Mircea', 'Mihai', 'mmirc@gmail.com', '0752525462','pass444');
INSERT INTO users ( userType, FirstName, LastName, Email, Phone, UPassword) VALUES ( 0 ,'Ion', 'Zapada', 'iamzapada@gmail.com', '0752525463','pass555');
SELECT * FROM users;

# address
INSERT INTO address(City,Street,Number) VALUES ('Iasi', 'Mihai Eminescu', '15');
INSERT INTO address(City,Street,Number) VALUES ('Iasi', 'Mihai Viteazu', '24');
INSERT INTO address(City,Street,Number) VALUES ('Roman', 'Stefan cel Mare', '1');
INSERT INTO address(City,Street,Number) VALUES ('Piatra-Neamt', 'Emiliei', '12');
INSERT INTO address(City,Street,Number) VALUES ('Vaslui', 'Croitoriei', '2');
INSERT INTO address(City,Street,Number) VALUES ('Bacau', 'Centru', '13');
SELECT * FROM address;

# routes
INSERT INTO routes(startCity, interCity1,interCity2,stopCity) VALUES ('Iasi','Roman','Piatra-Neamt','Bacau');
INSERT INTO routes(startCity, interCity1,interCity2,stopCity) VALUES ('Bacau','Piatra-Neamt','Roman','Iasi');
INSERT INTO routes(startCity, interCity1,interCity2,stopCity) VALUES ('Bacau','Piatra-Neamt','Targu Neamt','Pascani');
INSERT INTO routes(startCity, interCity1,interCity2,stopCity) VALUES ('Pascani','Targu Neamt','Piatra-Neamt','Bacau');
INSERT INTO routes(startCity, interCity1,interCity2,stopCity) VALUES ('Suceava','Vaslui','Pascani','Iasi');
INSERT INTO routes(startCity, interCity1,interCity2,stopCity) VALUES ('Iasi','Pascani','Vaslui','Suceava');
SELECT * FROM routes;

#drivers
INSERT INTO drivers(routeID,space,usedSpace) VALUES(1,500,0);
INSERT INTO drivers(routeID,space,usedSpace) VALUES(1,500,0);
INSERT INTO drivers(routeID,space,usedSpace) VALUES(2,450,0);
INSERT INTO drivers(routeID,space,usedSpace) VALUES(3,100,0);
INSERT INTO drivers(routeID,space,usedSpace) VALUES(4,300,0);
INSERT INTO drivers(routeID,space,usedSpace) VALUES(5,1500,0);
INSERT INTO drivers(routeID,space,usedSpace) VALUES(6,300,0);
INSERT INTO drivers(routeID,space,usedSpace) VALUES(2,200,0);
SELECT * FROM drivers;


# some join test
# for the user class in python
SELECT u.FirstName , u.LastName, u.Email, u.Phone, a.City, a.Street, a.Number, u.UPassword FROM users u, address a WHERE u.userID = a.userID;

# for the orders table in python
SELECT o.orderID, o.driverID, o.name ,CONCAT(d.City," Str.", d.Street, " Nr.", d.Number) AS Address FROM orders o, destinations d WHERE o.orderID = d.orderID;

select	startCity, interCity1, interCity2, stopCity from routes WHERE interCity1 LIke "Piatra-Neamt" OR interCity2 LIKE "Piatra-Neamt" or stopCity LIKE "Piatra-Neamt";

# some concat
SELECT routeID, CONCAT(startCity ,' ', interCity1 ,' ', interCity2 ,' ', stopCity) AS Route FROM routes where routeID = 1;

# emergency wipe
drop table destinations;
drop table orders;
drop table drivers;
drop table routes;
drop table address;
drop table users;

SELECT    userID
FROM      users
ORDER BY  userID DESC
LIMIT     1;

SELECT * FROM DRIVERS;
SELECT driverID  FROM drivers WHERE  space > usedSpace + 100;
select * from orders;
select * from destinations;