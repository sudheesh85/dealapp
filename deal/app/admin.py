from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import path
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from .models import User,Interest,ServiceLoc #,User_Interest
from .forms import UserInterestForm
from multiselectfield import MultiSelectFormField
from .sms import sms
#import pyotp
#from django import forms
# Register your models here.


# Admin Action Functions to update all employee gender as Male
'''def update_gender_all(modeladmin, request, queryset):
    queryset.update(gender='Male')


# Action description
update_gender_all.short_description = "Mark Selected Gender update as Male"

#def categories(instance):
    #return ', '.join(instance.categories)'''

class InterestAdmin(admin.ModelAdmin):
    #list_display=('category_name',)
    #list_display_links = ('category_name',)
    pass
class ServiceLocAdmin(admin.ModelAdmin):
    exclude=('loc_id',)
    pass
class UserAdmin(admin.ModelAdmin):
    exclude = ('created_at','userCD')   # exclude list of fields those not display in admin form
    # fields = ('name', 'address', 'gender','age')  # list of fields display in admin form
    # readonly_fields = ('age',)  # list of fields as readonly [NonEditable fields]
    sortable_by = 'id'  # field 'id' sorted by descending order
    #date_hierarchy = 'created_at'  # field 'created_at' as date field display as descending order
    search_fields = ['name','nick_name']#,'city','mobile']  # list of fields search in admin table
    list_display = ('name','serviceLoc','mobile','Interest')#'city','email','gender','mobile') # list of fields display in admin table
    list_display_links = ('name',)#city')  # list of fields display in table show as link
    # list_select_related = ('type',)  # select_related in added only foreign key fields for query performance
    # raw_id_fields = ('product','type') # perfetch_related in added only manytomany fields for query performance
    list_filter = ('name','status','serviceLoc')  # list of fields filter in admin table
    form=UserInterestForm
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

    @receiver(post_save, sender=User)
    def my_handler(sender,**kwargs):
        #print("saved successfully")
        user=User.objects.filter(userCD='CE5JKy')[0]
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
        #return user
        
        


'''class User_InterestAdmin(admin.ModelAdmin):
    #exclude = ('category_id',)#'user_interest')
    list_display=('userCD','get_interest')
    #list_display_links=('userCD',)
    #change_list_template = 'admin/interest.html'
    form=UserInterestForm
    def get_interest(self,obj):
        #intr=User_Interest.objects.all().values('interest')
        #print(obj.userCD)
        intr=User_Interest.objects.all().last()
        print(obj.userCD,obj.interest)
        if intr.userCD == obj.userCD:
            usr_interest=obj.interest
        #print(usr_interest)
        for i in obj.interest:
            if i not in intr.interest:
                print("Entering")
                intr.interest.append(i)
        intr.save()
        return obj.interest
    def category(self,obj):
        intr=User_Interest.objects.all().values('interest')
        cat=Interest.objects.all().values('category_id')

        for i in intr:
            User_Interest.category_id=Interest.objects.only(cat).get(category_name=i)'''
        
        
            
        
  
# unregister app
admin.site.unregister(Group)

# register app
admin.site.register(User, UserAdmin)
admin.site.register(Interest,InterestAdmin)
admin.site.register(ServiceLoc,ServiceLocAdmin)
#admin.site.register(User_Interest,User_InterestAdmin)


# admin header and title modification
admin.site.site_header = "Admin DashBoard"
admin.site.site_title = "DealApp"
admin.site.index_title = 'Welcome To Deal Portal'

#admin.site.register(User)






