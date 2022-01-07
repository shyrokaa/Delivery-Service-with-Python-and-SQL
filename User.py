class User:
    def __init__(self):
        self.uid = ""
        self.type = 0
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

    def add(self, uid_in,utype_in, fname_in, lname_in, email_in, phone_in, city_in, street_in, number_in, password_in):
        self.uid = uid_in
        self.type = utype_in
        self.first_name = fname_in
        self.last_name = lname_in
        self.email = email_in
        self.phone = phone_in
        self.city = city_in
        self.street = street_in
        self.number = number_in
        self.password = password_in