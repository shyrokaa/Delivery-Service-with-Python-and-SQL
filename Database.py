from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import os

import mysql.connector


class DB:
    def __init__(self):
        self.db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="ds")
        self.command = self.db.cursor(buffered=True, dictionary=True)

    def select_user(self, fname, lname):
        self.command.execute(
            "SELECT * FROM users where FirstName LIKE '" + fname + "' AND LastName LIKE '" + lname + "';")
        found = 0

        result = self.command.fetchone()
        print(result)

        for item in self.command:
            found = found + 1

        self.db.commit()
        if found == 0:
            return 0
        else:
            return 1

    def look_for_user(self, email, password):
        print("looking for user...")
        self.command.execute(
            "SELECT * FROM users where Email LIKE '" + email + "';")

        result = self.command.fetchone()
        self.db.commit()

        if result:
            if result["Email"] == email:
                if result["UPassword"] == password:
                    return 2
                else:
                    return 1
            else:
                return 0
        else:
            return 0

    def add_new_user(self, user):
        print("adding a new user...")
        # null data will produce an error signaled to user( wont parse data to database due to it being void)
        if user.first_name != "" \
                and user.last_name != "" \
                and user.email != "" \
                and user.phone != "" \
                and user.city != "" \
                and user.street != "" \
                and user.number != "" \
                and user.password != "":
            # checking if the email was already used
            self.command.execute("SELECT * FROM users where Email LIKE '" + user.email + "';")
            found = 0
            for item in self.command:
                found = found + 1
                print(item)

            self.command.execute("SELECT userID FROM users ORDER BY userID DESC LIMIT 1;")
            result = self.command.fetchone()
            new_id = result["userID"] + 1

            if found == 0:
                # empty space found
                self.command.execute(
                    "INSERT INTO users(userID,userType,FirstName, LastName, Email, Phone, UPassword) "
                    "VALUES(" +
                    str(new_id) + "," +
                    str(user.type) + "," +
                    "'" + user.first_name + "'," +
                    "'" + user.last_name + "'," +
                    "'" + user.email + "'," +
                    "'" + user.phone + "'," +
                    "'" + user.password + "')")

                self.command.execute(
                    "INSERT INTO address(userID,City,Street,Number) "
                    "VALUES(" +
                    str(new_id) + "," +
                    "'" + user.city + "'," +
                    "'" + user.street + "'," +
                    "'" + user.number + "')")

                self.db.commit()
                return 1
            else:
                # there is no empty space there
                return 0
        else:
            return 0

    def add_new_order(self, order, user):
        # considering order being loaded in already
        self.command.execute("SELECT orderID FROM orders ORDER BY orderID DESC LIMIT 1;")
        result = self.command.fetchone()
        if result:
            new_id = result["orderID"] + 1
        else:
            new_id = "1"

        # case 1) start of route is the city of the pick-up point
        self.command.execute("SELECT startCity  FROM routes WHERE startCity LIKE '" + user.city + "'")
        start_results = self.command.fetchone()
        if start_results:
            # case A destination in the intermediary city 1
            self.command.execute(
                "SELECT routeID, interCity1  FROM routes WHERE startCity LIKE '" + user.city + "' AND interCity1 LIKE '"
                + order.city + "'")

            destination_results = self.command.fetchone()
            if destination_results:
                self.command.execute(
                    "SELECT driverID  FROM drivers WHERE  space > usedSpace + " + str(order.weight) + " AND routeID ="
                    + str(destination_results["routeID"]))
                driver_results = self.command.fetchone()
                if driver_results:
                    self.command.execute("INSERT INTO orders(orderID,userID,driverID,name,weight) VALUES("
                                         + str(new_id) + ", "
                                         + user.uid + ", "
                                         + str(driver_results["driverID"]) + ", "
                                         + "'" + order.name + "',"
                                         + order.weight + ")")
                    self.command.execute("INSERT INTO destinations(orderID,city,street,number) VALUES("
                                         + str(new_id) + ", "
                                         + "'" + order.city + "', "
                                         + "'" + order.street + "', "
                                         + "'" + order.number + "')")
                    self.command.execute(
                        "UPDATE drivers SET usedSpace =  usedSpace + " + str(order.weight) +
                        " WHERE driverID = " + str(driver_results["driverID"]))
                    self.db.commit()
                    return 1

            # case B destination in the intermediary city 2
            self.command.execute(
                "SELECT routeID, interCity2  FROM routes WHERE startCity LIKE '" + user.city + "' AND interCity2 LIKE '" + order.city + "'")
            destination_results = self.command.fetchone()
            if destination_results:
                self.command.execute(
                    "SELECT driverID  FROM drivers WHERE  space > usedSpace + " + str(order.weight) + " AND routeID ="
                    + str(destination_results["routeID"]))
                driver_results = self.command.fetchone()
                if driver_results:
                    self.command.execute("INSERT INTO orders(orderID,userID,driverID,name,weight) VALUES("
                                         + str(new_id) + ", "
                                         + user.uid + ", "
                                         + str(driver_results["driverID"]) + ", "
                                         + "'" + order.name + "', "
                                         + order.weight + ")")
                    self.command.execute("INSERT INTO destinations(orderID,city,street,number) VALUES("
                                         + str(new_id) + ", "
                                         + "'" + order.city + "', "
                                         + "'" + order.street + "', "
                                         + "'" + order.number + "')")
                    self.command.execute(
                        "UPDATE drivers SET usedSpace =  usedSpace + " + str(order.weight) +
                        " WHERE driverID = " + str(driver_results["driverID"]))
                    self.db.commit()
                    return 1

            # case C destination in the intermediary city 2
            self.command.execute(
                "SELECT routeID, stopCity  FROM routes WHERE startCity LIKE '" + user.city + "' AND stopCity LIKE '" + order.city + "'")
            destination_results = self.command.fetchone()
            if destination_results:
                self.command.execute(
                    "SELECT driverID  FROM drivers WHERE  space > usedSpace + " + str(order.weight) + " AND routeID ="
                    + str(destination_results["routeID"]))
                driver_results = self.command.fetchone()
                if driver_results:
                    self.command.execute("INSERT INTO orders(orderID,userID,driverID,name,weight) VALUES("
                                         + str(new_id) + ", "
                                         + user.uid + ", "
                                         + str(driver_results["driverID"]) + ", "
                                         + "'" + order.name + "', "
                                         + order.weight + ")")
                    self.command.execute("INSERT INTO destinations(orderID,city,street,number) VALUES("
                                         + str(new_id) + ", "
                                         + "'" + order.city + "', "
                                         + "'" + order.street + "', "
                                         + "'" + order.number + "')")
                    self.command.execute(
                        "UPDATE drivers SET usedSpace =  usedSpace + " + str(order.weight) +
                        " WHERE driverID = " + str(driver_results["driverID"]))
                    self.db.commit()
                    return 1

        # case 2) inter1 of route is the city of the pick-up point
        self.command.execute("SELECT interCity1  FROM routes WHERE startCity LIKE '" + user.city + "'")
        start_results = self.command.fetchone()
        if start_results:
            # case A destination in the intermediary city 2
            self.command.execute(
                "SELECT routeID, interCity2  FROM routes WHERE startCity LIKE '" + user.city + "' AND interCity2 LIKE '" + order.city + "'")
            destination_results = self.command.fetchone()
            if destination_results:
                self.command.execute(
                    "SELECT driverID  FROM drivers WHERE  space > usedSpace + " + str(order.weight) + " AND routeID ="
                    + str(destination_results["routeID"]))
                driver_results = self.command.fetchone()
                if driver_results:
                    self.command.execute("INSERT INTO orders(orderID,userID,driverID,name,weight) VALUES("
                                         + str(new_id) + ", "
                                         + user.uid + ", "
                                         + str(driver_results["driverID"]) + ", "
                                         + "'" + order.name + "', "
                                         + order.weight + ")")
                    self.command.execute("INSERT INTO destinations(orderID,city,street,number) VALUES("
                                         + str(new_id) + ", "
                                         + "'" + order.city + "', "
                                         + "'" + order.street + "', "
                                         + "'" + order.number + "')")
                    self.command.execute(
                        "UPDATE drivers SET usedSpace =  usedSpace + " + str(order.weight) +
                        " WHERE driverID = " + str(driver_results["driverID"]))
                    self.db.commit()
                    return 1

            # case B destination in the stop city
            self.command.execute(
                "SELECT routeID, stopCity  FROM routes WHERE startCity LIKE '" + user.city + "' AND stopCity LIKE '" + order.city + "'")
            destination_results = self.command.fetchone()
            if destination_results:
                self.command.execute(
                    "SELECT driverID  FROM drivers WHERE  space > usedSpace + " + str(order.weight) + " AND routeID ="
                    + str(destination_results["routeID"]))
                driver_results = self.command.fetchone()
                if driver_results:
                    self.command.execute("INSERT INTO orders(orderID,userID,driverID,name,weight) VALUES("
                                         + str(new_id) + ", "
                                         + user.uid + ", "
                                         + str(driver_results["driverID"]) + ", "
                                         + "'" + order.name + "', "
                                         + order.weight + ")")
                    self.command.execute("INSERT INTO destinations(orderID,city,street,number) VALUES("
                                         + str(new_id) + ", "
                                         + "'" + order.city + "', "
                                         + "'" + order.street + "', "
                                         + "'" + order.number + "')")
                    self.command.execute(
                        "UPDATE drivers SET usedSpace =  usedSpace + " + str(order.weight) +
                        " WHERE driverID = " + str(driver_results["driverID"]))
                    self.db.commit()
                    return 1

        # case 3) inter2 of route is the city of the pick-up point
        self.command.execute("SELECT interCity1  FROM routes WHERE startCity LIKE '" + user.city + "'")
        start_results = self.command.fetchone()
        if start_results:
            # case A destination in the stop city
            self.command.execute(
                "SELECT routeID,stopCity  FROM routes WHERE startCity LIKE '" + user.city + "' AND stopCity LIKE '" + order.city + "'")
            destination_results = self.command.fetchone()
            if destination_results:
                self.command.execute(
                    "SELECT driverID  FROM drivers WHERE  space > usedSpace + " + str(order.weight) + " AND routeID ="
                    + str(destination_results["routeID"]))
                driver_results = self.command.fetchone()
                if driver_results:
                    self.command.execute("INSERT INTO orders(orderID,userID,driverID,name,weight) VALUES("
                                         + str(new_id) + ", "
                                         + user.uid + ", "
                                         + str(driver_results["driverID"]) + ", "
                                         + "'" + order.name + "', "
                                         + order.weight + ")")
                    self.command.execute("INSERT INTO destinations(orderID,city,street,number) VALUES("
                                         + str(new_id) + ", "
                                         + "'" + order.city + "', "
                                         + "'" + order.street + "', "
                                         + "'" + order.number + "')")
                    self.command.execute(
                        "UPDATE drivers SET usedSpace =  usedSpace + " + str(order.weight) +
                        " WHERE driverID = " + str(driver_results["driverID"]))
                    self.db.commit()
                    return 1
        return 0

    def loadRoute(self, table):
        print("loading routes...")
        i = 1
        j = 1
        self.command.execute("SELECT routeID FROM routes ORDER BY routeID DESC LIMIT 1;")
        result = self.command.fetchone()
        count = result["routeID"] + 1

        while i < count:

            self.command.execute(
                "SELECT routeID , CONCAT(startCity ,' ', interCity1 ,' ', interCity2 ,' ', stopCity) " +
                "AS Route FROM routes WHERE routeID =" + str(i))

            result = self.command.fetchone()
            if result:
                table.setItem(j - 1, 0, QTableWidgetItem(str(result["routeID"])))
                table.setItem(j - 1, 1, QTableWidgetItem(result["Route"]))
                j = j + 1
            i = i + 1

    def loadDriver(self, table):
        print("loading drivers...")
        i = 1
        j = 1
        self.command.execute("SELECT driverID FROM drivers ORDER BY driverID DESC LIMIT 1;")
        result = self.command.fetchone()
        count = result["driverID"] + 1

        while i < count:

            self.command.execute(
                "SELECT d.driverID, d.routeID , " +
                "CONCAT(r.startCity ,' ', r.interCity1 ,' ', r.interCity2 ,' ', r.stopCity) " +
                "AS Route FROM routes r , drivers d WHERE r.routeID = d.routeID AND driverID =" + str(i))

            result = self.command.fetchone()
            if result:
                table.setItem(j - 1, 0, QTableWidgetItem(str(result["driverID"])))
                table.setItem(j - 1, 1, QTableWidgetItem(str(result["routeID"])))
                table.setItem(j - 1, 2, QTableWidgetItem(result["Route"]))
                j = j + 1
            i = i + 1

    def loadOrders(self, table, user):
        print("loading orders...")
        i = 1
        j = 1
        self.command.execute("SELECT orderID FROM orders ORDER BY orderID DESC LIMIT 1;")
        result = self.command.fetchone()
        count = result["orderID"] + 1

        while i < count:
            self.command.execute(
                "SELECT o.orderID, o.driverID, o.name ,CONCAT(d.City, ' Str.', d.Street, ' Nr.', d.Number) " +
                "AS Address FROM orders o, destinations d WHERE d.orderID = o.orderID AND o.orderID = " + str(
                    i) + " AND o.userID = " + user.uid)
            result = self.command.fetchone()
            if result:
                table.setItem(j - 1, 0, QTableWidgetItem(str(result["orderID"])))
                table.setItem(j - 1, 1, QTableWidgetItem(str(result["driverID"])))
                table.setItem(j - 1, 2, QTableWidgetItem(result["name"]))
                table.setItem(j - 1, 3, QTableWidgetItem(result["Address"]))
                j = j + 1
            i = i + 1

    def select_existing_user(self, user, email, password):
        self.command.execute(
            "SELECT u.userID ,u.userType, u.FirstName , u.LastName, u.Email, u.Phone, a.City, a.Street, a.Number, u.UPassword " +
            "FROM users u, address a " +
            "WHERE u.userID = a.userID AND u.Email LIKE '" + email + "';")

        result = self.command.fetchone()
        self.db.commit()

        user.add(
            str(result["userID"]),
            result["userType"],
            result["FirstName"],
            result["LastName"],
            result["Email"],
            result["Phone"],
            result["City"],
            result["Street"],
            result["Number"],
            result["UPassword"])

    def remove_route(self, ID):
        print("removing route...")

        self.command.execute("SELECT o.orderID, d.driverID FROM orders o, drivers d " +
                             "WHERE d.driverID = o.driverID AND d.routeID = " + ID)
        result = self.command.fetchone()
        if result:
            return 1
        else:
            self.command.execute("DELETE FROM drivers WHERE routeID = " + ID)
            self.command.execute("DELETE FROM routes WHERE routeID = " + ID)
            self.db.commit()
        return 0

    def add_route(self, startC, interC1, interC2, stopC):
        print("adding route...")
        self.command.execute("SELECT routeID FROM routes ORDER BY routeID DESC LIMIT 1;")
        result = self.command.fetchone()
        new_id = result["routeID"] + 1
        self.command.execute("INSERT INTO routes(routeID, startCity, interCity1,interCity2,stopCity) VALUES("
                             + str(new_id) + ","
                             + "'" + startC + "',"
                             + "'" + interC1 + "',"
                             + "'" + interC2 + "',"
                             + "'" + stopC + "')"
                             )
        self.db.commit()

    def remove_driver(self, ID):
        print("removing route...")

        self.command.execute("SELECT o.orderID, d.driverID FROM orders o, drivers d " +
                             "WHERE d.driverID = o.driverID AND d.driverID = " + ID)
        result = self.command.fetchone()
        if result:
            return 1
        else:
            self.command.execute("DELETE FROM drivers WHERE driverID = " + ID)
            self.db.commit()
        return 0

    def add_driver(self, RID, space, uspace):
        print("adding route...")
        self.command.execute("SELECT driverID FROM drivers ORDER BY driverID DESC LIMIT 1;")
        result = self.command.fetchone()
        new_id = result["driverID"] + 1
        self.command.execute("INSERT INTO drivers(driverID, routeID, space,usedSpace) VALUES("
                             + str(new_id) + ","
                             + RID + ","
                             + space + ","
                             + uspace + ")"
                             )
        self.db.commit()

    def remove_order(self, ID):
        print("removing order...")

        self.command.execute("SELECT * FROM orders WHERE orderID = " + ID)
        order = self.command.fetchone()

        self.command.execute(
            "SELECT o.orderID, d.driverID FROM orders o, drivers d WHERE d.driverID = o.driverID AND o.orderID = " + ID)
        driver = self.command.fetchone()
        self.command.execute(
            "UPDATE drivers SET usedSpace =  usedSpace - " + str(order["weight"]) +
            " WHERE driverID = " + str(driver["driverID"]))
        self.command.execute("DELETE FROM destinations WHERE orderID = " + ID)
        self.command.execute("DELETE FROM orders WHERE orderID = " + ID)
        self.db.commit()

    def loadallOrders(self, table):
        print("loading orders...")
        i = 1
        j = 1
        self.command.execute("SELECT orderID FROM orders ORDER BY orderID DESC LIMIT 1;")
        result = self.command.fetchone()
        count = result["orderID"] + 1

        while i < count:
            self.command.execute(
                "SELECT o.orderID , u.FirstName , o.name , o.weight " +
                "FROM orders o,users u WHERE u.userID = o.userID AND o.orderID =" + str(i))
            result = self.command.fetchone()
            if result:
                table.setItem(j - 1, 0, QTableWidgetItem(str(result["orderID"])))
                table.setItem(j - 1, 1, QTableWidgetItem(result["FirstName"]))
                table.setItem(j - 1, 2, QTableWidgetItem(result["name"]))
                table.setItem(j - 1, 3, QTableWidgetItem(str(result["weight"])))
                j = j + 1
            i = i + 1
