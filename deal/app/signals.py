from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import User


@receiver(post_save, sender=User)
def my_handler(sender, **kwargs):
    print("saved successfully")