import random
import string

class tokenGenerator:
    def get_token(self):
        letters_and_digits = string.ascii_letters + string.digits
        token = ''.join((random.choice(letters_and_digits) for i in range(16)))
        return token
    #print("Random alphanumeric String is:", result_str)
tok = tokenGenerator()

class qrcodeGenerator:
    def qrcode(self,usercd,dealid):
        return usercd[:3] + dealid[:3]
qr = qrcodeGenerator()


#get_random_alphanumeric_string(8)
#get_random_alphanumeric_string(8)