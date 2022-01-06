# this class is meant to make it easier for me to parse commands to the database
# since it stores all the data I need in a place
class Order:

    def __init__(self):
        self.name = ""
        self.driverID = 0
        self.city = ""
        self.street = ""
        self.number = ""
        self.weight = ""

    def add_base_data(self, name_in, City_in, Street_in, Number_in, weight_in):
        self.name = name_in
        self.city = City_in
        self.street = Street_in
        self.number = Number_in
        self.weight = weight_in
