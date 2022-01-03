# imports for the interface
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import os

# imports for SQL functionality
import mysql.connector

# some control values for this thing to check if the user is signed in + to see if the profile is found in the
# database + to see if the password matches the one in the database + to see if the user is an admin
signedIn = True
validProfile = True
validPass = True
admin = False


# surface level information about the user of the database

class DB():
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

            if found == 0:
                # empty space found
                self.command.execute(
                    "INSERT INTO users(FirstName, LastName, Email, Phone, City, Street, SNumber, UPassword) "
                    "VALUES(" +
                    "'" + user.first_name + "'," +
                    "'" + user.last_name + "'," +
                    "'" + user.email + "'," +
                    "'" + user.phone + "'," +
                    "'" + user.city + "'," +
                    "'" + user.street + "'," +
                    "'" + user.number + "'," +
                    "'" + user.password + "')")
                self.db.commit()
                return 1
            else:
                # there is no empty space there
                return 0
        else:
            return 0

    def select_existing_user(self, user, email, password):
        self.command.execute(
            "SELECT u.FirstName , u.LastName, u.Email, u.Phone, a.City, a.Street, a.Number, u.UPassword FROM users u, address a WHERE u.userID = a.userID AND u.Email LIKE '" + email + "';")

        result = self.command.fetchone()
        self.db.commit()

        user.add(
            result["FirstName"],
            result["LastName"],
            result["Email"],
            result["Phone"],
            result["City"],
            result["Street"],
            result["Number"],
            result["UPassword"])


# global database for simplicity
DATABASE = DB()

class User():
    def __init__(self):

        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.phone = ""
        self.city = ""
        self.street = ""
        self.number = ""
        self.password = ""

        # grade - to make a distinction between regular user | manager

        # regular user should be able to:
        # create orders
        # view his own orders

        # manager should be able to:
        # create routes for the drivers
        # remove or mark orders as completed for each user
        #

        self.grade = ""

    def add(self, fname_in, lname_in, email_in, phone_in, city_in, street_in, number_in, password_in):

        self.first_name = fname_in
        self.last_name = lname_in
        self.email = email_in
        self.phone = phone_in
        self.city = city_in
        self.street = street_in
        self.number = number_in
        self.password = password_in


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Delivery Service Home")
        self.initUI()
        # user is defined here for simplicity
        self.user = User()

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
        self.title.setText("Delivery Services")
        self.title.adjustSize()
        self.title.move(150, 160)

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

    def signIn(self):
        self.sin = SignIN()
        self.sin.show()
        self.hide()

    def routes(self):
        self.rou = Routes()
        self.hide()
        self.rou.show()


# global main window for easyer access to it and such
app = QApplication(sys.argv)
win = MainWindow()


class NewOrder(QMainWindow):
    def __init__(self):
        super(NewOrder, self).__init__()
        self.setGeometry(200, 200, 1000, 800)
        self.setWindowTitle("New Order")
        self.initUI()

    def initUI(self):
        # oras
        # strada
        # numar

        # greutate colet

        self.title = QtWidgets.QLabel(self)
        self.title.setFont(QFont('Arial', 20))
        self.title.setText("New Delivery Order")
        self.title.adjustSize()
        self.title.move(350, 20)

        # Pick UP information

        self.tab1 = QtWidgets.QLabel(self)
        self.tab1.setText("Pick UP")
        self.tab1.move(150, 100)

        self.city1 = QtWidgets.QLabel(self)
        self.city1.setText("City")
        self.city1.move(100, 150)

        self.street1 = QtWidgets.QLabel(self)
        self.street1.setText("Street")
        self.street1.move(100, 200)

        self.number1 = QtWidgets.QLabel(self)
        self.number1.setText("Number")
        self.number1.move(100, 250)

        self.city1_text = QtWidgets.QTextEdit(self)
        self.city1_text.move(150, 150)

        self.street1_text = QtWidgets.QTextEdit(self)
        self.street1_text.move(150, 200)

        self.number1_text = QtWidgets.QTextEdit(self)
        self.number1_text.move(150, 250)

        # Drop OFF information

        self.tab2 = QtWidgets.QLabel(self)
        self.tab2.setText("Drop OFF")
        self.tab2.move(650, 100)

        self.city2 = QtWidgets.QLabel(self)
        self.city2.setText("City")
        self.city2.move(600, 150)

        self.street2 = QtWidgets.QLabel(self)
        self.street2.setText("Street")
        self.street2.move(600, 200)

        self.number2 = QtWidgets.QLabel(self)
        self.number2.setText("Number")
        self.number2.move(600, 250)

        self.city2_text = QtWidgets.QTextEdit(self)
        self.city2_text.move(650, 150)

        self.street2_text = QtWidgets.QTextEdit(self)
        self.street2_text.move(650, 200)

        self.number2_text = QtWidgets.QTextEdit(self)
        self.number2_text.move(650, 250)

        # weight of the object
        self.weight = QtWidgets.QLabel(self)
        self.weight.setText("Weight")
        self.weight.move(350, 300)

        self.weight_text = QtWidgets.QTextEdit(self)
        self.weight_text.move(400, 300)

        # annotations

        self.details = QtWidgets.QLabel(self)
        self.details.setText("*Notes")
        self.details.move(350, 350)

        self.details_text = QtWidgets.QTextEdit(self)
        self.details_text.move(400, 350)

        # buttons and stuff
        self.back_btt = QtWidgets.QPushButton(self)
        self.back_btt.setText("Home")
        self.back_btt.move(900, 0)
        self.back_btt.clicked.connect(self.back)

        self.enter_btt = QtWidgets.QPushButton(self)
        self.enter_btt.setText("Place order")
        self.enter_btt.move(400, 400)
        self.enter_btt.clicked.connect(self.enter)

    def enter(self):
        # check for good pass and email in the database
        print("data introduced into database")

    def back(self):
        win.show()
        self.hide()


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
        win.user.add(
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
        DATABASE.select_user("Mickey", "Ionescu")
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
        self.setGeometry(200, 200, 1000, 800)
        self.setWindowTitle("Routes")
        self.initUI()

    def initUI(self):
        # labels
        self.title = QtWidgets.QLabel(self)
        self.title.setFont(QFont('Arial', 20))
        self.title.setText("Available Routes")
        self.title.adjustSize()
        self.title.move(350, 20)

        # buttons

        self.back_btt = QtWidgets.QPushButton(self)
        self.back_btt.setText("Home")
        self.back_btt.move(900, 0)
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

        # buttons

        self.back_btt = QtWidgets.QPushButton(self)
        self.back_btt.setText("Home")
        self.back_btt.move(400, 0)
        self.back_btt.clicked.connect(self.back)

        self.orders_btt = QtWidgets.QPushButton(self)
        self.orders_btt.setText("Your Orders")
        self.orders_btt.move(150, 300)
        self.orders_btt.clicked.connect(self.orders)

        self.neworder_btt = QtWidgets.QPushButton(self)
        self.neworder_btt.setText("NewOrder")
        self.neworder_btt.move(150, 350)
        self.neworder_btt.clicked.connect(self.newOrder)

        # profile biz

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
        print("here should be a list of the orders one placed")
        self.orders = Orders()
        self.orders.show()
        self.hide()

    def newOrder(self):

        if (signedIn):
            # proceed directly to the order
            self.newo = NewOrder()
            self.newo.show()
            self.hide()
        else:
            # sign in then proceed to order
            self.sin = SignIN()
            self.sin.show()
            self.hide()


class Orders(QMainWindow):
    def __init__(self):
        super(Orders, self).__init__()
        self.setGeometry(200, 200, 1000, 800)
        self.setWindowTitle("Profile")
        self.initUI()

    def initUI(self):
        # labels
        self.title = QtWidgets.QLabel(self)
        self.title.setFont(QFont('Arial', 20))
        self.title.setText("Your Orders")
        self.title.adjustSize()
        self.title.move(350, 100)


def main():
    win.show()
    sys.exit(app.exec_())


main()
