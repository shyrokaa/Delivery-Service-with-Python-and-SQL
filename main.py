# imports for the interface
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import os

# imports for SQL functionality

from Database import *
from User import *
from Order import *
from stringFunctions import *

# some control values for this thing to check if the user is signed in + to see if the profile is found in the
# database + to see if the password matches the one in the database + to see if the user is an admin
signedIn = True
validProfile = True
validPass = True
admin = False
# surface level information about the user of the database


# global database for simplicity
DATABASE = DB()


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Delivery Service Home")
        self.initUI()
        # user is defined here for simplicity
        self.user = User()
        self.order = Order()

    def initUI(self):
        self.image = QtWidgets.QLabel(self)

        if os.path.isfile("Assets//logo.png"):
            print("image loaded")
            pixmap = QPixmap("Assets//logo.png")
            self.image.resize(pixmap.width(), pixmap.height())
            self.image.setPixmap(pixmap)
            self.image.move(150, 10)
        else:
            print("error in image path")

        # labels
        self.title = QtWidgets.QLabel(self)
        self.title.setFont(QFont('Arial', 20))
        self.title.setText("Delivery Services Moldova")
        self.title.adjustSize()
        self.title.move(100, 160)

        # buttons and such
        # new user
        self.newaccount_btt = QtWidgets.QPushButton(self)
        self.newaccount_btt.setText("Sign up")
        self.newaccount_btt.move(200, 200)
        self.newaccount_btt.clicked.connect(self.newAccount)

        # existing user
        self.signIn_btt = QtWidgets.QPushButton(self)
        self.signIn_btt.setText("Sign In")
        self.signIn_btt.move(200, 250)
        self.signIn_btt.clicked.connect(self.signIn)

        # routes

        self.routes_btt = QtWidgets.QPushButton(self)
        self.routes_btt.setText("Routes")
        self.routes_btt.move(200, 300)
        self.routes_btt.clicked.connect(self.routes)

    def newAccount(self):
        self.sup = SignUP()
        self.hide()
        self.sup.show()
        self.TOGGLE = False

    def signIn(self):
        self.sin = SignIN()
        self.sin.show()
        self.hide()
        self.TOGGLE = True

    def routes(self):
        self.rou = Routes()
        self.hide()
        self.rou.show()


# global main window for easier access to it and such
app = QApplication(sys.argv)
win = MainWindow()


class NewOrder(QMainWindow):
    def __init__(self):
        super(NewOrder, self).__init__()
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("New Order")
        self.initUI()

    def initUI(self):
        # Drop OFF information
        self.tab2 = QtWidgets.QLabel(self)
        self.tab2.setText("Drop OFF")
        self.tab2.move(150, 50)

        self.name2 = QtWidgets.QLabel(self)
        self.name2.setText("Name")
        self.name2.move(150, 100)

        self.city2 = QtWidgets.QLabel(self)
        self.city2.setText("City")
        self.city2.move(150, 150)

        self.street2 = QtWidgets.QLabel(self)
        self.street2.setText("Street")
        self.street2.move(150, 200)

        self.number2 = QtWidgets.QLabel(self)
        self.number2.setText("Number")
        self.number2.move(150, 250)

        self.weight = QtWidgets.QLabel(self)
        self.weight.setText("Weight")
        self.weight.move(150, 300)

        self.error = QtWidgets.QLabel(self)
        self.error.setText("")
        self.error.move(50, 300)

        self.name2_text = QtWidgets.QTextEdit(self)
        self.name2_text.move(200, 100)

        self.city2_text = QtWidgets.QTextEdit(self)
        self.city2_text.move(200, 150)

        self.street2_text = QtWidgets.QTextEdit(self)
        self.street2_text.move(200, 200)

        self.number2_text = QtWidgets.QTextEdit(self)
        self.number2_text.move(200, 250)

        self.weight_text = QtWidgets.QTextEdit(self)
        self.weight_text.move(200, 300)

        # buttons and stuff
        self.back_btt = QtWidgets.QPushButton(self)
        self.back_btt.setText("Home")
        self.back_btt.move(400, 0)
        self.back_btt.clicked.connect(self.back)

        self.enter_btt = QtWidgets.QPushButton(self)
        self.enter_btt.setText("Place order")
        self.enter_btt.move(200, 350)
        self.enter_btt.clicked.connect(self.enter)

    def enter(self):
        # check for good pass and email in the database
        win.order.add_base_data(self.name2_text.toPlainText(),
                                self.city2_text.toPlainText(),
                                self.street2_text.toPlainText(),
                                self.number2_text.toPlainText(),
                                self.weight_text.toPlainText())

        err = DATABASE.add_new_order(win.order, win.user)
        if err == 0:
            self.error.setText("No Driver Found")
            self.error.adjustSize()
        else:

            if win.TOGGLE:
                self.hide()
                win.sin.profile.show()
            else:
                self.hide()
                win.sup.profile.show()

    def back(self):
        if win.TOGGLE:
            self.hide()
            win.sin.profile.show()
        else:
            self.hide()
            win.sup.profile.show()


class SignIN(QMainWindow):
    def __init__(self):
        super(SignIN, self).__init__()
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("New Order")
        self.initUI()

    def initUI(self):
        self.title = QtWidgets.QLabel(self)
        self.title.setFont(QFont('Arial', 20))
        self.title.setText("Sign In")
        self.title.adjustSize()
        self.title.move(200, 100)

        self.email = QtWidgets.QLabel(self)
        self.email.setText("Email")
        self.email.move(150, 150)

        self.password = QtWidgets.QLabel(self)
        self.password.setText("Password")
        self.password.move(150, 200)

        self.errlabel = QtWidgets.QLabel(self)
        self.errlabel.setText("")
        self.errlabel.adjustSize()
        self.errlabel.move(150, 300)

        self.enter_btt = QtWidgets.QPushButton(self)
        self.enter_btt.setText("Sign in")
        self.enter_btt.move(200, 250)
        self.enter_btt.clicked.connect(self.enter)

        self.back_btt = QtWidgets.QPushButton(self)
        self.back_btt.setText("Home")
        self.back_btt.move(400, 0)
        self.back_btt.clicked.connect(self.back)

        self.email_text = QtWidgets.QTextEdit(self)
        self.email_text.move(200, 150)

        self.password_text = QtWidgets.QTextEdit(self)
        self.password_text.move(200, 200)

    def enter(self):
        # check for good pass and email in the database

        valid = DATABASE.look_for_user(self.email_text.toPlainText(), self.password_text.toPlainText())

        if valid == 2:
            print("correct")
            DATABASE.select_existing_user(win.user, self.email_text.toPlainText(), self.password_text.toPlainText())
            self.profile = Profile()
            self.profile.show()
            self.hide()
        elif valid == 1:
            self.errlabel.setText("Wrong Password")
            self.errlabel.adjustSize()
        else:
            self.errlabel.setText("No Account found")
            self.errlabel.adjustSize()

    def back(self):
        win.show()
        self.hide()


class SignUP(QMainWindow):
    def __init__(self):
        super(SignUP, self).__init__()
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Sign Up")
        self.initUI()

    def initUI(self):
        # labels

        self.title = QtWidgets.QLabel(self)
        self.title.setFont(QFont('Arial', 20))
        self.title.setText("Sign Up")
        self.title.adjustSize()
        self.title.move(200, 20)

        # bad input
        self.binput = QtWidgets.QLabel(self)
        self.binput.setFont(QFont('Arial', 10))
        self.binput.setText("")
        self.binput.adjustSize()
        self.binput.move(400, 400)

        self.fname = QtWidgets.QLabel(self)
        self.fname.setFont(QFont('Arial', 10))
        self.fname.setText("First Name")
        self.fname.adjustSize()
        self.fname.move(150, 100)

        self.lname = QtWidgets.QLabel(self)
        self.lname.setFont(QFont('Arial', 10))
        self.lname.setText("Last Name")
        self.lname.adjustSize()
        self.lname.move(150, 150)

        self.email = QtWidgets.QLabel(self)
        self.email.setFont(QFont('Arial', 10))
        self.email.setText("Email")
        self.email.adjustSize()
        self.email.move(150, 200)

        self.phone = QtWidgets.QLabel(self)
        self.phone.setFont(QFont('Arial', 10))
        self.phone.setText("Phone Number")
        self.phone.adjustSize()
        self.phone.move(150, 250)

        self.city = QtWidgets.QLabel(self)
        self.city.setFont(QFont('Arial', 10))
        self.city.setText("City")
        self.city.adjustSize()
        self.city.move(150, 300)

        self.street = QtWidgets.QLabel(self)
        self.street.setFont(QFont('Arial', 10))
        self.street.setText("Street")
        self.street.adjustSize()
        self.street.move(150, 350)

        self.number = QtWidgets.QLabel(self)
        self.number.setFont(QFont('Number', 10))
        self.number.setText("Number")
        self.number.adjustSize()
        self.number.move(150, 400)

        self.password = QtWidgets.QLabel(self)
        self.password.setFont(QFont('Arial', 10))
        self.password.setText("Password")
        self.password.adjustSize()
        self.password.move(150, 450)

        # buttons

        # Sign Up button, obvioous reasons

        self.enter_btt = QtWidgets.QPushButton(self)
        self.enter_btt.setText("Sign up")
        self.enter_btt.move(400, 450)
        self.enter_btt.clicked.connect(self.enter)

        # return to main window for more information

        self.back_btt = QtWidgets.QPushButton(self)
        self.back_btt.setText("Home")
        self.back_btt.move(400, 0)
        self.back_btt.clicked.connect(self.back)

        # text boxes for information to introduce into the database

        self.fname_text = QtWidgets.QTextEdit(self)
        self.fname_text.move(260, 95)

        self.lname_text = QtWidgets.QTextEdit(self)
        self.lname_text.move(260, 145)

        self.email_text = QtWidgets.QTextEdit(self)
        self.email_text.move(260, 195)

        self.phone_text = QtWidgets.QTextEdit(self)
        self.phone_text.move(260, 245)

        self.city_text = QtWidgets.QTextEdit(self)
        self.city_text.move(260, 295)

        self.street_text = QtWidgets.QTextEdit(self)
        self.street_text.move(260, 345)

        self.number_text = QtWidgets.QTextEdit(self)
        self.number_text.move(260, 395)

        self.password_text = QtWidgets.QTextEdit(self)
        self.password_text.move(260, 445)

    def enter(self):
        print("data introduced into database")

        # adding on screen information to the user

        DATABASE.command.execute("SELECT userID FROM users ORDER BY userID DESC LIMIT 1;")
        result = DATABASE.command.fetchone()
        new_id = result["userID"] + 1

        win.user.add(
            str(new_id),
            0,
            self.fname_text.toPlainText(),
            self.lname_text.toPlainText(),
            self.email_text.toPlainText(),
            self.phone_text.toPlainText(),
            self.city_text.toPlainText(),
            self.street_text.toPlainText(),
            self.number_text.toPlainText(),
            self.password_text.toPlainText())

        # entering data in the database if possible

        valid = DATABASE.add_new_user(win.user)

        if valid:
            self.profile = Profile()
            self.profile.show()
            self.hide()
            self.binput.setText("")
            self.binput.adjustSize()
        else:
            self.binput.setText("Invalid Data")
            self.binput.adjustSize()

    def back(self):
        win.show()
        self.hide()


class Routes(QMainWindow):
    def __init__(self):
        super(Routes, self).__init__()
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Routes")
        self.initUI()

    def initUI(self):
        # labels
        self.title = QtWidgets.QLabel(self)
        self.title.setFont(QFont('Arial', 20))
        self.title.setText("Available Routes")
        self.title.adjustSize()
        self.title.move(150, 20)

        # table to display the routes in the table
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.resize(350, 350)
        self.tableWidget.move(100, 100)
        DATABASE.loadRoute(self.tableWidget)

        # buttons
        self.back_btt = QtWidgets.QPushButton(self)
        self.back_btt.setText("Home")
        self.back_btt.move(400, 0)
        self.back_btt.clicked.connect(self.back)

    def back(self):
        self.hide()
        win.show()


class Profile(QMainWindow):
    def __init__(self):
        super(Profile, self).__init__()
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Profile")
        self.initUI()

    def initUI(self):

        # profile image so that it looks more like something authentic and not some demonstration
        # self.photo.setPixmap(QtGui.QPixmap("Assets//default_profile_picture.png"))
        self.image = QtWidgets.QLabel(self)

        if os.path.isfile("Assets//default_profile_picture.png"):
            print("image loaded")
            pixmap = QPixmap("Assets//default_profile_picture.png")
            self.image.resize(pixmap.width(), pixmap.height())
            self.image.setPixmap(pixmap)
            self.image.move(40, 10)
        else:
            print("error in image path")

        # labels
        self.title = QtWidgets.QLabel(self)
        self.title.setFont(QFont('Arial', 20))
        self.title.setText("Your Profile")
        self.title.adjustSize()
        self.title.move(120, 0)

        # buttons ( will depend on the profile)

        self.back_btt = QtWidgets.QPushButton(self)
        self.back_btt.setText("Sign Out")
        self.back_btt.move(400, 0)
        self.back_btt.clicked.connect(self.back)

        if win.user.type != 1:
            self.orders_btt = QtWidgets.QPushButton(self)
            self.orders_btt.setText("Your Orders")
            self.orders_btt.move(150, 300)
            self.orders_btt.clicked.connect(self.orders)

            self.neworder_btt = QtWidgets.QPushButton(self)
            self.neworder_btt.setText("NewOrder")
            self.neworder_btt.move(150, 350)
            self.neworder_btt.clicked.connect(self.newOrder)
        else:
            self.routes_btt = QtWidgets.QPushButton(self)
            self.routes_btt.setText("Add New Route")
            self.routes_btt.move(150, 300)
            self.routes_btt.clicked.connect(self.routes)

            self.drivers_btt = QtWidgets.QPushButton(self)
            self.drivers_btt.setText("Add New Driver")
            self.drivers_btt.move(150, 350)
            self.drivers_btt.clicked.connect(self.drivers)

            self.orders_btt = QtWidgets.QPushButton(self)
            self.orders_btt.setText("Complete Orders")
            self.orders_btt.move(150, 400)
            self.orders_btt.clicked.connect(self.ordersC)

        # profile biz

        # user id

        self.uid_label = QtWidgets.QLabel(self)
        self.uid_label.setFont(QFont('Arial', 10))
        self.uid_label.setText("User ID:")
        self.uid_label.adjustSize()
        self.uid_label.move(300, 50)

        self.uid = QtWidgets.QLabel(self)
        self.uid.setFont(QFont('Arial', 10))
        self.uid.setText(win.user.uid)
        self.uid.adjustSize()
        self.uid.move(380, 50)

        # first name
        self.first_name_label = QtWidgets.QLabel(self)
        self.first_name_label.setFont(QFont('Arial', 10))
        self.first_name_label.setText("First Name:")
        self.first_name_label.adjustSize()
        self.first_name_label.move(300, 100)

        self.first_name = QtWidgets.QLabel(self)
        self.first_name.setFont(QFont('Arial', 10))
        self.first_name.setText(win.user.first_name)
        self.first_name.adjustSize()
        self.first_name.move(380, 100)

        # last name
        self.last_name_label = QtWidgets.QLabel(self)
        self.last_name_label.setFont(QFont('Arial', 10))
        self.last_name_label.setText("Last Name:")
        self.last_name_label.adjustSize()
        self.last_name_label.move(300, 120)

        self.last_name = QtWidgets.QLabel(self)
        self.last_name.setFont(QFont('Arial', 10))
        self.last_name.setText(win.user.last_name)
        self.last_name.adjustSize()
        self.last_name.move(380, 120)

    def back(self):
        self.hide()
        win.show()

    def orders(self):
        self.orders = Orders()
        self.orders.show()
        self.hide()

    def routes(self):
        print("here should be a list of the orders one placed")
        self.routes = RouteAlter()
        self.routes.show()
        self.hide()

    def drivers(self):
        print("here should be a list of the drivers one placed")
        self.drivers = DriverAlter()
        self.drivers.show()
        self.hide()

    def ordersC(self):
        print("here should be a list of the orders")
        self.ordersC = OrderAlter()
        self.ordersC.show()
        self.hide()

    def newOrder(self):
        self.newo = NewOrder()
        self.newo.show()
        self.hide()


class Orders(QMainWindow):
    def __init__(self):
        super(Orders, self).__init__()
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Profile")
        self.initUI()

    def initUI(self):
        # labels
        self.title = QtWidgets.QLabel(self)
        self.title.setFont(QFont('Arial', 20))
        self.title.setText("Your Orders")
        self.title.adjustSize()
        self.title.move(150, 50)

        # table of orders

        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setColumnWidth(0, 20)
        self.tableWidget.setColumnWidth(1, 20)
        self.tableWidget.setColumnWidth(2, 80)
        self.tableWidget.setColumnWidth(3, 180)

        self.tableWidget.resize(360, 400)
        self.tableWidget.move(75, 100)

        DATABASE.loadOrders(self.tableWidget,win.user)

        self.back_btt = QtWidgets.QPushButton(self)
        self.back_btt.setText("Back")
        self.back_btt.move(400, 0)
        self.back_btt.clicked.connect(self.back)

    def back(self):
        self.hide()
        if win.TOGGLE:
            win.sin.profile.show()
        else:
            win.sup.profile.show()

class RouteAlter(QMainWindow):
    def __init__(self):
        super(RouteAlter, self).__init__()
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Profile")
        self.initUI()

    def initUI(self):
        # labels
        self.title = QtWidgets.QLabel(self)
        self.title.setFont(QFont('Arial', 20))
        self.title.setText("Add or remove a route")
        self.title.adjustSize()
        self.title.move(150, 50)

        # table of orders

        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.resize(350, 100)
        self.tableWidget.move(50, 350)
        DATABASE.loadRoute(self.tableWidget)

        self.startC_label = QtWidgets.QLabel(self)
        self.startC_label.setFont(QFont('Arial', 10))
        self.startC_label.setText("Start City:")
        self.startC_label.adjustSize()
        self.startC_label.move(100, 100)

        self.interC1_label = QtWidgets.QLabel(self)
        self.interC1_label.setFont(QFont('Arial', 10))
        self.interC1_label.setText("Intermediate City 1:")
        self.interC1_label.adjustSize()
        self.interC1_label.move(100, 150)

        self.interC2_label = QtWidgets.QLabel(self)
        self.interC2_label.setFont(QFont('Arial', 10))
        self.interC2_label.setText("Intermediate City 1:")
        self.interC2_label.adjustSize()
        self.interC2_label.move(100, 200)

        self.stopC_label = QtWidgets.QLabel(self)
        self.stopC_label.setFont(QFont('Arial', 10))
        self.stopC_label.setText("Stop City:")
        self.stopC_label.adjustSize()
        self.stopC_label.move(100, 250)

        self.ID_label = QtWidgets.QLabel(self)
        self.ID_label.setFont(QFont('Arial', 10))
        self.ID_label.setText("Route ID to remove:")
        self.ID_label.adjustSize()
        self.ID_label.move(100, 300)

        self.err_label = QtWidgets.QLabel(self)
        self.err_label.setFont(QFont('Arial', 10))
        self.err_label.setText("")
        self.err_label.adjustSize()
        self.err_label.move(50, 450)

        # specific values

        self.startC = QtWidgets.QTextEdit(self)
        self.startC.move(230, 100)

        self.interC1 = QtWidgets.QTextEdit(self)
        self.interC1.move(230, 150)

        self.interC2 = QtWidgets.QTextEdit(self)
        self.interC2.move(230, 200)

        self.stopC = QtWidgets.QTextEdit(self)
        self.stopC.move(230, 250)

        self.ID = QtWidgets.QTextEdit(self)
        self.ID.move(230, 300)

        # buttons to work with

        self.back_btt = QtWidgets.QPushButton(self)
        self.back_btt.setText("Back")
        self.back_btt.move(400, 0)
        self.back_btt.clicked.connect(self.back)

        self.insert_btt = QtWidgets.QPushButton(self)
        self.insert_btt.setText("Insert")
        self.insert_btt.move(400, 175)
        self.insert_btt.clicked.connect(self.insert)

        self.delete_btt = QtWidgets.QPushButton(self)
        self.delete_btt.setText("Remove")
        self.delete_btt.move(400, 300)
        self.delete_btt.clicked.connect(self.delete)

    def back(self):
        self.hide()
        if win.TOGGLE:
            win.sin.profile.show()
        else:
            win.sup.profile.show()

    def insert(self):
        # INSERTING VALUES AND UPDATING THE UI TABLE
        DATABASE.add_route(self.startC.toPlainText(),
                           self.interC1.toPlainText(),
                           self.interC2.toPlainText(),
                           self.stopC.toPlainText())
        DATABASE.loadRoute(self.tableWidget)

    def delete(self):
        error = DATABASE.remove_route(self.ID.toPlainText())
        if error:
            self.err_label.setText("orders exist on this route!")
            self.err_label.adjustSize()
        else:
            self.err_label.setText("")
            self.err_label.adjustSize()


class DriverAlter(QMainWindow):
    def __init__(self):
        super(DriverAlter, self).__init__()
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Profile")
        self.initUI()

    def initUI(self):
        # labels
        self.title = QtWidgets.QLabel(self)
        self.title.setFont(QFont('Arial', 20))
        self.title.setText("Add or remove a driver")
        self.title.adjustSize()
        self.title.move(150, 50)

        # table of orders

        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 50)
        self.tableWidget.setColumnWidth(2, 200)
        self.tableWidget.resize(350, 100)
        self.tableWidget.move(50, 350)
        DATABASE.loadDriver(self.tableWidget)


        self.RID_label = QtWidgets.QLabel(self)
        self.RID_label.setFont(QFont('Arial', 10))
        self.RID_label.setText("Route ID:")
        self.RID_label.adjustSize()
        self.RID_label.move(100, 100)

        self.space_label = QtWidgets.QLabel(self)
        self.space_label.setFont(QFont('Arial', 10))
        self.space_label.setText("space:")
        self.space_label.adjustSize()
        self.space_label.move(100, 150)

        self.uspace_label = QtWidgets.QLabel(self)
        self.uspace_label.setFont(QFont('Arial', 10))
        self.uspace_label.setText("used space:")
        self.uspace_label.adjustSize()
        self.uspace_label.move(100, 200)

        self.ID_label = QtWidgets.QLabel(self)
        self.ID_label.setFont(QFont('Arial', 10))
        self.ID_label.setText("Driver ID to remove:")
        self.ID_label.adjustSize()
        self.ID_label.move(100, 300)

        self.err_label = QtWidgets.QLabel(self)
        self.err_label.setFont(QFont('Arial', 10))
        self.err_label.setText("")
        self.err_label.adjustSize()
        self.err_label.move(50, 450)


        # specific values

        self.RID = QtWidgets.QTextEdit(self)
        self.RID.move(230, 100)

        self.space = QtWidgets.QTextEdit(self)
        self.space.move(230, 150)

        self.uspace = QtWidgets.QTextEdit(self)
        self.uspace.move(230, 200)


        self.ID = QtWidgets.QTextEdit(self)
        self.ID.move(230, 300)

        # buttons to work with

        self.back_btt = QtWidgets.QPushButton(self)
        self.back_btt.setText("Back")
        self.back_btt.move(400, 0)
        self.back_btt.clicked.connect(self.back)

        self.insert_btt = QtWidgets.QPushButton(self)
        self.insert_btt.setText("Insert")
        self.insert_btt.move(400, 175)
        self.insert_btt.clicked.connect(self.insert)

        self.delete_btt = QtWidgets.QPushButton(self)
        self.delete_btt.setText("Remove")
        self.delete_btt.move(400, 300)
        self.delete_btt.clicked.connect(self.delete)

    def back(self):
        self.hide()
        if win.TOGGLE:
            win.sin.profile.show()
        else:
            win.sup.profile.show()

    def insert(self):
        # INSERTING VALUES AND UPDATING THE UI TABLE
        DATABASE.add_driver(self.RID.toPlainText(),
                           self.space.toPlainText(),
                           self.uspace.toPlainText())
        DATABASE.loadRoute(self.tableWidget)

    def delete(self):
        error = DATABASE.remove_driver(self.ID.toPlainText())
        if error:
            self.err_label.setText("driver has orders that are not complete!")
            self.err_label.adjustSize()
        else:
            self.err_label.setText("")
            self.err_label.adjustSize()




class OrderAlter(QMainWindow):
    def __init__(self):
        super(OrderAlter, self).__init__()
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Profile")
        self.initUI()

    def initUI(self):
        # labels
        self.title = QtWidgets.QLabel(self)
        self.title.setFont(QFont('Arial', 20))
        self.title.setText("Complete Orders")
        self.title.adjustSize()
        self.title.move(150, 50)

        # table of orders

        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 50)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnWidth(3, 50)

        self.tableWidget.resize(350, 200)
        self.tableWidget.move(50, 250)
        DATABASE.loadallOrders(self.tableWidget)

        self.ID_label = QtWidgets.QLabel(self)
        self.ID_label.setFont(QFont('Arial', 10))
        self.ID_label.setText("Order ID to complete:")
        self.ID_label.adjustSize()
        self.ID_label.move(100, 200)

        self.err_label = QtWidgets.QLabel(self)
        self.err_label.setFont(QFont('Arial', 10))
        self.err_label.setText("")
        self.err_label.adjustSize()
        self.err_label.move(50, 450)


        # specific values

        self.ID = QtWidgets.QTextEdit(self)
        self.ID.move(230, 200)

        # buttons to work with

        self.back_btt = QtWidgets.QPushButton(self)
        self.back_btt.setText("Back")
        self.back_btt.move(400, 0)
        self.back_btt.clicked.connect(self.back)

        self.delete_btt = QtWidgets.QPushButton(self)
        self.delete_btt.setText("Complete")
        self.delete_btt.move(400, 200)
        self.delete_btt.clicked.connect(self.delete)

    def back(self):
        self.hide()
        if win.TOGGLE:
            win.sin.profile.show()
        else:
            win.sup.profile.show()

    def delete(self):
        DATABASE.remove_order(self.ID.toPlainText())

def main():
    win.show()
    sys.exit(app.exec_())

main()
