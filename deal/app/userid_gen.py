from django.utils.crypto import get_random_string
from datetime import datetime as dt,timedelta
import pyotp
class RandomTokenGenerator:
    def make_id(self):
        return get_random_string(16)

uid = RandomTokenGenerator()

class GenerateOTP:
    def get_otp(self):
        totp=pyotp.TOTP('base32secret3232')
        return totp.now()
    def get_exp_time(self):
        now=dt.now()
        validity=30
        exp_time=now+timedelta(minutes=10)
        return exp_time

otp=GenerateOTP()