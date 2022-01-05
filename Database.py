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
        print("ceva")

        # case 1) start of route is the city of the pick-up point
        self.command.execute("SELECT startCity  FROM routes WHERE startCity LIKE '" + user.city + "'")
        start_results = self.command.fetchone()
        if start_results:
            # case A destination in the intermediary city 1
            self.command.execute("SELECT interCity  FROM routes WHERE startCity LIKE '" + user.City + "' AND interCity1 LIKE '" + order.City + "'")
            destination_results = self.command.fetchone()
            if destination_results:
                # some routes were found
                # add driver finding phase
                print(destination_results)






    def loadRoute(self, table):
        print("ceva")
        i = 1
        end = 0
        while end == 0:

            self.command.execute(
                "SELECT routeID , CONCAT(startCity ,' ', interCity1 ,' ', interCity2 ,' ', stopCity) " +
                "AS Route FROM routes WHERE routeID =" + str(i))

            result = self.command.fetchone()
            if result:
                print(result["routeID"])
                table.setItem(i - 1, 0, QTableWidgetItem(str(result["routeID"])))
                table.setItem(i - 1, 1, QTableWidgetItem(result["Route"]))
                i = i + 1
            else:
                end = 1

    def loadOrders(self, table):
        print("ceva")
        i = 1
        end = 0
        while end == 0:
            self.command.execute(
                "SELECT o.orderID, o.driverID, o.name ,CONCAT(d.City, ' Str.', d.Street, ' Nr.', d.Number) " +
                "AS Address FROM orders o, destinations d WHERE o.orderID = " + str(i))
            result = self.command.fetchone()
            if result:

                table.setItem(i - 1, 0, QTableWidgetItem(str(result["orderID"])))
                table.setItem(i - 1, 1, QTableWidgetItem(str(result["driverID"])))
                table.setItem(i - 1, 2, QTableWidgetItem(result["name"]))
                table.setItem(i - 1, 3, QTableWidgetItem(result["Address"]))

                i = i + 1
            else:
                end = 1

    def select_existing_user(self, user, email, password):
        self.command.execute(
            "SELECT u.userID ,u.FirstName , u.LastName, u.Email, u.Phone, a.City, a.Street, a.Number, u.UPassword " +
            "FROM users u, address a " +
            "WHERE u.userID = a.userID AND u.Email LIKE '" + email + "';")

        result = self.command.fetchone()
        self.db.commit()

        user.add(
            str(result["userID"]),
            result["FirstName"],
            result["LastName"],
            result["Email"],
            result["Phone"],
            result["City"],
            result["Street"],
            result["Number"],
            result["UPassword"])
