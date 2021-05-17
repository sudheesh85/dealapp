import datetime
from django.db import models
#from django.db.models import JSONField
from django.contrib.postgres.fields import ArrayField ,JSONField
from django.utils.timezone import now
#from djongo import models
from django.utils.crypto import get_random_string
from .userid_gen import uid,otp
from .passwd_gen import tok
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
DEAL_STATUS=(
    ('ACTIVE','ACTIVE'),
    ('CONFIRMED','CONFIRMED'),
    ('ON HOLD','ON HOLD'),
    ('DEACTIVATE','DEACTIVATE')
)
DEVICE_TYPE=(
    ('{ANDROID}','{ANDROID}'),
    ('{iOS}','{iOS}')
)
AGE_LIMIT = (
    ('18-30','18-30'),
    ('31-40','31-40'),
    ('41-50','41-50'),
    ('51-60','51-60'),
    ('61-Above','61-Above')
)
METHOD = (
    ('Recieved','Recieved'),
    ('Send','Send'),
    ('Compliment','Compliment')
)
VENDOR_STATUS = (
    ('Active','Active'),
    ('Approval Pending','Approval Pending'),
    ('Deactivated','Deactivated')
)
PROVIDER_TYPE = (
    ('Vendor','Vendor'),
    ('Admin','Admin')
)
DEAL_PREFRENCE = (
    (1,'All in the City'),
    (2,'To Followers'),
    (3,'Those who already visited my shop'),
    (4,'Those who purchased above Rs.500')
)

class Interest(models.Model):
    
    category_id=models.IntegerField(default=100,unique=True)
    category_name=models.CharField(max_length=50,null=True,unique=True)
    image_title = models.CharField(max_length=50,null=True)
    category_img = models.ImageField(upload_to='yesdeal/media/gallory',blank=True, null=True)
    #@property
    #def category_id(self):
       #return self.id+100
    
    def __str__(self):
        return self.category_name
class Region(models.Model):
    city = models.CharField(max_length=50,null=True)
    def __str__(self):
        return self.city
class Area(models.Model):
    name = models.CharField(max_length=200,null=True)
    city = models.ForeignKey(to=Region, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
class Deal_scratch(models.Model):
    scratch_logo = models.ImageField(upload_to='yesdeal/media/logo',blank=True, null=True)

'''class Product(models.Model):
    #vendor_name = models.ForeignKey(Vendor,on_delete=models.CASCADE,null=True)
    product_cd = models.CharField(max_length=6,null=True,blank=True)
    product_name = models.CharField(max_length=200,null=True)
    product_category = models.ForeignKey(to=Interest, on_delete=models.CASCADE)
    item_price=models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    def save(self, *args, **kwargs):
           ## This to check if it creates a new or updates an old instance
           if self.pk is None:
              self.product_cd = uid.make_id()
           super(Product, self).save(*args, **kwargs)
    def __str__(self):
        return self.product_name'''

'''class ServiceLoc(models.Model):
    loc_id=models.IntegerField()
    location=models.CharField(max_length=50,null=True)
    @property
    def loc_id(self):
        return self.id+100
    
    def __str__(self):
        return self.location'''

class Vendor(models.Model):
    #vendor_id=models.IntegerField(default=1000,unique=True)
    user_name = models.CharField(max_length=20,null=True,unique=True,blank=True)
    password = models.CharField(max_length=20,null=True,blank=True)
    user_pin = models.CharField(max_length=4,null=True,blank=True)
    user_pin_verified = models.BooleanField(null=True,default=False)
    vendor_token = models.CharField(max_length=16,null=True,blank=True)
    vendor_cd=models.CharField(max_length=6,null=True,unique=True,blank=True)
    vendor_logo = models.ImageField(upload_to='document',blank=True, null=True)
    vendor_name=models.CharField(max_length=200,blank=True)
    phone_number=models.CharField(max_length=10,unique=True, blank=True)
    description=models.TextField(blank=True)
    vendor_street = models.CharField(max_length=100,blank=True)
    vendor_city = models.CharField(max_length=100,blank=True)
    vendor_pin_code = models.CharField(max_length=100,blank=True)
    vendor_img = models.ImageField(upload_to='yesdeal/media/gallory',blank=True, null=True)
    #vendor_img2 = models.ImageField(upload_to='yesdeal/media/vendor',blank=True, null=True)
    #vendor_img3 = models.ImageField(upload_to='yesdeal/media/vendor',blank=True, null=True)
    #vendor_img4 = models.ImageField(upload_to='yesdeal/media/vendor',blank=True, null=True)
    #vendor_img5 = models.ImageField(upload_to='yesdeal/media/vendor',blank=True, null=True)
    #product_name = models.ForeignKey(to=Product, on_delete=models.CASCADE,null=True)
    totalDeals=models.CharField(max_length=5,blank=True)
    totalActiveDeals=models.CharField(max_length=5,blank=True)
    vendor_email = models.CharField(max_length=100,blank=True)
    vendor_whatsapp = models.CharField(max_length=10,null=True, blank=True)
    vendor_webpage = models.URLField(max_length=200, blank=True,null=True)
    vendor_fb_link = models.URLField(max_length=200, blank=True,null=True)
    vendor_twitter_link = models.URLField(max_length=200, blank=True,null=True)
    vendor_status = models.TextField(choices=VENDOR_STATUS, default='', blank=True)
    
    def save(self, *args, **kwargs):
           ## This to check if it creates a new or updates an old instance
           if self.pk is None:
              self.vendor_cd = uid.make_id()
           super(Vendor, self).save(*args, **kwargs)
    #@property
    #def vendor_id(self):
       #return self.id+100

    def __str__(self):
        return self.vendor_name

class Product(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE,null=True)
    product_cd = models.CharField(max_length=6,null=True,blank=True)
    product_name = models.CharField(max_length=200,null=True)
    product_category = models.ForeignKey(to=Interest, on_delete=models.CASCADE)
    item_price=models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    def save(self, *args, **kwargs):
           ## This to check if it creates a new or updates an old instance
           if self.pk is None:
              self.product_cd = uid.make_id()
           super(Product, self).save(*args, **kwargs)
    def __str__(self):
        return self.product_name
#class Vendor_login(models.Model):
    #user_name = models.CharField(max_length=20,null=True,unique=True,blank=True)
    #password = models.CharField(max_length=20,null=True,blank=True)
    #vendor_token = models.CharField(max_length=16,null=True,blank=True)
    

    #def __str__(self):
        #return self.userName


'''class Deal_img_category(models.Model):
    img_title = models.CharField(max_length=50,null=True)
    product_name = models.ForeignKey(to=Product, on_delete=models.CASCADE,null=True)
    img_category = models.ForeignKey(to=Interest, on_delete=models.CASCADE)
    deal_img = models.ImageField(upload_to='yesdeal/media/deal',blank=True, null=True)

    def __str__(self):
        return self.deal_img
class Deal_img_vendor(models.Model):
    img_title = models.CharField(max_length=50,null=True)
    vendor_name = models.ForeignKey(Vendor,on_delete=models.CASCADE,null=True)
    product_name = models.ForeignKey(to=Product, on_delete=models.CASCADE,null=True)
    deal_img = models.ImageField(upload_to='yesdeal/media/vendor',blank=True, null=True)

    def __str__(self):
        return self.deal_img'''

class Images(models.Model):
    img_title = models.CharField(max_length=50,null=True)
    category = models.ForeignKey(Interest,on_delete=models.CASCADE,blank=True,null=True)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(upload_to='yesdeal/media/gallory',blank=True, null=True)
    provider = models.TextField(choices=PROVIDER_TYPE, default='', blank=True)
    class Meta:
        verbose_name = "Deal_Images"
        verbose_name_plural = "Deal_Images"
    def __str__(self):
        return self.img_title

class User(models.Model):
    #photo = models.ImageField(upload_to='document',blank=True, null=True)
    #userID=models.IntegerField()
    userCD=models.CharField(max_length=6,null=True,unique=True,blank=True)
    #password = models.CharField(max_length=8,null=True,blank=True)
    user_token = models.CharField(max_length=16,null=True,blank=True)
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
    #no_of_coins = models.FloatField(blank=True,default=0.0)
    created_at = models.DateTimeField(blank=True,auto_now_add=True)
    service_area = models.ForeignKey(Area,on_delete=models.CASCADE,null=True)
    #all_loc=ServiceLoc.objects.all()
    #loc_list=[]
    #for loc in all_loc:
        #loc_list.append([loc.location,loc.location])
    #serviceLoc=models.TextField(choices=loc_list,default='',blank=True)
    #vendor=Vendor.objects.all()
    #vlist=[]
    #for vndr in vendor:
        #vlist.append([vndr.vendor_name,vndr.vendor_name])
    #interested_vendors=MultiSelectField(choices=vlist,default='',blank=True)
    #vendor_is_followed=models.NullBooleanField(default=False)
    def save(self, *args, **kwargs):
           ## This to check if it creates a new or updates an old instance
           if self.pk is None:
              #self.userCD = uid.make_id()
              #self.password = pwd.get_password()
              #self.user_token = tok.get_token()
              self.otp=otp.get_otp()
              self.otp_exp_time=otp.get_exp_time()
           super(User, self).save(*args, **kwargs)
    @property
    def userID(self):
       return self.id
    
    def __str__(self):
        return self.name or ''
# Create your models here.

class Shared_coin_history(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE,null=True)
    numberOfRedeemableCoins = models.IntegerField(default=0)
    #from_user = models.CharField(max_length=12,blank=True)
    num_of_comp_coins = models.IntegerField(default=0)
    num_of_shared_coins = models.IntegerField(default=0)
    shared_at = models.DateTimeField(blank=True,default=now)
    shared_method = models.TextField(choices=METHOD, default='', blank=True)
    def __str__(self):
        return str(self.numberOfRedeemableCoins)

class User_Vendor(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE,null=True)
    user_is_followed=models.BooleanField(null=True,default=False)
    #numberOfRedeemableCoins=models.CharField(max_length=5,blank=True)
    numberOfRedeemableCoins = models.ForeignKey(Shared_coin_history,on_delete = models.CASCADE,default=0)
    totalCollectedDeals=models.CharField(max_length=5,blank=True)

    def __str__(self):
        return str(self.user) or ''


class Device(models.Model):
    userCD=models.ForeignKey(User,on_delete=models.CASCADE)
    device=JSONField()
    #user_lat = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    #user_long = models.DecimalField(max_digits=9, decimal_places=6,null=True)

    def __str__(self):
        return str(self.userCD)
class Global(models.Model):
    EXP_TIME=models.IntegerField(default=0)

    def __str__(self):
        return str(self.EXP_TIME)
#class sample(models.Model):
    #userCD=models.ForeignKey(User,on_delete=models.CASCADE)
    #board=ArrayField(models.CharField(max_length=50,blank=True),default=list)

class Branch(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    #branch_id = models.IntegerField()
    branch_name = models.CharField(max_length=500,blank=True)
    branch_street = models.CharField(max_length=100,blank=True)
    branch_city = models.CharField(max_length=100,blank=True)
    branch_pin = models.CharField(max_length=100,blank=True)
    branch_contact = models.CharField(max_length=100,blank=True)
    #@property
    #def branch_id(self):
       #return self.id+1000
    def __str__(self):
        return self.branch_name

class Yesdeal(models.Model):
    DEAL_PREFERENCE = (
        ('All in the City','All in the City'),
        ('To Followers','To Followers'),
        ('Those who already visited my shop','Those who already visited my shop'),
        ('Those who purchased above Rs.500','Those who purchased above Rs.500')
    )
    deal_id = models.CharField(max_length=6,null=True,unique=True,blank=True)
    deal_vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE,null=True)
    deal_title=models.CharField(max_length=500,null=True)
    deal_desc= models.TextField(blank=True)
    deal_org_price=models.DecimalField(max_digits=10, decimal_places=2)
    deal_spl_price=models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    deal_offer_percentage = models.DecimalField(max_digits=5,decimal_places=2,default=0.0)
    deal_srvc_city = models.ForeignKey(Region,on_delete=models.CASCADE,null=True)
    deal_srvc_area = models.ManyToManyField(Area, verbose_name="service_area")
    deal_category = models.ForeignKey(Interest, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    #deal_img = models.ForeignKey(Interest, on_delete=models.CASCADE)
    deal_img = models.ImageField(upload_to='yesdeal/media/gallory',blank=True, null=True)
    #deal_img2 = models.ImageField(upload_to='document',blank=True, null=True)
    #deal_img3 = models.ImageField(upload_to='document',blank=True, null=True)
    #deal_img4 = models.ImageField(upload_to='document',blank=True, null=True)
    #deal_img5 = models.ImageField(upload_to='document',blank=True, null=True)
    deal_start_time = models.DateTimeField(blank=True,default=now)
    deal_end_time = models.DateTimeField(blank=True,default=now)
    deal_avail_max = models.IntegerField(default=0)
    deal_collected_till = models.IntegerField(default=0)
    deal_category_on_age = models.TextField(choices = AGE_LIMIT,default='',blank=True)
    deal_category_on_gender = models.TextField(choices=GENDER_STATUS, default='', blank=True)
    #deal_QRCode = models.CharField(max_length=20, unique=True,blank=True, null=True)
    deal_preference = models.TextField(null=True,help_text="It's a good manners to write it")
    Alloted_deal_per_coupon = models.IntegerField(default=0)
    #deal_available_branch = models.ForeignKey(Branch,on_delete=models.CASCADE,null=True)
    deal_available_branch = models.ManyToManyField(Branch, verbose_name="vendor_branches")
    deal_status = models.TextField(choices=DEAL_STATUS, default='', blank=True)
    def save(self,*args,**kwargs):
        if self.pk is None:
            self.deal_id = uid.make_id()
            if self.deal_offer_percentage:
                self.deal_spl_price = self.deal_org_price - (self.deal_org_price * (self.deal_offer_percentage/100))
            else:
                self.deal_offer_percentage = ((self.deal_org_price - self.deal_spl_price) / self.deal_org_price) * 100
        super(Yesdeal, self).save(*args, **kwargs)


    #@property
    #def deal_id(self):
       #return self.id+10000
    def __str__(self):
        return self.deal_title

class User_Deal(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    deal = models.ForeignKey(Yesdeal,on_delete=models.CASCADE,null=True)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE,null=True)
    is_collected = models.BooleanField(null=True,default=False)
    collected_at = models.DateTimeField(blank=True,default=now)
    QRCode = models.CharField(max_length=20, unique=True,blank=True, null=True)
    is_deal_confirmed = models.BooleanField(null=True,default=False)
    is_deal_redeemed = models.BooleanField(null=True,default=False)
    deal_quantity = models.IntegerField(default=0)
    user_wah_points = models.IntegerField(default=0)
    deal_scratch_status = models.BooleanField(null=True,default=False)

    def __str__(self):
        return str(self.user)


