import graphene
#import graphql_jwt
from graphene import relay,ObjectType, Schema,Mutation
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType
from app.models import User,Interest,Device,Yesdeal,Branch,Vendor,Region,Area,Shared_coin_history,User_Vendor
from .userid_gen import uid,otp
from .passwd_gen import tok
from datetime import datetime as dt
from django.utils import timezone
from graphql import GraphQLError

class Gender(graphene.Enum):
    Male = "Male"
    Female = "Female"
class Status(graphene.Enum):
    A = "Active"
    I = "Inactive"
    T = "Terminated"
    S = "Suspended"
class Shared_method(graphene.Enum):
    R = "Received"
    S = "Send"
    C = "Complement"
class Venor_Status(graphene.Enum):
    A="Active"
    P = "Approval Pending"
    D = "Deactivated"

class YesdealType(DjangoObjectType):
    class Meta:
        model = Yesdeal
        filter_fields=[]
        interfaces = (relay.Node,)
class VendorType(DjangoObjectType):
    class Meta:
        model = Vendor
        filter_fields=[]
        interfaces = (relay.Node,)

class BranchType(DjangoObjectType):
    class Meta:
        model = Branch
        filter_fields=[]
        interfaces = (relay.Node,)

class UserType(DjangoObjectType):
    class Meta:
        model=User
        filter_fields = ['mobile']
        interfaces = (relay.Node, )
class InterestType(DjangoObjectType):
    class Meta:
        model = Interest
        filter_fields=[]
        interfaces = (relay.Node, )
class RegionType(DjangoObjectType):
    class Meta:
        model = Region
        filter_fields=[]
        interfaces = (relay.Node,)
class AreaType(DjangoObjectType):
    class Meta:
        model = Area
        filter_fields=[]
        interfaces = (relay.Node,)
class SharedType(DjangoObjectType):
    class Meta:
        model = Shared_coin_history
        filter_fields=[]
        interfaces = (relay.Node,)
class UserVendorType(DjangoObjectType):
    class Meta:
        model = User_Vendor
        filter_fields=[]
        interfaces = (relay.Node,)
class DeviceType(DjangoObjectType):
    class Meta:
        model=Device
        filter_fields=[]
        interfaces=(relay.Node,)
class YesdealInput(graphene.InputObjectType):
    deal_sku_cd = graphene.String()
    deal_title = graphene.String()
    deal_desc = graphene.String()
    deal_org_price = graphene.Float()
    deal_spl_price = graphene.Float()
    deal_category = graphene.Int()
    deal_count = graphene.Int()
    deal_vendor = graphene.Int()
    deal_available_branch = graphene.Int()
class VendorInput(graphene.InputObjectType):
    user_name = graphene.String()
    password = graphene.String()
    vendor_token = graphene.String()
    vendor_name=graphene.String()
    phone_number = graphene.String()
    description = graphene.String()
    vendor_street = graphene.String()
    vendor_city = graphene.String()
    location_pin = graphene.String()
    totalDeals = graphene.Int()
    totalActiveDeals = graphene.Int()
    vendor_webpage = graphene.String()
    vendor_fb_link = graphene.String()
    vendor_twitter_link = graphene.String()
#class VendorloginInput(graphene.InputObjectType):
    #user_name = graphene.String()
    #password = graphene.String()
    #vendor_token = graphene.String()
class SharedInput(graphene.InputObjectType):
    user = graphene.String()
    vendor = graphene.String()
    numberOfRedeemableCoins = graphene.Int()
    num_of_comp_coins = graphene.Int()
    num_of_shared_coins = graphene.Int()
    shared_method = Shared_method()
class UserVendorInput(graphene.InputObjectType):
    user = graphene.String()
    vendor = graphene.String()
    user_is_followed = graphene.Boolean()
    numberOfRedeemableCoins = graphene.Int()
    totalCollectedDeals = graphene.String()
class BranchInput(graphene.InputObjectType):
    vendor = graphene.String()
    branch_name = graphene.String()
    branch_street = graphene.String()
    branch_city = graphene.String()
    branch_pin = graphene.String()
    branch_contact = graphene.String()
class RegionInput(graphene.InputObjectType):
    pass
class AreaInput(graphene.InputObjectType):
    pass

class UserInput(graphene.InputObjectType):
    name=graphene.String()
    userCD=graphene.String()
    user_token = graphene.String()
    mobile=graphene.String()
    status=graphene.String()
    interest=graphene.List(graphene.String)
    otp=graphene.String()
    otp_exp_time=graphene.DateTime()
    is_otp_verified=graphene.Boolean()
    gender = Gender()
    status = Status()
    
class DeviceInput(graphene.InputObjectType):
    device=graphene.JSONString()

class addDevice(graphene.Mutation):
    class Arguments:
        #userCD=graphene.String()
        input=UserInput(required=True) 
        device=DeviceInput()
    device=graphene.Field(DeviceType)
    @staticmethod
    def mutate(root,info,input=None,device=None):
        print(device.device)
        user=User.objects.get(mobile=input.mobile)
        print(user.userCD)
        device=Device.objects.create(userCD=user,device=device.device)
        device.save()
        return addDevice(device=device)
class addVendor(graphene.Mutation):
    class Arguments:
        input=VendorInput()
    vendor = graphene.Field(VendorType)
    ok = graphene.String()
    @staticmethod
    def mutate(root,info,input=None):
        vendor = Vendor(
            user_name = input.user_name,
            password = input.password,
            vendor_name = input.vendor_name,
            phone_number = input.phone_number,
            description = input.description,
            vendor_street = input.vendor_street,
            vendor_city = input.vendor_city,
            location_pin = input.location_pin,
            totalDeals = input.totalDeals,
            totalActiveDeals = input.totalActiveDeals,
            vendor_webpage = input.vendor_webpage,
            vendor_fb_link = input.vendor_fb_link,
            vendor_twitter_link = input.vendor_twitter_link,
            vendor_status = "Approval Pending"
        )
        ok = "Vendor registered successfully"
        vendor.save()
        return addVendor(vendor=vendor,ok=ok)
class vendorLogin(graphene.Mutation):
    class Arguments:
        input=VendorInput()
    login = graphene.Field(VendorType)
    ok = graphene.String() 
    @staticmethod
    def mutate(root,info,input=None):
        login = Vendor.objects.get(user_name=input.user_name)
        if login and login.vendor_status == 'Active':
            if login.password == input.password:
                login.vendor_token = tok.get_token()
                ok = "login successfully"
            else:
                ok = "password is incorrect"

        else:
            ok = "Either vendor does not exist or active in the system "
        login.save()
        return vendorLogin(login=login,ok=ok)
class updatePassword(graphene.Mutation):
    class Arguments:
        input=VendorInput()
    upd_pwd = graphene.Field(VendorType)
    ok = graphene.String()
    @staticmethod
    def mutate(root,info,input=None):
        upd_pwd = Vendor.objects.get(user_name = input.user_name)
        if upd_pwd and upd_pwd.vendor_status == 'Active':
            upd_pwd.password = input.password
            upd_pwd.vendor_token = tok.get_token()
            ok = "password has been changed successfully"
        else:
            ok="Vendor is not active in the system"
        upd_pwd.save()
        return updatePassword(upd_pwd=upd_pwd,ok=ok)

class addBranch(graphene.Mutation):
    class Arguments:
        input=BranchInput()
    branch = graphene.Field(BranchType)
    @staticmethod
    def mutate(root,info,input=None):
        vendor_obj = Vendor.objects.get(vendor_cd = input.vendor)
        branch = Branch.objects.create(
            vendor=vendor_obj,
            branch_name = input.branch_name,
            branch_street = input.branch_street,
            branch_city = input.branch_city,
            branch_pin = input.branch_pin,
            branch_contact = input.branch_contact
        )
        branch.save()
        return addBranch(branch=branch)
class updateCoin(graphene.Mutation):
    class Arguments:
        input = SharedInput()
    ok = graphene.String()
    user_coin = graphene.Field(SharedType)
    @staticmethod
    def mutate(root,info,input=None):
        user_obj = User.objects.get(userCD  = input.user)
        vendor_obj = Vendor.objects.get(vendor_cd =input.vendor)
        user_coin = Shared_coin_history.objects.filter(user = user_obj.id,vendor = vendor_obj.id).latest('shared_at')
        #vendor_obj = Vendor.objects.get(id =input.vendor)
        #user_obj = User.objects.get(userCD  = input.user)
        if user_coin:
            print("coins:",user_coin,type(user_coin.numberOfRedeemableCoins))
            init_coin = user_coin.numberOfRedeemableCoins
        else:
            init_coin = 0
        if input.shared_method == 'Send' and init_coin > input.num_of_shared_coins:
            init_coin = init_coin - input.num_of_shared_coins
        else:
            ok = "User does not have enough coin to send"
        if input.shared_method =='Received':
            init_coin = init_coin + input.num_of_shared_coins
        if input.shared_method == 'Complement':
            init_coin = init_coin + input.num_of_comp_coins
        shared_coin = Shared_coin_history.objects.create(
            user = user_obj,
            vendor = vendor_obj,
            numberOfRedeemableCoins = init_coin,
            num_of_shared_coins = input.num_of_shared_coins,
            num_of_comp_coins = input.num_of_comp_coins,
            shared_method = input.shared_method)
        shared_coin.save()
        return updateCoin(user_coin = shared_coin)    
class updateUserVendor(graphene.Mutation):
    class Arguments:
        input = UserVendorInput()
    ok = graphene.String()
    user_vendor = graphene.Field(UserVendorType)
    @staticmethod
    def mutate(root,info,input=None):
        user_obj = User.objects.get(userCD  = input.user)
        vendor_obj = Vendor.objects.get(vendor_cd =input.vendor)
        user_vendor = User_Vendor.objects.filter(user = user_obj.id,vendor = vendor_obj.id)
        shared_obj = Shared_coin_history.objects.filter(user = user_obj.id,vendor = vendor_obj.id).latest('shared_at')
        #vendor_obj = Vendor.objects.get(id =input.vendor)
        #user_obj = User.objects.get(id  = input.user)
        if user_vendor:
            print("inside",shared_obj.numberOfRedeemableCoins)
            #if input.user_is_followed:
            user_vendor[0].user_is_followed = input.user_is_followed
            print(user_vendor[0].user_is_followed)
            if input.totalCollectedDeals:
                user_vendor[0].totalCollectedDeals = input.totalCollectedDeals
            user_vendor[0].numberOfRedeemableCoins = shared_obj
            user_vendor[0].save()
            return updateUserVendor(user_vendor=user_vendor[0])
        else:
            user_vendor = User_Vendor.objects.create(
                user = user_obj,
                vendor = vendor_obj,
                user_is_followed = input.user_is_followed,
                numberOfRedeemableCoins = shared_obj,
                totalCollectedDeals = input.totalCollectedDeals
            )
            user_vendor.save()
            return updateUserVendor(user_vendor=user_vendor)
class AddUser(graphene.Mutation):
    class Arguments:
        #id=graphene.ID(required=True)
        input=UserInput(required=True) 
    ok=graphene.String()  
    user=graphene.Field(UserType)

    @staticmethod
    def mutate(root, info,input=None):
        print(input.mobile)
        user,created = User.objects.get_or_create(mobile=input.mobile)
        print("user:",created)
        if created:
            user.save()
            ok="New user hs been created"
            return AddUser(user=user,ok=ok)
        else:
            ok="User already exist please call UpdateUser"
            return AddUser(ok=ok)
class SendOTP(graphene.Mutation):
    class Arguments:
        mobile = graphene.String()
    ok = graphene.String()
    user = graphene.Field(UserType)
    @staticmethod
    def mutate(root,info,mobile):
        user,created = User.objects.get_or_create(mobile=mobile)
        if created:

            ok="OTP for new user has been created"
        else:
            user.user_token = user.user_token.replace(user.user_token[:6],'xxxxxx')
            user.otp=otp.get_otp()
            user.is_otp_verified=False
            user.otp_exp_time=otp.get_exp_time()
            ok="OTP for existing user has been created"
        user.save()
        return SendOTP(user=user,ok=ok)


class UpdateUser(graphene.Mutation):
    class Arguments:
        input = UserInput()
    ok=graphene.String()
    user = graphene.Field(UserType)
    @staticmethod
    def mutate(root,info,input=None):
        user = User.objects.get(userCD = input.userCD)
        condition = [user.is_otp_verified,user.user_token == input.user_token]
        if all(condition) :
            if user.userCD == input.userCD  :
                if input.name:
                    user.name=input.name
                if input.gender:
                    user.gender = input.gender
                if input.status:
                    user.status = input.status
                #if input.mobile:
                    #user.mobile=input.mobile
                if input.interest:
                    #user.interest=input.interest
                    user.interest.set(input.interest)
            user.save()
            ok="User has been updated"
            return UpdateUser(user=user,ok=ok)
        else:
            raise GraphQLError('User must be authenticated')


class verifyOTP(graphene.Mutation):
    class Arguments:
        input=UserInput(required=True) 
    ok = graphene.String()
    user = graphene.Field(UserType)
    @staticmethod
    def mutate(root,info,input=None):
        user=User.objects.get(mobile=input.mobile)
        ctime=timezone.now()
        print(ctime)
        condition=[user.otp==input.otp,not user.is_otp_verified,ctime < user.otp_exp_time]
        if not user.userCD:
            user.userCD = uid.make_id()
            user.user_token = tok.get_token()
            user.created_at = ctime
            if all(condition):
                user.is_otp_verified=True
                user.otp="xxxxxx"
                ok="OTP has been verified and user has been created"
            else:
                ok="OTP verification failed"
        else:
            if all(condition):
                user.user_token = tok.get_token()
                user.is_otp_verified=True
                user.otp="xxxxxx"
                ok="OTP has been verified"
            else:
                user.is_otp_verified=False
                ok="OTP verification failed"
        user.save()
        return verifyOTP(user=user,ok=ok)

class ResendOTP(graphene.Mutation):
    class Arguments:
        mobile = graphene.String()
    ok = graphene.String()
    user = graphene.Field(UserType)
    @staticmethod
    def mutate(root,info,mobile):
        try:
            user = User.objects.get(mobile=mobile)
            #user.user_token = tok.get_token()
            user.otp=otp.get_otp()
            user.is_otp_verified=False
            user.otp_exp_time=otp.get_exp_time()
            ok="OTP for existing user has been resent"
            user.save()
            return ResendOTP(user=user,ok=ok)
        except:
            ok="User does not exist"
            return ResendOTP(ok=ok)
class InterestInput(graphene.InputObjectType):
    category_name=graphene.String()
    category_id = graphene.Int()
class AddInterest(graphene.Mutation):
    class Arguments:
        input=InterestInput(required=True)
    interest=graphene.Field(InterestType)
    @staticmethod
    def mutate(root,info,input=None):

        interest=Interest(
            category_id=input.category_id,
            category_name=input.category_name
        )
        interest.save()
        return AddInterest(interest=interest)
class AddDeal(graphene.Mutation):
    class Arguments:
        input = YesdealInput()
    deal = graphene.Field(YesdealType)
    @staticmethod
    def mutate(root,info,input=None):
        vendor_obj = Vendor.objects.get(id=input.deal_vendor)
        category_obj = Interest.objects.get(id=input.deal_category)
        branch_obj = Branch.objects.get(id=input.deal_available_branch)
        city_obj = Region.objects.get(id=input.deal_srvc_city)
        area_obj = Area.objects.get(id=input.deal_srvc_area)
        #input.deal_vendor = vendor
        deal=Yesdeal.objects.create(
            deal_vendor=vendor_obj,
            deal_title=input.deal_title,
            deal_desc = input.deal_desc,
            deal_count=input.deal_count,
            deal_org_price = input.deal_org_price,
            deal_spl_price = input.deal_spl_price,
            deal_category=category_obj,
            deal_available_branch = branch_obj,
            deal_srvc_city = city_obj,
            deal_srvc_area = area_obj)
        #if deal:
        deal.save()
        return AddDeal(deal=deal)
class Mutation(ObjectType):
    #add_user = AddUser.Field()
    Resend_otp=ResendOTP.Field()
    verify_otp=verifyOTP.Field()
    add_interest=AddInterest.Field()
    add_device=addDevice.Field()
    add_vendor = addVendor.Field()
    update_user=UpdateUser.Field()
    add_deal = AddDeal.Field()
    #token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    #verify_token = graphql_jwt.Verify.Field()
    #refresh_token = graphql_jwt.Refresh.Field()
    sendOTP = SendOTP.Field()
    shared_coin = updateCoin.Field()
    user_vendor = updateUserVendor.Field()
    add_branch = addBranch.Field()
    vendor_login = vendorLogin.Field()
    forgot_password = updatePassword.Field()

class Query(ObjectType):
    user = graphene.Field(UserType, userCD=graphene.String())
    interest=graphene.Field(InterestType,pk=graphene.Int())
    deal = graphene.List(lambda:graphene.List(YesdealType),userCD=graphene.String(),token =graphene.String(required=True))
    jeep=graphene.String()
    userVendor = graphene.List(UserVendorType,user=graphene.String(required=True),vendor=graphene.String())
    #all_cars=graphene.List(CarType)
    all_user=DjangoFilterConnectionField(UserType)
    all_interest=DjangoFilterConnectionField(InterestType)
    all_device=DjangoFilterConnectionField(DeviceType)
    all_deal = DjangoFilterConnectionField(YesdealType)
    all_vendor = DjangoFilterConnectionField(VendorType)

    #def resolve_car(self,info):
        #return Car.objects.all()

    def resolve_user(self, info,**kwargs):
        userCD=kwargs.get("userCD")
        user = info.context.user
        print(user)
        if userCD is not None:
            return User.objects.get(userCD=userCD)
        #return f"Mercedes Benz | Model:23qwer | Color: Black"'''
    def resolve_userVendor(self,info,**kwargs):
        user = kwargs.get("user")
        vendor = kwargs.get("vendor") 
        user_obj = User.objects.get(userCD  = user)
        vendor_obj = Vendor.objects.get(vendor_cd = vendor)
        return User_Vendor.objects.filter(user=user_obj.id,vendor=vendor_obj.id)
    def resolve_deal(self,info,**kwargs):
        userCD = kwargs.get("userCD")
        user_token=kwargs.get("token")
        if userCD is not None:
            user = User.objects.get(userCD=userCD)
            #a=app_user_interest.objects.all()
            #print(a)
            #intr=a.category_name.all(user_id=user.id)
            #print(user.id)
            if user.user_token == user_token:
                user_deal=[]
                interest=user.interest.all().values('id')

                print(interest)
                for value in interest:
                    for key,id in value.items():
                    #print(id)
                        coll_deal = Yesdeal.objects.filter(deal_category_id=id)
                        print(id,coll_deal)
                        if coll_deal:
                            user_deal.append(coll_deal)
                return user_deal
            else:
                raise GraphQLError('User must be authenticated')
        else:
            raise GraphQLError("UserCD must be passed as input argument")
    def resolve_all_deal(self,info,**kwargs):
        return Yesdeal.objects.all()
    def resolve_jeep(self,info):
        return f'ya hoo!!!'
    def resolve_all_user(self,info,**kwargs):
        return User.objects.all()
    def resolve_interest(self,info,**kwargs):
        id=kwargs.get("pk")
        if id is not None:
            return Interest.objects.get(id=id)
    def resolve_all_interest(self,info,**kwargs):
        return Interest.objects.all()
    def resolve_all_device(self,info,**kwargs):
        return Device.objects.all()
    def resolve_all_vendor(self,info,**kwargs):
        return Vendor.objects.all()

schema = Schema(query=Query,mutation=Mutation)