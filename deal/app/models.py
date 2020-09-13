
from django.utils.timezone import now
from djongo import models
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
    '''def loc_id(self):
       return self.id+100'''
    
    def __str__(self):
        return self.location

class Vendor(models.Model):
    pass

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
    device_token=models.CharField(max_length=100,blank=True,default='')
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

'''class User_Interest(models.Model):
    
    userCD=models.ForeignKey(User,on_delete=models.CASCADE)
    #category_id=models.ForeignKey(Interest,on_delete=models.CASCADE)
    choice=Interest.objects.all()#.values('category_id')
    ch_list=[]
    for ch in choice:
        ch_list.append([ch.category_name,ch.category_name])
    interest=MultiSelectField(choices=ch_list,min_choices=3,default='',blank=True)
    #print(type(interest))
    
    def __str__(self):
        return str(self.interest)'''


