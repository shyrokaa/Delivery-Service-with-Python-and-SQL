
CREATE TABLE users( userID NUMERIC(4) NOT NULL ,userType NUMERIC(4),FirstName varchar2(100), LastName varchar2(100), Email varchar2(100), Phone varchar2(20), UPassword varchar2(100),PRIMARY KEY(userID)); 
SELECT * FROM users;

CREATE TABLE address( userID NUMERIC(4) NOT NULL , City varchar(100), Street varchar2(100), Number1 varchar(20),FOREIGN KEY (userID) REFERENCES users(userID)); 
SELECT * FROM address;

CREATE TABLE routes(routeID NUMERIC(4) NOT NULL ,startCity varchar(100), interCity1 varchar2(100), interCity2 varchar2(100), stopCity varchar2(100),PRIMARY KEY(routeID));
SELECT * FROM routes;

CREATE TABLE drivers( driverID NUMERIC(4) NOT NULL , routeID NUMERIC(4), space NUMERIC(4), usedSpace NUMERIC(4),FOREIGN KEY (routeID) REFERENCES routes(routeID),PRIMARY KEY(driverID));
SELECT * FROM drivers;

CREATE TABLE orders(orderID NUMERIC(4) NOT NULL ,userID NUMERIC(4), driverID NUMERIC(4),name varchar2(100), weight NUMERIC(4), FOREIGN KEY (userID) REFERENCES users(userID),FOREIGN KEY (driverID) REFERENCES drivers(driverID),PRIMARY KEY(orderID));
SELECT * FROM orders;

CREATE TABLE destinations( orderID NUMERIC(4) NOT NULL , City varchar2(100), Street varchar2(100), Number1 varchar2(20),FOREIGN KEY (orderID) REFERENCES orders(orderID)); 
SELECT * FROM destinations;

-- RELATIONSHIPS BETWEEN TABLES
-- ONE TO ONE   - > users (userID)   ---  address(userID)

-- ONE TO MANY  - > users (userID)   ---  orders(userID) 
--			   - > driver(driverID) ---  orders(driverID) 

-- MANY TO MANY - > users(userID)    ---  drivers(driverID)
-- intermediary table = orders

-- INSERTS FOR SOME EXISTING DATA

-- users
INSERT INTO users (userID, userType, FirstName, LastName, Email, Phone, UPassword) VALUES ( 1,1 ,'Mike', 'Bell', 'mbell@gmail.com', '0753765967','parola123');
INSERT INTO users (userID, userType, FirstName, LastName, Email, Phone, UPassword) VALUES ( 2,0 ,'Sara', 'Jones', 'sarj@gmail.com', '0752525464','pass333');
INSERT INTO users (userID, userType, FirstName, LastName, Email, Phone, UPassword) VALUES ( 3,0 ,'Marius', 'Dumitru', 'dumm@gmail.com', '0762523464','pass111');
INSERT INTO users (userID, userType, FirstName, LastName, Email, Phone, UPassword) VALUES ( 4,0 ,'Ioana', 'Maciu', 'maciu@gmail.com', '0752525461','pass222');
INSERT INTO users (userID, userType, FirstName, LastName, Email, Phone, UPassword) VALUES ( 5,0 ,'Mircea', 'Mihai', 'mmirc@gmail.com', '0752525462','pass444');
INSERT INTO users (userID, userType, FirstName, LastName, Email, Phone, UPassword) VALUES ( 6,0 ,'Ion', 'Zapada', 'iamzapada@gmail.com', '0752525463','pass555');
SELECT * FROM users;

-- address
INSERT INTO address(userID,City,Street,Number1) VALUES (1,'Iasi', 'Mihai Eminescu', '15');
INSERT INTO address(userID,City,Street,Number1) VALUES (2,'Iasi', 'Mihai Viteazu', '24');
INSERT INTO address(userID,City,Street,Number1) VALUES (3,'Roman', 'Stefan cel Mare', '1');
INSERT INTO address(userID,City,Street,Number1) VALUES (4,'Piatra-Neamt', 'Emiliei', '12');
INSERT INTO address(userID,City,Street,Number1) VALUES (5,'Vaslui', 'Croitoriei', '2');
INSERT INTO address(userID,City,Street,Number1) VALUES (6,'Bacau', 'Centru', '13');
SELECT * FROM address;

-- routes
INSERT INTO routes(routeID,startCity, interCity1,interCity2,stopCity) VALUES (1,'Iasi','Roman','Piatra-Neamt','Bacau');
INSERT INTO routes(routeID,startCity, interCity1,interCity2,stopCity) VALUES (2,'Bacau','Piatra-Neamt','Roman','Iasi');
INSERT INTO routes(routeID,startCity, interCity1,interCity2,stopCity) VALUES (3,'Bacau','Piatra-Neamt','Targu Neamt','Pascani');
INSERT INTO routes(routeID,startCity, interCity1,interCity2,stopCity) VALUES (4,'Pascani','Targu Neamt','Piatra-Neamt','Bacau');
INSERT INTO routes(routeID,startCity, interCity1,interCity2,stopCity) VALUES (5,'Suceava','Vaslui','Pascani','Iasi');
INSERT INTO routes(routeID,startCity, interCity1,interCity2,stopCity) VALUES (6,'Iasi','Pascani','Vaslui','Suceava');
SELECT * FROM routes;

-- drivers
INSERT INTO drivers(driverID,routeID,space,usedSpace) VALUES(1,1,500,0);
INSERT INTO drivers(driverID,routeID,space,usedSpace) VALUES(2,1,500,0);
INSERT INTO drivers(driverID,routeID,space,usedSpace) VALUES(3,2,450,0);
INSERT INTO drivers(driverID,routeID,space,usedSpace) VALUES(4,3,100,0);
INSERT INTO drivers(driverID,routeID,space,usedSpace) VALUES(5,4,300,0);
INSERT INTO drivers(driverID,routeID,space,usedSpace) VALUES(6,5,1500,0);
INSERT INTO drivers(driverID,routeID,space,usedSpace) VALUES(7,6,300,0);
INSERT INTO drivers(driverID,routeID,space,usedSpace) VALUES(8,2,200,0);
SELECT * FROM drivers;

