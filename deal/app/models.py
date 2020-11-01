
from django.db import models
from django.db.models import JSONField
from django.contrib.postgres.fields import ArrayField #,JSONField
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
    
    category_id=models.IntegerField(default=100,unique=True)
    category_name=models.CharField(max_length=50,null=True,unique=True)
    #@property
    #def category_id(self):
       #return self.id+100
    
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
    userCD=models.CharField(max_length=6,null=True,unique=True,blank=True)
    name = models.CharField(max_length=100,null=True)
    nick_name = models.CharField(max_length=100,null=True)
    #city = models.CharField(max_length=50,default="Kochi")
    email = models.CharField(max_length=100, null=True,blank=True)
    gender = models.TextField(choices=GENDER_STATUS, default='', blank=True)
    dob=models.DateField(null=True)
    mobile = models.CharField(max_length=12,unique=True, blank=True)
    otp=models.CharField(max_length=6,null=True,blank=True)
    otp_exp_time=models.DateTimeField(blank=True,default=now)
    is_otp_verified=models.BooleanField(null=True,default=False)
    #device_token=models.CharField(max_length=100,blank=True,default='')
    #choice=Interest.objects.all()#.values('category_name')
    #ch_list=[]
    #for ch in choice:
        #ch_list.append([ch.category_name,ch.category_name])
    #interest=MultiSelectField(choices=ch_list,min_choices=3,default='',blank=True)  
    #interest=ArrayField(models.CharField(max_length=100,blank=True),null=True,size=50,default=list)
    interest = models.ManyToManyField(Interest, verbose_name="user_interest")
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
    device=JSONField()
  

    def __str__(self):
        return str(self.userCD)
class Global(models.Model):
    EXP_TIME=models.IntegerField(default=0)

    def __str__(self):
        return str(self.EXP_TIME)
class sample(models.Model):
    userCD=models.ForeignKey(User,on_delete=models.CASCADE)
    board=ArrayField(models.CharField(max_length=50,blank=True),default=list)

class Branch(models.Model):
    vendor_id = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    branch_id = models.IntegerField()
    branch_name = models.CharField(max_length=500,blank=True)
    branch_street = models.CharField(max_length=100,blank=True)
    branch_city = models.CharField(max_length=100,blank=True)
    brnach_pin = models.CharField(max_length=100,blank=True)
    branch_contact = models.CharField(max_length=100,blank=True)
    @property
    def branch_id(self):
       return self.id+1000
    def __str__(self):
        return self.branch_name

class Yesdeal(models.Model):
    deal_id = models.IntegerField()
    deal_title=models.CharField(max_length=500,null=True)
    deal_desc= models.TextField(blank=True)
    deal_org_price=models.DecimalField(max_digits=10, decimal_places=2)
    deal_spl_price=models.DecimalField(max_digits=10, decimal_places=2)
    deal_srvc_loc = models.CharField(max_length=100,blank=True,null=True)
    deal_category = models.ForeignKey(Interest, on_delete=models.CASCADE)
    deal_img1 = models.ImageField(upload_to='document',blank=True, null=True)
    deal_img2 = models.ImageField(upload_to='document',blank=True, null=True)
    deal_img3 = models.ImageField(upload_to='document',blank=True, null=True)
    deal_img4 = models.ImageField(upload_to='document',blank=True, null=True)
    deal_img5 = models.ImageField(upload_to='document',blank=True, null=True)
    deal_start_time = models.DateTimeField(blank=True,auto_now_add=True)
    deal_end_time = models.DateTimeField(blank=True,auto_now_add=True)
    deal_count = models.IntegerField(default=0)
    deal_vendor_name = models.CharField(max_length=200,blank=True)
    deal_available_branch = models.ForeignKey(Branch,on_delete=models.CASCADE,null=True)
    @property
    def deal_id(self):
       return self.id+10000
    def __str__(self):
        return self.deal_title



