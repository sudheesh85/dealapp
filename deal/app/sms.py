#from twilio.rest import TwilioRestClient
from twilio.rest import Client

class Message:
    def sendMsg(self,ph,otp):
# Your Account Sid and Auth Token from twilio.com/user/account
        account_sid = "AC5c5132ae7e3856c21722097bc6af6873"
        auth_token  = "ee19e242b9694edeb8e701a7854d7e0a"
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