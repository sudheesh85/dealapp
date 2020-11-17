import random
import string

class passwdGenerator:
    def get_password(self):
        letters_and_digits = string.ascii_letters + string.digits
        password = ''.join((random.choice(letters_and_digits) for i in range(8)))
        return password
    #print("Random alphanumeric String is:", result_str)
pwd = passwdGenerator()

#get_random_alphanumeric_string(8)
#get_random_alphanumeric_string(8)