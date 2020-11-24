import random
import string

class tokenGenerator:
    def get_token(self):
        letters_and_digits = string.ascii_letters + string.digits
        token = ''.join((random.choice(letters_and_digits) for i in range(8)))
        return token
    #print("Random alphanumeric String is:", result_str)
tok = tokenGenerator()


#get_random_alphanumeric_string(8)
#get_random_alphanumeric_string(8)