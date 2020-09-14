#from twilio.rest import TwilioRestClient
from twilio.rest import Client

class Message:
    def sendMsg(self,ph,otp):
# Your Account Sid and Auth Token from twilio.com/user/account
        account_sid = "12345"
        auth_token  = "xxxxx"
        #client = TwilioRestClient(account_sid, auth_token)
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body="Use this code for dealapp authentication:"+otp,
            to=ph,#"+17044503102",
            from_="+15089257246",
            #media_url="http://www.example.com/hearts.png"
            )
        print(message.sid)

sms=Message()