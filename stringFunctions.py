# checks if the mail has a specific format
def emailFormat(input_string):
    mail_list = ['@gmail.com', '@yahoo.com', '@gmail.ro','@yahoo.ro']
    return list(filter(input_string.endswith, mail_list)) != []

