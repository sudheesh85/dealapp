from pyfcm import FCMNotification

class Fcm:
    def send_notification(self,user_objects,title, message, data):
        #try:
            print(title)
            FCM_SERVER_KEY="AAAAlZQmY_k:APA91bH47xB6TaR-Z_UixO57Lne_ApLFGftyeP8Q7oAZTG-vb52Lb4PhTiQmZJ5jK-9vy4DfWhWw_fmxlCst4zLk80EeY4yiyRwunUl2qMfuxmxk6IWoE-X5uP6i9B6u2ABA_UuQusel"

            push_service = FCMNotification(api_key=FCM_SERVER_KEY)
            print(push_service)
            fcm_token = []
            #for obj in user_objects:
            fcm_token.append(user_objects.device_token)
            print(fcm_token)
            return push_service.notify_multiple_devices(
                registration_ids=fcm_token,message_title=title,
                message_body=message, data_message=data)
        #except:
            #print("not working")
FCM=Fcm()