# this class is meant to make it easier for me to parse commands to the database
# since it stores all the data I need in a place
class Order:
    def __init__(self):
        self.userID = 0
        self.driverID = 0
        self.City = ""
        self.Street = ""
        self.Number = ""
        self.weight = ""

    def add_base_data(self, userID_in, City_in, Street_in, Number_in):
        self.userID = userID_in
        self.City = City_in
        self.Street = Street_in
        self.Number = Number_in

    def add_full_data(self, driverID_in):
        self.driverID = driverID_in
