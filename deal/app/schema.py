import graphene
#import graphql_jwt
from graphene import relay,ObjectType, Schema,Mutation
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType
from app.models import User,Interest,Device,Yesdeal,Branch,Vendor,Region,Area,Shared_coin_history,User_Vendor,Images,Product,Deal_scratch,User_Deal
from .userid_gen import uid,otp
from .passwd_gen import tok,qr
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
class Vendor_Status(graphene.Enum):
    A="Active"
    P = "Approval Pending"
    D = "Deactivated"
class Provider_Type(graphene.Enum):
    V='Vendor'
    A='Admin'
class Deal_Status(graphene.Enum):
    A = 'ACTIVE'
    C = 'CONFIRMED'
    H = 'ON HOLD'
    D = 'DEACTIVATE'
class Age_Limit(graphene.Enum):
    A = '18-30'
    B = '31-40'
    C = '41-50'
    D = '51-60'
    E = '61-Above'
class Rating(graphene.Enum):
    1 = '*'
    2 = '**'
    3 = '***'
    4 = '****'
    5 = '*****'

class UserDealType(DjangoObjectType):
    class Meta:
        model = User_Deal
        filter_fields=[]
        interfaces = (relay.Node,)
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
class LogoType(DjangoObjectType):
    class Meta:
        model = Deal_scratch
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
class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        filter_fields=[]
        interfaces=(relay.Node,)
class ImageType(DjangoObjectType):
    class Meta:
        model = Images
        filter_fields=[]
        interfaces=(relay.Node,)
class ImagesInput(graphene.InputObjectType):
    img_title=graphene.String()
    category = graphene.String()
    vendor = graphene.String()
    product = graphene.String()
    provider = Provider_Type()
class ProductInput(graphene.InputObjectType):
    vendor = graphene.String()
    product_cd = graphene.String()
    product_name = graphene.String()
    product_category = graphene.String()
    item_price = graphene.Float()
    token = graphene.String()
class UserDealInput(graphene.InputObjectType):
    user = graphene.String()
    vendor = graphene.String()
    deal = graphene.String()
    is_collected = graphene.Boolean()
    is_deal_confirmed = graphene.Boolean()
    is_deal_redeemed = graphene.Boolean()
    deal_quantity = graphene.Int()
    user_wah_points = graphene.Int()
    user_rating = Rating()
    rating_status = graphene.String()
    user_review = graphene.List(graphene.String)
    deal_scratch_status = graphene.Boolean()
class YesdealInput(graphene.InputObjectType):
    deal_sku_cd = graphene.String()
    deal_title = graphene.String()
    deal_desc = graphene.String()
    deal_org_price = graphene.Float()
    deal_spl_price = graphene.Float()
    deal_category = graphene.Int()
    deal_count = graphene.Int()
    deal_vendor = graphene.Int()
    product = graphene.String()
    deal_available_branch = graphene.Int()
    deal_start_time = graphene.DateTime()
    deal_end_time = graphene.DateTime()
    deal_avail_max = graphene.Int()
    deal_collected_till = graphene.Int()
    deal_category_on_age = Age_Limit()
    deal_category_on_gender = Gender()
    deal_preference = graphene.String()
    Alloted_deal_per_coupon = graphene.Int()
    deal_status = Deal_Status()
class VendorInput(graphene.InputObjectType):
    user_name = graphene.String()
    password = graphene.String()
    user_pin = graphene.String()
    user_pin_verified = graphene.Boolean()
    vendor_token = graphene.String()
    vendor_name=graphene.String()
    phone_number = graphene.String()
    description = graphene.String()
    vendor_street = graphene.String()
    vendor_city = graphene.String()
    vendor_pin_code = graphene.String()
    totalDeals = graphene.Int()
    totalActiveDeals = graphene.Int()
    vendor_email = graphene.String()
    vendor_whatsapp = graphene.String()
    vendor_webpage = graphene.String()
    vendor_fb_link = graphene.String()
    vendor_twitter_link = graphene.String()
    vendor_status=Vendor_Status()
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
    user_lat = graphene.Float()
    user_long = graphene.Float()
class addProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput()
    product = graphene.Field(ProductType)    
    ok = graphene.String()
    @staticmethod
    def mutate(root,info,input=None):
        vendor_obj = Vendor.objects.get(vendor_cd=input.vendor)
        cat_obj = Interest.objects.get(category_id = input.product_category)
        if vendor_obj and vendor_obj.vendor_status == 'Active':
            if vendor_obj.vendor_token == input.token :
                product = Product.objects.create(
                    vendor = vendor_obj,
                    product_name = input.product_name,
                    product_category = cat_obj,
                    item_price = input.item_price
                )
                ok="Product added successfuly"
            else:
                raise GraphQLError('User must be authenticated')
        else:
            raise GraphQLError('Vendor must be registered')
        product.save()
        return addProduct(product=product,ok=ok)
                
class uploadVendorImg(graphene.Mutation):
    image = graphene.Field(ImageType)
    @staticmethod
    def mutate(root,info,input=None):
        files = info.context.Files['image']
        image = Image(
            img_title=input.img_titile,
            vendor = input.vendor,
            product = input.product,
            provider = input.provider)
        image.save()
        return uploadVendorImg(image = image)

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
        device=Device.objects.create(userCD=user,device=device)
        device.save()
        return addDevice(device=device)
class registerVendor(graphene.Mutation):
    class Arguments:
        input=VendorInput()
    vendor = graphene.Field(VendorType)
    ok = graphene.String()
    @staticmethod
    def mutate(root,info,input=None):
        vendor = Vendor(
            user_name = input.user_name,
            password = input.password,
            user_pin = input.user_pin,
            vendor_name = input.vendor_name,
            phone_number = input.phone_number,
            #description = input.description,
            vendor_street = input.vendor_street,
            vendor_city = input.vendor_city,
            vendor_pin_code = input.vendor_pin_code,
            #totalDeals = input.totalDeals,
            #totalActiveDeals = input.totalActiveDeals,
            #vendor_webpage = input.vendor_webpage,
            #vendor_fb_link = input.vendor_fb_link,
            #vendor_twitter_link = input.vendor_twitter_link,
            vendor_status = "Approval Pending"
        )
        ok = "Vendor registered successfully"
        vendor.save()
        return registerVendor(vendor=vendor,ok=ok)
class updateVendor(graphene.Mutation):
    class Arguments:
        input = VendorInput()
    upd_vendor = graphene.Field(VendorType)
    ok = graphene.String()
    @staticmethod
    def mutate(root,info,input=None):
        vendor = Vendor.objects.get(user_name=input.user_name)
        print(vendor,vendor.user_name,vendor.vendor_token)
        if vendor:
            if vendor.vendor_token == input.vendor_token:
                if input.vendor_name:
                    vendor.vendor_name = input.vendor_name
                if input.description:
                    vendor.description = input.description
                if input.totalDeals:
                    vendor.totalDeals = input.totalDeals
                if input.totalActiveDeals:
                    vendor.totalActiveDeals = input.totalActiveDeals
                if input.vendor_email:
                    vendor.vendor_email = input.vendor_email
                if input.vendor_whatsapp:
                    vendor.vendor_whatsapp = input.vendor_whatsapp
                if input.vendor_webpage:
                    vendor.vendor_webpage = input.vendor_webpage
                if input.vendor_fb_link:
                    vendor.vendor_fb_link = input.vendor_fb_link
                if input.vendor_twitter_link:
                    vendor.vendor_twitter_link = input.vendor_twitter_link
                if input.vendor_status:
                    vendor.vendor_status = input.vendor_status
                ok = "vendor updated successfully"
            else:
                ok = "user must be authorized"
                raise GraphQLError('User must be authenticated')
       
        vendor.save()
        return updateVendor(upd_vendor=vendor,ok=ok)
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
                raise GraphQLError('password is incorrect')

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

class verifyPIN(graphene.Mutation):
    class Arguments:
        input = VendorInput()
    ok = graphene.String()
    vendor = graphene.Field(VendorType)
    @staticmethod
    def mutate(root,info,input=None):
        vendor = Vendor.objects.get(user_name=input.user_name)
        if vendor:
            if vendor.user_pin == input.user_pin:
                vendor.pin_verified = True
                ok = "PIN Verified"
            else:
                vendor.pin_verified = False
                ok = "Incorrect PIN"
        else:
            ok = "Vendor doesnot exist"
        vendor.save()
        return verifyPIN(vendor = vendor,ok=ok)

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
        prd_obj = Product.objects.get(id = input.product)
        #input.deal_vendor = vendor
        deal=Yesdeal.objects.create(
            deal_vendor=vendor_obj,
            deal_title=input.deal_title,
            deal_desc = input.deal_desc,
            deal_count=input.deal_count,
            deal_org_price = input.deal_org_price,
            deal_spl_price = input.deal_spl_price,
            deal_category=category_obj,
            product = prd_obj,
            deal_available_branch = branch_obj,
            deal_srvc_city = city_obj,
            deal_srvc_area = area_obj,
            deal_start_time = input.deal_start_time,
            deal_end_time = input.deal_end_time,
            deal_avail_max = input.deal_avail_max,
            deal_collected_till = input.deal_collected_till,
            deal_category_on_age = input.deal_category_on_age,
            deal_category_on_gender = input.deal_category_on_gender,
            deal_preference = input.deal_preference,
            Alloted_deal_per_coupon = input.Alloted_deal_per_coupon,
            deal_status = input.deal_status)
        #if deal:
        deal.save()
        return AddDeal(deal=deal)
class collectDeal(graphene.Mutation):
    class Arguments:
        input = UserDealInput()
    ok = graphene.String()
    deal = graphene.Field(UserDealType)
    @staticmethod
    def mutate(root,info,input=None):
        vendor_obj = Vendor.objects.get(vendor_cd = input.vendor)
        user_obj = User.objects.get(userCD  = input.user)
        deal_obj = Yesdeal.objects.get(deal_id = input.deal)
        userdeal = User_Deal.objects.create(
            user = user_obj,
            deal = deal_obj,
            vendor = vendor_obj,
            is_collected = input.is_collected,
            QRCode = qr.qrcode(user_obj.userCD,deal_obj.deal_id),
            #is_deal_confirmed = input.is_deal_confirmed,
            #is_deal_redeemed = input.is_deal_redeemed,
            #deal_quantity = input.deal_quantity,
            #user_wah_points = input.user_wah_points,
            #deal_scratch_status = input.deal_scratch_status
        )
        userdeal.save()
        ok = "Entry made on user_deal table"
        return collectDeal(deal = userdeal,ok=ok)
class upd_collect_deal(graphene.Mutation):
    class Arguments:
        input = UserDealInput()
    upd_deal = graphene.Field(UserDealType)
    ok = graphene.String()
    @staticmethod
    def mutate(root,info,input=None):
        deal_obj = Yesdeal.objects.get(deal_id = input.deal)
        user_obj = User.objects.get(userCD  = input.user)
        upd_deal = User_Deal.objects.filter(user = user_obj.id,deal=deal_obj.id)
        
        #deal_obj = Yesdeal.objects.get(deal_id = input.deal)
        if upd_deal:
            print(upd_deal[0].is_deal_confirmed,upd_deal[0].user_wah_points,input.user_wah_points)
            if isinstance(input.is_deal_confirmed,bool):
                upd_deal[0].is_deal_confirmed = input.is_deal_confirmed
            if isinstance(input.is_deal_redeemed,bool):
                upd_deal[0].is_deal_redeemed = input.is_deal_redeemed
            if input.user_wah_points:
                print(input.user_wah_points)
                upd_deal[0].user_wah_points = input.user_wah_points
                print(upd_deal[0].user_wah_points)
            if input.deal_quantity:
                upd_deal[0].deal_quantity = input.deal_quantity
            if isinstance(input.deal_scratch_status,bool):
                upd_deal[0].deal_scratch_status = input.deal_scratch_status
            if input.user_rating:
                upd_deal[0].user_rating = input.user_rating
            if input.rating_status:
                upd_deal[0].rating_status = input.rating_status
            if input.user_review:
                upd_deal[0].user_review = input.user_review
        else:
            ok = "user or deal does not exist"
        upd_deal[0].save()
        ok="use deal table updated"
        print(upd_deal[0].user_wah_points)
        return upd_collect_deal(upd_deal = upd_deal[0],ok=ok )
class Mutation(ObjectType):
    #add_user = AddUser.Field()
    Resend_otp=ResendOTP.Field()
    verify_otp=verifyOTP.Field()
    add_interest=AddInterest.Field()
    add_device=addDevice.Field()
    register_vendor = registerVendor.Field()
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
    upd_vendor = updateVendor.Field()
    upload_image = uploadVendorImg.Field()
    add_Product = addProduct.Field()
    verify_PIN = verifyPIN.Field()
    collect_deal = collectDeal.Field()
    update_collect = upd_collect_deal.Field()

class Query(ObjectType):
    user = graphene.Field(UserType, userCD=graphene.String())
    interest=graphene.Field(InterestType,pk=graphene.Int())
    deal = graphene.List(lambda:graphene.List(YesdealType),userCD=graphene.String(),token =graphene.String(required=True))
    jeep=graphene.String()
    userVendor = graphene.List(UserVendorType,user=graphene.String(required=True),vendor=graphene.String())
    dealImages = graphene.List(ImageType,vendor=graphene.String(),product=graphene.String(),provider=graphene.String())
    catImages = graphene.List(ImageType,category = graphene.String(),provider=graphene.String())
    vendor_product = graphene.List(ProductType,vendor = graphene.String())
    get_user_deal = graphene.List(UserDealType,user=graphene.String(),deal=graphene.String())
    all_user=DjangoFilterConnectionField(UserType)
    all_interest=DjangoFilterConnectionField(InterestType)
    all_device=DjangoFilterConnectionField(DeviceType)
    all_deal = DjangoFilterConnectionField(YesdealType)
    all_vendor = DjangoFilterConnectionField(VendorType)
    all_images = DjangoFilterConnectionField(ImageType)
    all_product = DjangoFilterConnectionField(ProductType)
    get_logo = DjangoFilterConnectionField(LogoType)

    #def resolve_car(self,info):
        #return Car.objects.all()
    def resolve_get_logo(self,info,**kwargs):
        return Deal_scratch.objects.all()
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
    def resolve_get_user_deal(self,info,**kwargs):
        user = kwargs.get("user")
        deal = kwargs.get("deal")
        deal_obj = Yesdeal.objects.get(deal_id = deal)
        user_obj = User.objects.get(userCD  = user)
        return User_Deal.objects.filter(user=user_obj.id,deal=deal_obj.id)
    def resolve_catImages(self,info,**kwargs):
        print("here")
        category = kwargs.get("category")
        provider = kwargs.get("provider")
        cat_obj = Interest.objects.get(category_id=category)
        print(cat_obj.id)
        return Images.objects.filter(category_id=cat_obj.id,provider=provider)
    def resolve_dealImages(self,info,**kwargs):
        print("here")
        vendor = kwargs.get("vendor")
        product = kwargs.get("product")
        provider = kwargs.get("provider")
        vendor_obj = Vendor.objects.get(vendor_cd = vendor)
        prd_obj = Product.objects.get(product_cd = product)
        print(vendor,product)
        return Images.objects.filter(vendor_id=vendor_obj.id,product_id=prd_obj.id,provider=provider)
    def resolve_vendor_product(self,info,**kwargs):
        vendor = kwargs.get("vendor")
        vendor_obj = Vendor.objects.get(vendor_cd = vendor)
        return Product.objects.filter(vendor_id = vendor_obj.id)
        
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
    def resolve_all_images(self,info,**kwargs):
        return Images.objects.all()
    def resolve_all_product(self,info,**kwargs):
        return Product.objects.all()

schema = Schema(query=Query,mutation=Mutation)