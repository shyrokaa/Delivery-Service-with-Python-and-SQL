from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

# some control values for this thing
signedIn = True


# surface level information about the user of the database
class User():
    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.phone = ""
        self.address = ""
        self.password = ""


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(200, 200, 1000, 800)
        self.setWindowTitle("Tema BD")
        self.initUI()

    def initUI(self):

        # labels
        self.title = QtWidgets.QLabel(self)
        self.title.setFont(QFont('Arial', 20))
        self.title.setText("Delivery services")
        self.title.adjustSize()
        self.title.move(350, 20)

        # buttons and such
        # new user
        self.newaccount_btt = QtWidgets.QPushButton(self)
        self.newaccount_btt.setText("Sign up")
        self.newaccount_btt.move(800, 0)
        self.newaccount_btt.clicked.connect(self.newAccount)

        # existing user
        self.signIn_btt = QtWidgets.QPushButton(self)
        self.signIn_btt.setText("Sign In")
        self.signIn_btt.move(900, 0)
        self.signIn_btt.clicked.connect(self.signIn)

        # new order
        self.neworder_btt = QtWidgets.QPushButton(self)
        self.neworder_btt.setText("NewOrder")
        self.neworder_btt.move(400, 150)
        self.neworder_btt.clicked.connect(self.newOrder)

        # routes

        self.routes_btt = QtWidgets.QPushButton(self)
        self.routes_btt.setText("Routes")
        self.routes_btt.move(400, 200)
        self.routes_btt.clicked.connect(self.routes)

    def newAccount(self):
        self.sup = SignUP()
        self.hide()
        self.sup.show()

    def signIn(self):
        self.sin = SignIN()
        self.sin.show()
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
        self.setGeometry(200, 200, 1000, 800)
        self.setWindowTitle("New Order")
        self.initUI()

    def initUI(self):
        self.title = QtWidgets.QLabel(self)
        self.title.setFont(QFont('Arial', 20))
        self.title.setText("Sign In")
        self.title.adjustSize()
        self.title.move(450, 20)

        self.email = QtWidgets.QLabel(self)
        self.email.setText("Email")
        self.email.move(450, 250)

        self.password = QtWidgets.QLabel(self)
        self.password.setText("Password")
        self.password.move(450, 300)

        self.enter_btt = QtWidgets.QPushButton(self)
        self.enter_btt.setText("Sign in")
        self.enter_btt.move(500, 500)
        self.enter_btt.clicked.connect(self.enter)

        self.back_btt = QtWidgets.QPushButton(self)
        self.back_btt.setText("Home")
        self.back_btt.move(900, 0)
        self.back_btt.clicked.connect(self.back)

        self.email_text = QtWidgets.QTextEdit(self)
        self.email_text.move(550, 250)

        self.password_text = QtWidgets.QTextEdit(self)
        self.password_text.move(550, 300)

    def enter(self):
        # check for good pass and email in the database
        print("data introduced into database")

    def back(self):
        win.show()
        self.hide()


class SignUP(QMainWindow):
    def __init__(self):
        super(SignUP, self).__init__()
        self.setGeometry(200, 200, 1000, 800)
        self.setWindowTitle("Sign Up")
        self.initUI()

    def initUI(self):
        # labels

        self.title = QtWidgets.QLabel(self)
        self.title.setFont(QFont('Arial', 20))
        self.title.setText("Sign Up")
        self.title.adjustSize()
        self.title.move(450, 20)


        self.fname = QtWidgets.QLabel(self)
        self.fname.setText("First Name")
        self.fname.move(450, 150)

        self.lname = QtWidgets.QLabel(self)
        self.lname.setText("Last Name")
        self.lname.move(450, 200)

        self.email = QtWidgets.QLabel(self)
        self.email.setText("Email")
        self.email.move(450, 250)

        self.phone = QtWidgets.QLabel(self)
        self.phone.setText("Phone Number")
        self.phone.move(450, 300)

        self.address = QtWidgets.QLabel(self)
        self.address.setText("Address")
        self.address.move(450, 350)

        self.password = QtWidgets.QLabel(self)
        self.password.setText("Password")
        self.password.move(450, 400)

        # buttons

        # Sign Up button, obvioous reasons

        self.enter_btt = QtWidgets.QPushButton(self)
        self.enter_btt.setText("Sign up")
        self.enter_btt.move(500, 500)
        self.enter_btt.clicked.connect(self.enter)

        # return to main window for more information

        self.back_btt = QtWidgets.QPushButton(self)
        self.back_btt.setText("Home")
        self.back_btt.move(900, 0)
        self.back_btt.clicked.connect(self.back)

        # text boxes for information to introduce into the database

        self.fname_text = QtWidgets.QTextEdit(self)
        self.fname_text.move(550, 150)

        self.lname_text = QtWidgets.QTextEdit(self)
        self.lname_text.move(550, 200)

        self.email_text = QtWidgets.QTextEdit(self)
        self.email_text.move(550, 250)

        self.phone_text = QtWidgets.QTextEdit(self)
        self.phone_text.move(550, 300)

        self.address_text = QtWidgets.QTextEdit(self)
        self.address_text.move(550, 350)

        self.password_text = QtWidgets.QTextEdit(self)
        self.password_text.move(550, 400)

    def enter(self):
        print("data introduced into database")
        # checks for information validity for insertion and such by doing a select and seeing if email is already used
        # i will say its true for now coz im a lazy fuck

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

def main():
    win.show()
    sys.exit(app.exec_())

main()
