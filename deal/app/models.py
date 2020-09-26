
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.timezone import now
#from djongo import models
from django.utils.crypto import get_random_string
from .userid_gen import uid,otp
from django import forms
from multiselectfield import MultiSelectField
from django.db.models.signals import post_save
from django.dispatch import receiver


GENDER_STATUS = (
    ('Male','Male'),
    ('Female','Female')
)
USER_STATUS= (
    ('ACTIVE','ACTIVE'),
    ('INACTIVE','INACTIVE'),
    ('SUSPENDED','SUSPENDED')
)
DEVICE_TYPE=(
    ('{ANDROID}','{ANDROID}'),
    ('{iOS}','{iOS}')
)

class Interest(models.Model):
    
    category_id=models.IntegerField()
    category_name=models.CharField(max_length=50,null=True)
    @property
    def category_id(self):
       return self.id+100
    
    def __str__(self):
        return self.category_name
class ServiceLoc(models.Model):
    loc_id=models.IntegerField()
    location=models.CharField(max_length=50,null=True)
    @property
    def loc_id(self):
        return self.id+100
    
    def __str__(self):
        return self.location

class Vendor(models.Model):
    vendor_id=models.IntegerField()
    vendor_name=models.CharField(max_length=200,blank=True)
    phone_number=models.CharField(max_length=10,unique=True, blank=True)
    description=models.TextField(blank=True)
    totalDeals=models.CharField(max_length=5,blank=True)
    totalActiveDeals=models.CharField(max_length=5,blank=True)
    numberOfRedeemableCoins=models.CharField(max_length=5,blank=True)
    totalCollectedDeals=models.CharField(max_length=5,blank=True)
    
    @property
    def vendor_id(self):
       return self.id+100

    def __str__(self):
        return self.vendor_name


class User(models.Model):
    #photo = models.ImageField(upload_to='document',blank=True, null=True)
    #userID=models.IntegerField()
    userCD=models.CharField(max_length=6,blank=True,unique=True)
    name = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100)
    #city = models.CharField(max_length=50,default="Kochi")
    email = models.CharField(max_length=100, blank=True)
    gender = models.TextField(choices=GENDER_STATUS, default='', blank=True)
    dob=models.DateField(null=True)
    mobile = models.BigIntegerField(unique=True, blank=True)
    otp=models.CharField(max_length=6,null=True,blank=True)
    otp_exp_time=models.DateTimeField(blank=True,default=now)
    is_otp_verified=models.NullBooleanField(default=False)
    #device_token=models.CharField(max_length=100,blank=True,default='')
    choice=Interest.objects.all()#.values('category_name')
    ch_list=[]
    for ch in choice:
        ch_list.append([ch.category_name,ch.category_name])
    interest=MultiSelectField(choices=ch_list,min_choices=3,default='',blank=True)  
    status = models.TextField(choices=USER_STATUS, default='', blank=True)
    no_of_coins = models.FloatField(blank=True,default=0.0)
    created_at = models.DateTimeField(blank=True,auto_now_add=True)
    all_loc=ServiceLoc.objects.all()
    loc_list=[]
    for loc in all_loc:
        loc_list.append([loc.location,loc.location])
    serviceLoc=models.TextField(choices=loc_list,default='',blank=True)
    vendor=Vendor.objects.all()
    vlist=[]
    for vndr in vendor:
        vlist.append([vndr.vendor_name,vndr.vendor_name])
    interested_vendors=MultiSelectField(choices=vlist,default='',blank=True)
    #vendor_is_followed=models.NullBooleanField(default=False)
    def save(self, *args, **kwargs):
           ## This to check if it creates a new or updates an old instance
           if self.pk is None:
              self.userCD = uid.make_id()
              self.otp=otp.get_otp()
              self.otp_exp_time=otp.get_exp_time()
           super(User, self).save(*args, **kwargs)
    @property
    def userID(self):
       return self.id
    
    def __str__(self):
        return self.name
# Create your models here.

class Device(models.Model):
    userCD=models.ForeignKey(User,on_delete=models.CASCADE)
    device_token=ArrayField(models.CharField(max_length=256),blank=True)
    device_type=ArrayField(models.TextField(choices=DEVICE_TYPE,default=''))
    device_id=models.CharField(max_length=20,blank=True)

    def __str__(self):
        return str(self.userCD)


#class User_Interest(models.Model):
    
#    userCD=models.ForeignKey(User,on_delete=models.CASCADE)
    #category_id=models.ForeignKey(Interest,on_delete=models.CASCADE)
 #   choice=Interest.objects.all()#.values('category_id')
 #   ch_list=[]
 #   for ch in choice:
 #       ch_list.append([ch.category_name,ch.category_name])
 #   interest=MultiSelectField(choices=ch_list,min_choices=3,default='',blank=True)
 #   #print(type(interest))
    
 #   def __str__(self):
  #      return str(self.interest)'''


