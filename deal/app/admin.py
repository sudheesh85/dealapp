from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from prettyjson import PrettyJSONWidget
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import path
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from .models import Interest,User,Vendor,Device,Global,Yesdeal,Branch,User_Vendor,User_Deal,Region,Area,Shared_coin_history,Product,Images
#from .forms import UserInterestForm,DeviceForm
from multiselectfield import MultiSelectFormField
from .sms import sms
from .fcm import FCM
#import pyotp
#from django import forms
# Register your models here.


# Admin Action Functions to update all employee gender as Male
#def update_gender_all(modeladmin, request, queryset):
 #   queryset.update(gender='Male')


# Action description
#update_gender_all.short_description = "Mark Selected Gender update as Male"

#def categories(instance):
    #return ', '.join(instance.categories)
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass
@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    pass
@admin.register(Yesdeal)
class YesdealAdmin(admin.ModelAdmin):
    pass
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    pass
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    pass

@admin.register(User_Vendor)
class UserVendorAdmin(admin.ModelAdmin):
    list_display=('user','vendor','numberOfRedeemableCoins','user_is_followed','totalCollectedDeals')
    #pass
@admin.register(User_Deal)
class UserDealAdmin(admin.ModelAdmin):
    list_display=('user','deal','vendor','is_collected','is_deal_redeemed')

@admin.register(Global)
class GlobalAdmin(admin.ModelAdmin):
    list_display = ('OTP_EXP_TIME',)
    def OTP_EXP_TIME(self,obj):
        return obj.EXP_TIME
    #pass
class InterestAdmin(admin.ModelAdmin):
    #list_display=('category_name',)
    #list_display_links = ('category_name',)
    pass
class ServiceLocAdmin(admin.ModelAdmin):
    exclude=('loc_id',)
    #pass
class VendorAdmin(admin.ModelAdmin):
    pass

@admin.register(Shared_coin_history)
class Shared_coin_historyAdmin(admin.ModelAdmin):
    exclude = ('numberOfRedeemableCoins',)
    list_display=('user','vendor','num_of_comp_coins','num_of_shared_coins','shared_method')
    #pass

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display=('userCD','Device_dtl')
    #form = DeviceForm

    def Device_dtl(self,obj):
        return obj.device
'''class DeviceAdmin(admin.ModelAdmin):
    list_display=('userCD','Device_dtl',)
    form = DeviceModelForm
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget }
    }
    def Device_dtl(self,obj):
        return obj.device'''

class UserAdmin(admin.ModelAdmin):
    exclude = ('created_at','userCD','user_token')   # exclude list of fields those not display in admin form
    # fields = ('name', 'address', 'gender','age')  # list of fields display in admin form
    # readonly_fields = ('age',)  # list of fields as readonly [NonEditable fields]
    sortable_by = 'id'  # field 'id' sorted by descending order
    #date_hierarchy = 'created_at'  # field 'created_at' as date field display as descending order
    search_fields = ['name','nick_name']#,'city','mobile']  # list of fields search in admin table
    list_display = ('name','mobile','Interest')#,'Following')#'city','email','gender','mobile') # list of fields display in admin table
    list_display_links = ('name',)#city')  # list of fields display in table show as link
    # list_select_related = ('type',)  # select_related in added only foreign key fields for query performance
    # raw_id_fields = ('product','type') # perfetch_related in added only manytomany fields for query performance
    list_filter = ('name','status')#'serviceLoc')  # list of fields filter in admin table
    #form=UserInterestForm
    #list_editable = ('',)  # list of fields editable in admin table
    #filter_vertical = ('product',)  # filter vertical in added only manytomany fields for filter will displayed
    #actions = [update_gender_all]  # admin action function called
    # group wise fields display in admin form
    # fieldsets = [
    #     ('Body', {'classes': ('full-width',), 'fields': ('address',)})
    # ]
    #change_list_template = 'admin/dashboard/admin_filter_list.html'  # admin template called

    # manytomany fields display in admin table and multiple value separate by comma
    def Interest(self,obj):
        return obj.interest
    def Following(self,obj):
        return obj.interested_vendors
    

    ''' @receiver(post_save, sender=User)
    def my_handler(sender,**kwargs):
        #print("saved successfully")
        user=User.objects.filter(userCD='CE5JKy')[0]
        data={"Name":user.name}
        print(user.name)
        ph=user.mobile
        otp=user.otp
        #totp=pyotp.TOTP('base32secret3232')
        #user.otp=totp.now()
        if not user.is_otp_verified:
            sms.sendMsg(ph,otp)
            User.objects.filter(userCD='CE5JKy').update(is_otp_verified=True)
        else:
            print("User Already verified")
        print(FCM.send_notification(user,"User creation","user created successfully",data))'''
        #return user

# unregister app
admin.site.unregister(Group)

# register app
admin.site.register(User, UserAdmin)
admin.site.register(Interest,InterestAdmin)
#admin.site.register(ServiceLoc,ServiceLocAdmin)
admin.site.register(Vendor,VendorAdmin)
#admin.site.register(Device,DeviceAdmin)


# admin header and title modification
admin.site.site_header = "Admin DashBoard"
admin.site.site_title = "DealApp"
admin.site.index_title = 'Welcome To Deal Portal'

#admin.site.register(User)






